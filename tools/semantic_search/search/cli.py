import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

import numpy as np
from tqdm import tqdm

from .chunker import MarkdownChunker
from .embedding import EmbeddingClient
from .index import ForwardIndex
from .models import Chunk, SearchResult


def extract_features_parallel(
    file_paths: List[str],
    chunker: MarkdownChunker,
    embedder: EmbeddingClient,
    index: ForwardIndex,
    num_workers: int = 4
) -> List[Chunk]:
    """并行提取特征。"""
    all_new_chunks = []

    def process_file(file_path: str):
        try:
            path = Path(file_path)
            if not path.exists():
                return []

            mtime = path.stat().st_mtime
            if not index.needs_update(file_path, mtime):
                return []

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            chunks = chunker.chunk(file_path, content)
            if not chunks:
                return []

            # 获取 embeddings
            embeddings = embedder.embed_batch([c.text for c in chunks])
            for c, emb in zip(chunks, embeddings):
                c.embedding = np.array(emb, dtype=np.float32)

            return chunks
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)
            return []

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # 使用 tqdm 在 stderr 显示进度
        results = list(tqdm(
            executor.map(process_file, file_paths),
            total=len(file_paths),
            desc="Extracting features",
            file=sys.stderr
        ))

    for chunks in results:
        all_new_chunks.extend(chunks)

    return all_new_chunks

def main():
    parser = argparse.ArgumentParser(description="Semantic Search CLI for Knowledge Base")
    parser.add_argument("--cache-dir", default=".knowledge_cache", help="Directory to store cache files")
    parser.add_argument("--file-list", required=True, help="Path to a text file containing list of MD files to search")
    parser.add_argument("--query", required=True, help="Natural language query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers for embedding")
    parser.add_argument("--endpoint", default="http://localhost:1234/v1", help="Embedding API endpoint")
    parser.add_argument("--model", default="text-embedding-qwen3-embedding-8b", help="Embedding model name")

    args = parser.parse_args()

    cache_dir = Path(args.cache_dir)
    index = ForwardIndex(cache_dir)
    chunker = MarkdownChunker()
    embedder = EmbeddingClient(base_url=args.endpoint, model=args.model)

    # 1. 读取待搜索文件列表
    with open(args.file_list, 'r') as f:
        target_files = [line.strip() for line in f if line.strip()]

    # 2. 检查并更新 Cache (分批处理以支持断点保存)
    batch_size = 50 # 每 50 个文件保存一次索引
    for i in range(0, len(target_files), batch_size):
        batch = target_files[i:i + batch_size]
        new_chunks = extract_features_parallel(batch, chunker, embedder, index, num_workers=args.workers)
        if new_chunks:
            updated_files = {}
            for c in new_chunks:
                updated_files[c.source_file] = Path(c.source_file).stat().st_mtime
            index.save(new_chunks, updated_files)
            print(f"Batch {i//batch_size + 1} complete. Updated cache with {len(new_chunks)} new chunks from {len(updated_files)} files.", file=sys.stderr)

    # 3. 获取子集向量进行搜索
    subset_chunks, subset_embeddings = index.get_subset(target_files)

    if not subset_chunks or subset_embeddings is None:
        print(json.dumps([]))
        return

    # 4. 执行 Brute Force 搜索 (NumPy 实现)
    query_vec = np.array(embedder.embed(args.query), dtype=np.float32)

    # 归一化以进行余弦相似度计算
    # subset_embeddings shape: (n_chunks, dim)
    norms = np.linalg.norm(subset_embeddings, axis=1, keepdims=True)
    # 避免除以 0
    norms[norms == 0] = 1.0
    norm_embeddings = subset_embeddings / norms

    query_norm = np.linalg.norm(query_vec)
    if query_norm > 0:
        norm_query = query_vec / query_norm
    else:
        norm_query = query_vec

    similarities = norm_embeddings @ norm_query

    # 获取 Top-K
    top_k = min(args.top_k, len(subset_chunks))
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    results = [
        SearchResult(chunk=subset_chunks[i], score=float(similarities[i])).to_dict()
        for i in top_indices
    ]

    # 5. 输出结果到 stdout
    print(json.dumps(results, indent=2, ensure_ascii=False, default=str))

if __name__ == "__main__":
    main()

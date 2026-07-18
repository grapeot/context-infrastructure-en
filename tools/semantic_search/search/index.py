import fcntl
import json
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from .models import Chunk


class ForwardIndex:
    """存储和管理 Chunks 及其 Embedding。使用 mmap 优化加载性能。"""

    def __init__(self, index_dir: Path, dim: int = 4096):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.dim = dim
        self.embeddings_path = self.index_dir / "embeddings.npy"
        self.chunks_path = self.index_dir / "chunks.pkl"
        self.manifest_path = self.index_dir / "manifest.json"
        self.lock_path = self.index_dir / "index.lock"

        self.embeddings: Optional[np.ndarray] = None
        self.chunks: List[Chunk] = []
        self.manifest: Dict[str, Any] = {} # file_path -> {mtime, chunk_indices}

        self.load()

    def _get_lock(self, exclusive: bool = False):
        """获取文件锁。"""
        mode = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
        f = open(self.lock_path, 'w')
        fcntl.flock(f, mode)
        return f

    def load(self):
        """加载索引。使用 mmap 模式读取向量。"""
        if not self.manifest_path.exists():
            return

        with self._get_lock(exclusive=False) as _:
            with open(self.manifest_path, 'r') as f:
                self.manifest = json.load(f)

            if self.chunks_path.exists():
                with open(self.chunks_path, 'rb') as f:
                    self.chunks = pickle.load(f)

            if self.embeddings_path.exists():
                # 使用 mmap 只读模式加载，几乎瞬时
                self.embeddings = np.load(self.embeddings_path, mmap_mode='r')

    def save(self, new_chunks: List[Chunk], updated_files: Dict[str, float]):
        """保存/更新索引。需要排他锁。"""
        with self._get_lock(exclusive=True) as _:
            # 1. 更新 chunks 列表
            # 注意：这只是一个简单的实现。生产环境可能需要更精细的增量更新逻辑
            # 这里我们假设 new_chunks 是要追加或替换的

            # 简化的逻辑：先加载旧的，合并，再保存
            # 如果索引很大，这种方式会变慢。但对于个人知识库没问题。
            all_chunks = self.chunks

            # 移除被更新文件的旧 chunks
            all_chunks = [c for c in all_chunks if c.source_file not in updated_files]

            # 追加新 chunks
            start_idx = len(all_chunks)
            all_chunks.extend(new_chunks)

            # 更新 manifest
            for file_path, mtime in updated_files.items():
                indices = [i for i, c in enumerate(all_chunks) if c.source_file == file_path]
                self.manifest[file_path] = {
                    "mtime": mtime,
                    "indices": indices
                }

            self.chunks = all_chunks

            # 2. 保存元数据
            with open(self.chunks_path, 'wb') as f:
                pickle.dump(self.chunks, f)
            with open(self.manifest_path, 'w') as f:
                json.dump(self.manifest, f)

            # 3. 保存 Embeddings
            # 将所有 chunks 的 embedding 组合成一个大矩阵
            embeddings_list = [c.embedding for c in self.chunks]
            if embeddings_list:
                embeddings_array = np.array(embeddings_list, dtype=np.float32)
                np.save(self.embeddings_path, embeddings_array)
                # 重新加载为 mmap 模式
                self.embeddings = np.load(self.embeddings_path, mmap_mode='r')

    def get_subset(self, file_paths: List[str]) -> Tuple[List[Chunk], Optional[np.ndarray]]:
        """获取指定文件列表对应的子集。"""
        # 由于我们使用 mmap，可以直接通过索引访问 self.embeddings
        target_chunks = []
        indices = []

        file_set = set(file_paths)
        for i, chunk in enumerate(self.chunks):
            if chunk.source_file in file_set:
                target_chunks.append(chunk)
                indices.append(i)

        if not indices or self.embeddings is None:
            return target_chunks, None

        subset_embeddings = self.embeddings[indices]
        return target_chunks, subset_embeddings

    def needs_update(self, file_path: str, current_mtime: float) -> bool:
        """检查文件是否需要更新特征提取。"""
        record = self.manifest.get(file_path)
        if not record:
            return True
        return record.get("mtime") != current_mtime

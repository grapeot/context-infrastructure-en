---
id: axiom_dependency_topology_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T06. Dependency Topology Over Task Count

## 1. Core Axiom

Choose architecture based on the dependency graph (parallelizability, critical path, coupling coefficient), not based on how many tasks you can list. Task count is a vanity metric; the real enemy is serial constraints and tight coupling in the topology.

## 2. Deep Reasoning

### The Task Count Trap

Being able to list ten tasks sounds organized, but it masks the real question: what are the dependency relationships among those ten tasks? If they form a long chain (Task 1 → Task 2 → ... → Task 10), then no matter how many agents you use, the critical path length determines the final duration. Multi-agent coordination overhead will actually drag down overall speed. Conversely, if those ten tasks can be divided into five groups, each internally highly coupled but independent across groups, then a five-agent architecture can fully exploit parallelism. Task count itself carries zero information; topology is what matters.

### Three Key Dimensions of the Dependency Graph

**Parallelizability**: The maximum number of tasks that can execute simultaneously at any moment. This directly determines the upper bound of multi-agent systems. If parallelizability is only 2, then no matter how many agents you have, only two can work at the same time — the rest either wait or do useless work. Empirical research shows: when parallelizability ≤ 2, a single agent is superior; at 3–5, Orchestrator-Worker architecture starts to yield benefits; only above 5 is it worth considering Hierarchical or Decentralized architectures.

**Critical Path Length**: The longest dependency chain from start to finish. This is the quantification of serial constraints. Even with high parallelizability, if the critical path is long, the entire system will still be dragged down by this chain. For example, in educational video generation, the Solution Agent must finish first before Illustration and Narration can proceed in parallel; this Solution → {Illustration, Narration} chain determines the minimum duration. Shortening the critical path is often more effective than increasing parallelizability.

**Coupling Coefficient**: The density of dependencies among tasks. High coupling means a change in one task's output cascades to affect multiple downstream tasks, amplifying error propagation. In multi-agent systems, high coupling leads to frequent synchronization and recomputation, canceling out the benefits of parallelism. Low-coupling systems allow each agent to work relatively independently, interacting only at clearly defined interfaces.

### Topology-Driven Architecture Selection

These three dimensions jointly determine the optimal architecture. A single agent suits tasks with high coupling and low parallelizability, because it avoids multi-agent coordination overhead. Orchestrator-Worker architecture suits tasks with moderate parallelizability (3–5) and clear dependency relationships — a central coordinator handles task decomposition and scheduling, while Workers execute independently. Hierarchical architecture suits tasks with high parallelizability but long critical paths, managing complexity through multi-level recursive decomposition. Decentralized architecture suits tasks with low coupling and high parallelizability, with peer-to-peer communication among agents and no central coordination.

The key insight: architecture is not determined by how many agents you want — it is determined by the task's topology. If you first decide "I want to use five agents" and then forcibly split the task into five pieces, you will create artificial dependencies and synchronization points, actually reducing efficiency. The correct approach: first draw the DAG, analyze the topology, then choose the simplest architecture that matches the topology.

### Interface Design Over Task Titles

The correct granularity of design is not task titles ("data cleaning," "feature engineering," "model training") — it is the interfaces between tasks, i.e., data contracts and handoff artifacts. The interface between two agents defines their degree of coupling. If the interface is a clear, small, verifiable data structure (e.g., a JSON schema), the two agents can work relatively independently. If the interface is vague, large, or requires frequent negotiation, coupling is high and multi-agent benefits are small.

In the "4+4+1" multi-agent real estate research experiment on 2026-02-16, this point was clearly demonstrated. Four comprehensive agents each covered the full document set but had 50% responsibility overlap; this overlap zone was the interface. It was precisely at this interface that the fifth cross-verification agent discovered inconsistencies (e.g., contradictions in garage conversion feasibility, differing interpretations of the 750 sq ft threshold). These inconsistencies were not bugs — they were real contradictions in the information, only exposed through well-designed interfaces and verification mechanisms.

### When Topology Changes, Architecture Must Change Too

Architectural decisions can be tested and iterated. If you change the topology (e.g., by re-decomposing tasks to reduce coupling or shorten the critical path), the optimal architecture will also change. This means architecture is not a one-time decision — it is tightly coupled with task design. During the planning phase, you should simultaneously consider "what is the optimal architecture for this topology" and "can I simplify the architecture by changing the topology." Sometimes, spending time redesigning task boundaries to reduce coupling is more cost-effective than directly increasing the number of agents.

## 3. Application Criteria

**When to use**:
- Choosing between single-agent vs. orchestrator-worker vs. hierarchical approaches
- Planning multi-agent research, analysis, or delivery tasks
- Evaluating optimal granularity when decomposing large deliverables
- When system performance falls short, diagnosing whether it is a topology problem rather than an agent capability problem

**How to practice**:
1. First draw a DAG, listing all tasks and their dependency relationships
2. Estimate maximum parallelizability (number of tasks executable simultaneously) and critical path length (longest dependency chain)
3. Analyze coupling: which tasks' outputs affect multiple downstream tasks? How strong are these effects?
4. Cluster nodes by shared state and data flow, identifying natural agent boundaries
5. Choose the simplest architecture matching the topology (prefer single-agent, then Orchestrator-Worker, and only then Hierarchical)
6. Define clear interfaces (data contracts, handoff artifact formats, verification criteria)
7. Re-measure topology during execution; if critical path or coupling changes, re-evaluate architecture

**Pitfalls**:
- Being dazzled by task count and ignoring topology
- Artificially creating dependencies just to use multi-agent
- Designing vague interfaces, leading to frequent negotiation and synchronization among agents
- Ignoring the critical path and wasting optimization effort on non-bottleneck tasks (see X3 Efficiency Is Determined by the Bottleneck)

## 4. Related Axioms

- **T03 Context Isolation Is the Value of Multi-Agent**: The granularity of isolation should be determined by information dependency relationships in the topology
- **T02 Results Certainty Over Process Certainty**: Verify interface outputs, rather than enforcing a specific task decomposition method
- **X3 Efficiency Is Determined by the Bottleneck**: The critical path is the system's bottleneck; optimization elsewhere is irrelevant
- **T05 Cognition Is an Asset, Code Is a Commodity**: Understanding topology is more valuable than listing tasks

# Test strategy

- Unit: chunking, citation formatting, deterministic retriever, abstention.
- Functional: FastAPI contract using local deterministic backend.
- Integration: real Vector Search / UC permissions / model endpoint in staging.
- GenAI evaluation: retrieval correctness, context recall, citation correctness,
  answer correctness, abstention, safety, latency and cost.
- Production monitoring: sampled traces + quality scorers + SLI/SLO.

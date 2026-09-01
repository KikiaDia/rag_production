import asyncio, json, statistics, time
from pathlib import Path
from energy_rag.config import Settings
from energy_rag.factory import build_service
from evaluation.scorers import score_case


async def main() -> int:
    settings = Settings(backend="fake", min_relevance_score=0.2)
    service = build_service(settings)
    cases = json.loads(Path("evaluation/golden_dataset.json").read_text())
    scores, latencies = [], []
    for case in cases:
        started = time.perf_counter()
        result = await service.answer(case["question"])
        latencies.append((time.perf_counter() - started) * 1000)
        scores.append(score_case(case, result))
    metrics = {
        "context_recall": sum(s.retrieval_correct for s in scores) / len(scores),
        "citation_correctness": sum(s.citation_correct for s in scores) / len(scores),
        "answer_correctness": sum(s.answer_correct for s in scores) / len(scores),
        "abstention_accuracy": sum(s.abstention_correct for s in scores) / len(scores),
        "p95_latency_ms": max(latencies),
    }
    Path("evaluation/results").mkdir(parents=True, exist_ok=True)
    Path("evaluation/results/offline_eval.json").write_text(json.dumps(metrics, indent=2))
    failed = (
        metrics["context_recall"] < settings.min_context_recall
        or metrics["citation_correctness"] < settings.min_citation_correctness
        or metrics["answer_correctness"] < settings.min_answer_correctness
    )
    print(json.dumps(metrics, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

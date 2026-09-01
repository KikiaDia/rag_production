from dataclasses import dataclass


@dataclass(frozen=True)
class Score:
    retrieval_correct: bool
    citation_correct: bool
    answer_correct: bool
    abstention_correct: bool


def score_case(case: dict, result) -> Score:
    expected_docs = set(case["expected_document_ids"])
    retrieved_docs = {c.split(",")[0].strip("[") for c in result.citations}
    retrieval_correct = expected_docs.issubset(retrieved_docs) if expected_docs else result.abstained
    citation_correct = all(c.startswith("[") and c.endswith("]") for c in result.citations)
    answer_correct = all(t.lower() in result.answer.lower() for t in case["expected_terms"])
    abstention_correct = bool(result.abstained) == bool(case["should_abstain"])
    return Score(retrieval_correct, citation_correct, answer_correct, abstention_correct)

import json, os
from pathlib import Path
import mlflow

rows=json.loads(Path("evaluation/golden_dataset.json").read_text())
dataset=mlflow.genai.datasets.get_dataset(os.environ["EVAL_DATASET_NAME"])
dataset.merge_records([
    {
      "inputs":{"question":r["question"]},
      "expectations":{
        "expected_document_ids":r["expected_document_ids"],
        "expected_terms":r["expected_terms"],
        "should_abstain":r["should_abstain"]
      },
      "tags":{"case_id":r["id"],"git_sha":os.getenv("CI_COMMIT_SHA","local")}
    } for r in rows
])
print(f"Synced {len(rows)} rows")

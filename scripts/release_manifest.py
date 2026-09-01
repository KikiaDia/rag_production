import hashlib, json, os, platform
from pathlib import Path

def sha(path):
    p=Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None

manifest={
 "release":{"id":os.getenv("RELEASE_ID"),"git_sha":os.getenv("CI_COMMIT_SHA"),"git_tag":os.getenv("CI_COMMIT_TAG"),"artifact_digest":os.getenv("ARTIFACT_DIGEST")},
 "runtime":{"python":platform.python_version(),"dependency_lock_sha256":sha("requirements.lock")},
 "environment":{"name":os.getenv("ENVIRONMENT"),"bundle_target":os.getenv("BUNDLE_TARGET")},
 "prompt":{"name":os.getenv("PROMPT_NAME"),"ref":os.getenv("PROMPT_REF"),"resolved_version":os.getenv("PROMPT_RESOLVED_VERSION")},
 "model":{"endpoint":os.getenv("MODEL_ENDPOINT"),"type":os.getenv("MODEL_TYPE"),"temperature":os.getenv("MODEL_TEMPERATURE"),"max_tokens":os.getenv("MODEL_MAX_TOKENS")},
 "retrieval":{"vector_endpoint":os.getenv("VECTOR_SEARCH_ENDPOINT"),"index":os.getenv("VECTOR_INDEX_NAME"),"source_table":os.getenv("SOURCE_TABLE"),"corpus_snapshot":os.getenv("CORPUS_SNAPSHOT"),"embedding_model":os.getenv("EMBEDDING_MODEL"),"top_k":os.getenv("TOP_K"),"min_score":os.getenv("MIN_RELEVANCE_SCORE")},
 "evaluation":{"dataset":os.getenv("EVAL_DATASET_NAME"),"dataset_version":os.getenv("EVAL_DATASET_VERSION"),"run_id":os.getenv("EVALUATION_RUN_ID"),"golden_sha256":sha("evaluation/golden_dataset.json"),"report_sha256":sha("evaluation/results/offline_eval.json")},
 "deployment":{"databricks_yml_sha256":sha("databricks.yml")}
}
Path("release-manifest.json").write_text(json.dumps(manifest, indent=2))
print(json.dumps(manifest, indent=2))

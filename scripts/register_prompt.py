import os, mlflow
template = open(os.getenv("PROMPT_TEMPLATE_FILE", "prompts/rag_answer.txt"), encoding="utf-8").read()
p = mlflow.genai.register_prompt(
    name=os.environ["PROMPT_NAME"],
    template=template,
    commit_message=os.getenv("PROMPT_COMMIT_MESSAGE", "RAG prompt from CI"),
    tags={"git_sha": os.getenv("CI_COMMIT_SHA", "local"), "use_case":"energy_rag"},
)
mlflow.genai.set_prompt_model_config(
    name=p.name, version=p.version,
    model_config={
        "model_name": os.environ["MODEL_ENDPOINT"],
        "model_type": os.getenv("MODEL_TYPE","chat"),
        "temperature": float(os.getenv("MODEL_TEMPERATURE","0")),
        "max_tokens": int(os.getenv("MODEL_MAX_TOKENS","1000")),
    }
)
print(f"{p.name} version={p.version}")

from dataclasses import dataclass
from energy_rag.config import Settings


@dataclass(frozen=True)
class ResolvedPrompt:
    name: str
    version: int
    template: str
    model_config: dict[str, object]


def prompt_uri(name: str, ref: str) -> str:
    return f"prompts:/{name}/{ref}" if ref.isdigit() else f"prompts:/{name}@{ref}"


def load_runtime_prompt(settings: Settings) -> ResolvedPrompt:
    try:
        import mlflow
    except ImportError as exc:
        raise RuntimeError('Install MLflow: pip install -e ".[databricks]"') from exc

    prompt = mlflow.genai.load_prompt(prompt_uri(settings.prompt_name, settings.prompt_ref))
    cfg = dict(getattr(prompt, "model_config", None) or {})
    model_config = {
        "model_name": cfg.get("model_name", settings.model_endpoint),
        "model_type": cfg.get("model_type", settings.model_type),
        "temperature": cfg.get("temperature", settings.model_temperature),
        "max_tokens": cfg.get("max_tokens", settings.model_max_tokens),
    }
    return ResolvedPrompt(str(prompt.name), int(prompt.version), str(prompt.template), model_config)

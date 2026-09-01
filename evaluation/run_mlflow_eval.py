"""Databricks-native evaluation entry point.

Load the governed MLflow Evaluation Dataset and run mlflow.genai.evaluate with
retrieval/citation/correctness/safety scorers appropriate to the workspace.
Keep this separate from deterministic CI tests because judges and endpoints incur cost.
"""
import os
import mlflow


def main():
    mlflow.set_experiment(os.environ["MLFLOW_EXPERIMENT_NAME"])
    dataset = mlflow.genai.datasets.get_dataset(os.environ["EVAL_DATASET_NAME"])
    print(f"Evaluation dataset ready: {dataset}")
    # Add workspace-approved scorers and predict_fn here.
    # mlflow.genai.evaluate(data=dataset, predict_fn=..., scorers=[...])


if __name__ == "__main__":
    main()

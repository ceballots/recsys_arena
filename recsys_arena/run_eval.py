import os
import pandas as pd
from recsys_arena.evaluator.evaluator import evaluate_pairwise
from recsys_arena.evaluator.metrics import win_rate
from recsys_arena.utils.logging import get_logger
from recsys_arena.prompt_engine.loader import load_prompt_config, load_template
from recsys_arena.prompt_engine.prompt_spec import PromptSpec
from recsys_arena.evaluator.evaluator import RemoteEvaluator


logger = get_logger(__name__)

CONFIG_FILE = os.getenv("CONFIG_FILE", "configs/pairwise.yaml")
TEMPLATE_PATH = os.getenv("TEMPLATE_PATH", "")
LABEL_A = "System A"
LABEL_B = "System B"


def run_eval(input_file: str, output_file: str, model: str = "gpt-3.5-turbo"):
    df = pd.read_csv(input_file)

    prompt_cfg = load_prompt_config(CONFIG_FILE)

    template_file = prompt_cfg.get("template_file")
    if not template_file:
        raise ValueError("Template file path not found in the config.")

    template_path = os.path.join(TEMPLATE_PATH, template_file)

    tmpl = load_template(template_path)
    pairwise_prompt = PromptSpec(prompt_cfg["name"], tmpl, prompt_cfg["schema"])

    evaluator = RemoteEvaluator(model=model)

    results = []
    for _, row in df.iterrows():
        winner, explanation = evaluate_pairwise(
            row["source"], row["recs_a"], row["recs_b"], evaluator, pairwise_prompt, label_a=LABEL_A, label_b=LABEL_B
        )
        results.append(
            {
                "task_id": row["task_id"],
                "source": row["source"],
                "recs_a": row["recs_a"],
                "recs_b": row["recs_b"],
                "winner": winner,
                "explanation": explanation,
            }
        )

    result_df = pd.DataFrame(results)
    result_df.to_csv(output_file, index=False)

    win_a = win_rate(result_df, LABEL_A)
    logger.info(f"Win rate of {LABEL_A}: {win_a:.2%}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Pairwise recommendation evaluator")
    parser.add_argument(
        "--input-file",
        type=str,
        required=True,
        help="Path to the input CSV file (e.g. tasks.csv)",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Path to save the output results (e.g. output.csv)",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=False,
        default="gpt-3.5-turbo",
        help="Model to use for evaluation (e.g. gpt-4, gpt-3.5-turbo)",
    )

    args = parser.parse_args()

    run_eval(args.input_file, args.output_file, args.model)
import os
import pandas as pd
from recsys_arena.evaluator.evaluator import evaluate_pairwise
from recsys_arena.evaluator.metrics import win_rate
from recsys_arena.utils.logging import get_logger
from prompt_engine.loader import load_prompt_config, load_template
from prompt_engine.prompt_spec import PromptSpec
from recsys_arena.evaluator.evaluator import RemoteEvaluator


from pathlib import Path

logger = get_logger(__name__)

CONFIG_FILE = os.getenv("CONFIG_FILE", "../configs/pairwise.yaml")

# TODO: add offset
# TODO: async
# TODO: retries on specific errors
# TODO: stop the flow when specific errors (eg, no credits left)


def run_eval(input_file: str, output_file: str):
    df = pd.read_csv(input_file)

    prompt_cfg = load_prompt_config(CONFIG_FILE)

    template_file = prompt_cfg.get("template_file")
    if not template_file:
        raise ValueError("Template file path not found in the config.")

    config_directory = Path(input_file).parent
    template_path = config_directory / template_file

    tmpl = load_template(template_path)
    pairwise_prompt = PromptSpec(prompt_cfg["name"], tmpl, prompt_cfg["schema"])

    evaluator = RemoteEvaluator()

    results = []
    for _, row in df.iterrows():
        winner, explanation = evaluate_pairwise(
            row["source"], row["recs_a"], row["recs_b"], evaluator, pairwise_prompt
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

    win_a = win_rate(result_df, "System A")
    logger.info(f"Win rate of system A: {win_a:.2%}")


if __name__ == "__main__":
    run_eval("../sample_data/tasks.csv", "../output.csv")

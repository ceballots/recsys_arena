import litellm
from recsys_arena.utils.logging import get_logger
from abc import ABC, abstractmethod
from typing import Optional, Tuple
from recsys_arena.prompt_engine.prompt_spec import PromptSpec

logger = get_logger(__name__)


class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, prompt: str):
        pass


class RemoteEvaluator(Evaluator):
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model

    def evaluate(self, prompt):
        try:
            response = litellm.completion(
                model=self.model, messages=[{"role": "user", "content": prompt}]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.error(f"Unexpected error during LLM API call: {e}")
            raise e


def evaluate_pairwise(
    source: str,
    recs_a: str,
    recs_b: str,
    evaluator: Evaluator,
    prompt_spec: PromptSpec,
    label_a: Optional[str] = "System A",
    label_b: Optional[str] = "System B",
    label_unclear: Optional[str] = "Unclear",
) -> Tuple[str, str]:
    prompt = prompt_spec.render(
        context=source,
        recs_a=recs_a,
        recs_b=recs_b,
        label_a=label_a,
        label_b=label_b,
        label_unclear=label_unclear,
    )

    try:
        response = evaluator.evaluate(prompt)
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return "Failure", f"LLM call exception: {e}"

    try:
        parsed = prompt_spec.parse(response)
        return parsed.get("winner", "Error"), parsed.get("explanation", "")
    except Exception as e:
        logger.error(f"Parsing failed. Response: {response} | Error: {e}")
        return "Failure", f"Parse exception: {e}. Raw response: {response}"

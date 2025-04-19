from pathlib import Path
import yaml


def load_prompt_config(config_path: str | Path):
    config_path = Path(config_path).expanduser().resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Prompt config not found: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_template(template_path: str | Path):
    template_path = Path(template_path).expanduser().resolve()
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    with open(template_path, "r") as f:
        return f.read()

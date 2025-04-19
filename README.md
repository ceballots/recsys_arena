# recsys_arena
Basic implementation of Recsys Arena [Wu et al., 2024](https://arxiv.org/abs/2412.11068) — *RecSys Arena: Pair-wise Recommender System Evaluation with Large Language Models*

## Features

- Pairwise comparison of recommendations from two systems
- Uses configurable prompt templates and schemas
- Evaluates using a remote LLM backend
- Outputs results with winner and explanation

## 🛠️ Setup

### Requirements

- Python 3.8+
- [`uv`](https://github.com/astral-sh/uv) (for dependency management)

Install `uv` if you haven’t already:

```bash
pip install uv
```

Install project:

```bash
uv pip install -r pyproject.toml
```

## ⚙️ Configuration
You can override default paths using environment variables:

CONFIG_FILE: Path to the prompt configuration file
Default: ../configs/pairwise.yaml

TEMPLATE_PATH: Directory containing the prompt templates
Default: ../

## 📄 Input Format
Input CSV must contain:

- task_id: Unique identifier for the evaluation task
- source: Source context (eg, item or user description)
- recs_a: Recommendations from System A
- recs_b: Recommendations from System B

Sample row:

```csv
task_id,source,recs_a,recs_b
1,"user profile text","rec1A, rec2A","rec1B, rec2B"
```

## 🚀 Run the Evaluator
This project uses [LiteLLM](https://github.com/BerriAI/litellm) as the backend to call remote models like OpenAI, Anthropic, Mistral, and others.
Before running the evaluator, make sure you export your model provider's API key or credentials.

🔐 Set Environment Variables
For example, if you're using OpenAI:

```bash
export OPENAI_API_KEY=your_openai_key_here
```
Or for Anthropic:

```bash
export ANTHROPIC_API_KEY=your_anthropic_key_here
```

To run the evaluator directly from Python, you can call the run_eval function in your code like this:

```python
from recsys_arena.main import run_eval

run_eval("path/to/input.csv", "path/to/output.csv")
```

Alternatively, you can run it directly from the command line:

```bash
python -m recsys_arena.run_eval --input-file sample_data/tasks.csv --output-file output.csv
```

## ✅ TODO
- Add support for evaluation offset (pagination)
- Implement asynchronous evaluation
- Retry logic for transient evaluator errors
- Graceful stop on critical failures (e.g., no API credits)

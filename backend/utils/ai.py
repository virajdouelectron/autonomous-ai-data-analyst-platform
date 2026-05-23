import os
import requests

# AI utility scaffold for interacting with the Gemini API and processing model outputs.
# This module should include request construction, response parsing, and prompt management.

GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://api.gemini.example/v1/generate")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def build_insight_prompt(statistics: dict) -> str:
    """Convert dataframe statistics into a Gemini prompt for business insights."""
    facts = [f"{key}: {value}" for key, value in statistics.items()]
    fact_block = "\n".join(facts)

    return (
        "You are a business insights analyst. "
        "Given the following dataset statistics, summarize the most important trends, risks, and opportunities for a business user:\n\n"
        f"{fact_block}\n\n"
        "Provide concise, actionable insight statements and highlight any anomalies or values that require attention."
    )


def build_pandas_query_prompt(question: str, schema: dict) -> str:
    """Build a Gemini prompt that asks for valid pandas code using the provided schema."""
    if isinstance(schema, dict):
        schema_lines = [f"{column}: {dtype}" for column, dtype in schema.items()]
    else:
        schema_lines = [str(schema)]

    schema_block = "\n".join(schema_lines)

    return (
        "You are a helpful Python data analyst. Given a pandas DataFrame named `df` and the column schema below, "
        "generate only valid pandas code that answers the user's natural language question.\n\n"
        f"Column schema:\n{schema_block}\n\n"
        f"User question:\n{question}\n\n"
        "Requirements:\n"
        "- Use `df` as the DataFrame variable.\n"
        "- Return only executable pandas code, without markdown, backticks, explanation, or commentary.\n"
        "- Do not include imports.\n"
        "- If the answer is a scalar or series, assign it to `result` or use `df` operations.\n"
        "- Use standard pandas methods and expressions.\n\n"
        "Provide only the final Python code."
    )


def extract_code_from_gemini_response(text: str) -> str:
    """Extract code from Gemini model output and strip formatting wrappers."""
    import re

    if not text:
        return ""

    code = text.strip()
    match = re.search(r"```(?:python)?\s*(.*?)```", code, re.S)
    if match:
        code = match.group(1).strip()

    if code.startswith("python\n"):
        code = code[len("python\n") :].strip()

    return code


def call_gemini_api(prompt: str) -> str:
    """Send a prompt to the Gemini API and return the generated insights."""
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 512,
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    # The exact response format may vary depending on Gemini API version.
    return data.get("text") or data.get("insights") or str(data)


def generate_insight_from_stats(statistics: dict, system_prompt: str | None = None) -> str:
    """Wrapper that accepts a stats dict and an optional system prompt, calls Gemini, and returns text.

    - `statistics`: dictionary of statistics (e.g., output from `compute_missing_value_analysis`)
    - `system_prompt`: optional high-level instruction to prepend/override default system guidance

    Returns the raw text produced by the Gemini API.
    """
    # Build the fact block prompt from statistics
    facts = []
    # If statistics was a nested dict (per-column), flatten a bit for the prompt
    if isinstance(statistics, dict):
        for key, val in statistics.items():
            # If column-level dict, produce a concise line
            if isinstance(val, dict):
                summary_items = []
                for subk in ("missing_count", "missing_pct", "dtype", "min", "max", "mean"):
                    if subk in val:
                        summary_items.append(f"{subk}={val[subk]}")
                facts.append(f"{key}: {', '.join(summary_items)}")
            else:
                facts.append(f"{key}: {val}")
    else:
        facts.append(str(statistics))

    fact_block = "\n".join(facts)

    # Compose the final prompt: use provided system_prompt if present, else default
    if system_prompt and isinstance(system_prompt, str) and system_prompt.strip():
        prompt = f"{system_prompt}\n\nDataset statistics:\n{fact_block}\n\nPlease provide concise, actionable business insights." 
    else:
        prompt = build_insight_prompt({"stats": fact_block})

    return call_gemini_api(prompt)

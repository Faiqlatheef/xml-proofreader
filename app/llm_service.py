import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL_NAME = "meta-llama/llama-3.1-8b-instruct"


def build_prompt(text, style_guide, lang):
    return f"""
You are a strict proofreading system.

Your task:
Find ONLY incorrect words or short phrases.

STRICT RULES:
- DO NOT return full sentences
- ONLY return 1–5 word segments
- "original" must EXACTLY match text
- DO NOT return items where original == correction
- DO NOT return correct words
- ONLY return real mistakes
- Prefer small, precise corrections

STYLE GUIDE:
{style_guide}

RETURN STRICT JSON:
[
  {{
    "original": "exact wrong text",
    "correction": "correct text",
    "type": "spelling | grammar | punctuation | capitalization | clarity | styleguide",
    "reason": "short explanation"
  }}
]

TEXT:
{text}

ONLY RETURN JSON. NO EXTRA TEXT.
"""


def call_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "XML Proofreader"
        }
    )
    return response.choices[0].message.content


def safe_json_parse(output):
    try:
        return json.loads(output)
    except:
        try:
            start = output.index("[")
            end = output.rindex("]") + 1
            return json.loads(output[start:end])
        except:
            return []


def proofread_text(text, lang, style_guide_text):
    prompt = build_prompt(text, style_guide_text, lang)

    for attempt in range(2):
        try:
            raw_output = call_llm(prompt)

            print("\n--- LLM OUTPUT ---")
            print(raw_output)
            print("------------------\n")

            parsed = safe_json_parse(raw_output)

            if isinstance(parsed, list):

                parsed = clean_llm_output(parsed)

                parsed = parsed[:10]

                return parsed

        except Exception as e:
            print(f"LLM ERROR (attempt {attempt+1}):", e)

    return []

def clean_llm_output(errors):
    seen = set()
    cleaned = []

    for err in errors:
        original = err.get("original", "").strip()
        correction = err.get("correction", "").strip()

        # ❌ Skip empty
        if not original or not correction:
            continue

        # ❌ Skip same
        if original.lower() == correction.lower():
            continue

        # ❌ Skip long phrases (avoid sentence rewriting)
        if len(original.split()) > 5:
            continue

        # ❌ Skip punctuation-only fixes
        if correction.strip() in [original + ".", original + ","]:
            continue

        # ❌ Skip aggressive rewrites (meaning change)
        if len(correction) > len(original) * 1.5:
            continue

        # ❌ Skip abbreviation replacements (IP, AI, etc.)
        if correction.isupper() and len(correction) <= 5:
            continue

        # ❌ Skip if removing too much content
        if len(correction) < len(original) * 0.5:
            continue

        # Deduplicate
        key = (original.lower(), correction.lower())
        if key in seen:
            continue
        seen.add(key)

        cleaned.append(err)

    return cleaned
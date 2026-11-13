import os
import requests

def generate_report(original_text, analysis):
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    if not api_key:
        raise RuntimeError("GenAI API key is missing. Add OPENROUTER_API_KEY to your .env file.")

    prompt = f"""
You are Rant2Report, a professional complaint report writer.
Your task is to understand the user's complaint and CREATE A NEW REPORT FROM SCRATCH.
Do not merely correct grammar, paraphrase sentence-by-sentence, or copy the original wording.
Use the NLP analysis as structured context. Preserve only facts supported by the original complaint.
Never invent names, dates, locations, evidence, conversations, losses, or events.
If a detail is unknown, omit it rather than guessing.
Use neutral, respectful, formal language. Do not exaggerate or make legal conclusions.

Original complaint:
{original_text}

NLP analysis:
{analysis}

Return ONLY valid JSON with these keys:
{{
  "title": "concise professional subject",
  "category": "category",
  "priority": "priority",
  "summary": "one or two sentence overview written newly",
  "description": "a newly composed formal complaint in a coherent paragraph",
  "requested_action": "clear and reasonable action requested",
  "missing_information": ["optional details the user may add"]
}}
The report must be substantially newly composed, not a lightly edited copy.
"""
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Rant2Report"
        },
        json={
            "model": model,
            "temperature": 0.5,
            "messages": [
                {"role": "system", "content": "You generate fact-grounded professional complaint reports. Return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        },
        timeout=60
    )
    if response.status_code != 200:
        raise RuntimeError(f"GenAI request failed ({response.status_code}): {response.text[:500]}")
    payload = response.json()
    content = payload["choices"][0]["message"]["content"]
    import json
    try:
        report = json.loads(content)
    except json.JSONDecodeError:
        raise RuntimeError("The AI returned an invalid report format. Please try again.")
    required = ["title", "category", "priority", "summary", "description", "requested_action"]
    if not all(report.get(k) for k in required):
        raise RuntimeError("The AI response was incomplete. Please try again.")
    # Keep model output aligned with the deterministic NLP analysis.
    report["category"] = analysis["category"]
    report["priority"] = analysis["priority"]
    report["missing_information"] = report.get("missing_information", [])
    return report

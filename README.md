# Rant2Report
AI-Powered Complaint Understanding and Report Generation System.

## What it does
1. Accepts informal complaint text.
2. Uses NLP preprocessing and TF-IDF + Logistic Regression to classify the complaint.
3. Extracts simple structured details such as duration and date, and estimates priority/impact.
4. Sends the original complaint plus structured NLP analysis to a Generative AI model.
5. Generates a newly composed, professional report.
6. Recommends relevant reporting destinations.

The classifier uses a small starter dataset in `nlp_processor.py`. It is a working educational baseline, not a production-grade model. Add more labelled examples and evaluate it on a separate test set before claiming high accuracy.

## Requirements
- Python 3.10 or newer
- An OpenRouter API key and an enabled model

## Setup (Windows)
Open Command Prompt in this project folder:

```bash
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and replace the placeholder with your OpenRouter API key. Keep this file private. Never put the key in `script.js`, HTML, or any public repository.

The default model is set in `.env` as `openai/gpt-4o-mini`. You can change it to another model available to your OpenRouter account.

Run:

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## How NLP and GenAI are used
- NLP: TF-IDF vectorization, Logistic Regression text classification, rule-assisted information extraction, urgency estimation and impact detection.
- Generative AI: receives the original complaint and structured NLP results, then creates a new title, summary, formal description and requested action. The prompt instructs the model not to copy the input sentence-by-sentence or invent unsupported facts.

## Important
- This is an educational prototype. The starter classifier is trained on a small hand-labelled dataset and may misclassify unusual complaints.
- Priority is a heuristic estimate, not a safety or legal assessment.
- Destination suggestions are informational. Check the official portal and eligibility before submitting.
- The app does not submit complaints automatically.
- The complaint text is sent to the configured AI provider. Do not enter sensitive personal information unless you understand the provider's data handling terms.

# backend/app/services/summarizer.py

"""
AI Summarization using Groq LLM.

Responsibilities:
- Generate short factual summaries (2–3 lines)
- Generate optional LinkedIn-style captions
- Deterministic, cheap, fast prompts
- NO OpenAI usage (Groq only)
"""

import os
from typing import Optional

from groq import Groq

# --------------------------------------------------
# Groq Client Initialization
# --------------------------------------------------

def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Please define it in .env or environment variables."
        )
    return Groq(api_key=api_key)

# Fast + cheap Groq model
DEFAULT_MODEL = "llama-3.1-8b-instant"


# --------------------------------------------------
# Prompt Templates
# --------------------------------------------------

SUMMARY_SYSTEM_PROMPT = (
    "You are a precise AI assistant that summarizes AI-related news. "
    "Be factual, concise, and neutral. No hype."
)

SUMMARY_USER_PROMPT = """
Summarize the following AI news in 2–3 concise sentences.
Focus on WHAT happened and WHY it matters.

News Content:
{content}
"""


LINKEDIN_SYSTEM_PROMPT = (
    "You are an assistant that writes professional LinkedIn captions "
    "about AI and technology news."
)

LINKEDIN_USER_PROMPT = """
Write a short LinkedIn post (2–3 lines) about the following AI news.
Tone: professional, informative, not promotional.

News Content:
{content}
"""


# --------------------------------------------------
# Core Summarization Functions
# --------------------------------------------------

def _call_groq(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    max_tokens: int = 150,
) -> str:
    """
    Low-level Groq API call wrapper.
    """
    client = get_groq_client()
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content.strip()


def generate_summary(content: str) -> str:
    """
    Generate a short factual summary (2–3 lines).
    """

    if not content:
        return ""

    prompt = SUMMARY_USER_PROMPT.format(content=content[:4000])

    return _call_groq(
        system_prompt=SUMMARY_SYSTEM_PROMPT,
        user_prompt=prompt,
        temperature=0.1,   # deterministic
        max_tokens=120,
    )


def generate_linkedin_caption(content: str) -> str:
    """
    Generate a LinkedIn-style caption for broadcasting.
    """

    if not content:
        return ""

    prompt = LINKEDIN_USER_PROMPT.format(content=content[:4000])

    return _call_groq(
        system_prompt=LINKEDIN_SYSTEM_PROMPT,
        user_prompt=prompt,
        temperature=0.3,
        max_tokens=120,
    )


# --------------------------------------------------
# Unified Helper (used by pipeline)
# --------------------------------------------------

def summarize_news_item(title: str, content: Optional[str]) -> dict:
    """
    Safe summarization:
    - Uses Groq if available
    - Falls back if rate-limited
    - NEVER breaks ingestion
    """

    base_text = f"{title}\n\n{content or ''}"

    try:
        summary = generate_summary(base_text)
        linkedin_caption = generate_linkedin_caption(base_text)
    except Exception as e:
        summary = (content or title)[:300]
        linkedin_caption = ""

    return {
        "summary": summary,
        "linkedin_caption": linkedin_caption,
    }

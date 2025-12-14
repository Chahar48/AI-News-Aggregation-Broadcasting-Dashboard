from datetime import datetime, timedelta

def get_seed_news():
    """
    Deterministic seed data for MVP demo.
    GUARANTEES dashboard functionality.
    """

    base_time = datetime.utcnow()

    return [
        {
            "source_name": "OpenAI Blog",
            "title": "OpenAI releases new reasoning model",
            "author": "OpenAI",
            "url": "https://openai.com/blog/reasoning-model",
            "published_at": base_time - timedelta(hours=2),
            "content": "OpenAI has released a new reasoning-focused model improving multi-step problem solving.",
        },
        {
            "source_name": "Google AI Blog",
            "title": "Google introduces Gemini updates",
            "author": "Google AI",
            "url": "https://blog.google/ai/gemini-update",
            "published_at": base_time - timedelta(hours=5),
            "content": "Google announced new Gemini updates improving multimodal understanding.",
        },
        {
            "source_name": "TechCrunch AI",
            "title": "AI startups raise record funding in 2024",
            "author": "TechCrunch",
            "url": "https://techcrunch.com/ai-funding-2024",
            "published_at": base_time - timedelta(days=1),
            "content": "AI startups saw record-breaking investments as demand for foundation models grows.",
        },
        {
            "source_name": "arXiv AI",
            "title": "New transformer architecture improves efficiency",
            "author": "arXiv",
            "url": "https://arxiv.org/abs/2401.12345",
            "published_at": base_time - timedelta(days=2),
            "content": "Researchers propose a transformer variant that reduces inference cost significantly.",
        },
        {
            "source_name": "YouTube AI Channels",
            "title": "Explaining GPT-4 reasoning capabilities",
            "author": "YouTube",
            "url": "https://youtube.com/watch?v=ai-demo",
            "published_at": base_time - timedelta(days=3),
            "content": "A breakdown of GPT-4 reasoning improvements and real-world use cases.",
        },
    ]

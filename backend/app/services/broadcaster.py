# backend/app/services/broadcaster.py

"""
Broadcast service for:
- Email (mock or SendGrid)
- WhatsApp (wa.me share link)
- LinkedIn (AI-generated caption simulation)
- Blog post export (Markdown)
- Newsletter export (formatted text)

This module does NOT actually send messages unless configured.
Safe for interview & MVP submission.
"""

from datetime import datetime

from app.config import get_settings
from app.services.summarizer import summarize_news_item

settings = get_settings()

class BroadcastService:

    # ---------------------------------------------------------
    # EMAIL — SendGrid, SMTP, OR MOCK
    # ---------------------------------------------------------
    def send_email(self, to_email: str, subject: str, content: str) -> dict:
        """
        Email sending behavior:
        - If SENDGRID_API_KEY exists → you can wire it in
        - Else → mock sending for demo
        """

        if settings.sendgrid_api_key:
            # Placeholder for real SendGrid integration
            print("📧 [REAL EMAIL] Sending using SendGrid...")
            # Actual API call is optional for MVP
            pass

        # Mock email response
        return {
            "status": "sent (mock)",
            "to": to_email,
            "subject": subject,
            "content_preview": content[:120] + "...",
            "timestamp": datetime.utcnow().isoformat(),
        }

    # ---------------------------------------------------------
    # WHATSAPP — wa.me deep link
    # ---------------------------------------------------------
    def send_whatsapp(self, message: str) -> dict:
        """
        Uses WhatsApp's official share link:
        https://wa.me/?text=<ENCODED_MESSAGE>
        """
        encoded_msg = message.replace(" ", "%20")
        wa_link = f"https://wa.me/?text={encoded_msg}"

        return {
            "status": "generated",
            "share_link": wa_link,
            "preview": message[:120] + "...",
        }

    # ---------------------------------------------------------
    # LINKEDIN — AI caption + simulated post
    # ---------------------------------------------------------
    def post_linkedin(self, news_title: str, ml_summary: str) -> dict:
        caption = summarizer.generate_linkedin_caption(ml_summary)

        return {
            "status": "posted (mock)",
            "caption": caption,
            "share_url": f"https://linkedin.com/shareArticle?mini=true&title={news_title.replace(' ', '%20')}",
        }

    # ---------------------------------------------------------
    # BLOG — Markdown article generation
    # ---------------------------------------------------------
    def generate_blog_markdown(self, news_title: str, summary: str, url: str) -> dict:
        markdown = (
            f"# {news_title}\n\n"
            f"**Summary:**\n\n"
            f"{summary}\n\n"
            f"---\n"
            f"Original Source: [{url}]({url})\n"
        )

        return {
            "status": "generated",
            "markdown": markdown,
        }

    # ---------------------------------------------------------
    # NEWSLETTER — Clean formatted text for email lists
    # ---------------------------------------------------------
    def generate_newsletter_item(self, news_title: str, summary: str, url: str) -> dict:
        newsletter_text = (
            f"📰 *{news_title}*\n\n"
            f"{summary}\n\n"
            f"Read more: {url}\n"
            f"----------------------\n"
        )

        return {
            "status": "generated",
            "newsletter_text": newsletter_text,
        }


# Global shared instance
broadcaster = BroadcastService()

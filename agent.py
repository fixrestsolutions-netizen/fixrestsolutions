import os
import json
import requests
from anthropic import Anthropic

# Initialize API Clients
anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
WA_TOKEN = os.environ.get("WHATSAPP_TOKEN")
WA_PHONE_ID = os.environ.get("WHATSAPP_PHONE_ID")

SYSTEM_PROMPT = """You are Craig van Niekerk, Operations Manager at Fixrest Marketing (fixrest.co.za) in South Africa.

COMPANY OVERVIEW:
Fixrest Marketing builds AI-powered WhatsApp automation, multilingual customer engagement, content strategy, local SEO, and IT services for South African SMEs (salons, restaurants, contractors, tutors, established businesses).

CORE SERVICES:
1. WhatsApp Automation (<5s response, 24/7, English, Zulu, Afrikaans, Xhosa).
2. Digital Marketing (Instagram captions, SEO blog posts, email newsletters, Google Business Profile).
3. Local SEO (Google Business Profile optimization, 24h review replies).
4. IT Services (System setup, network configuration, software support).
5. Lead Generation (Daily automated prospect outreach).
6. Reporting & Strategy (Monthly plain-English performance reports).

PACKAGE TIERS (ZAR):
- Starter: R800/month (+ R1,000 setup) -> 24/7 WhatsApp auto-reply, English, FAQs, quote responses.
- Professional: R1,800/month (+ R2,000 setup) -> 4 languages (English, Zulu, Afrikaans, Xhosa), Calendly/Booksy integration, Airtable logging, instant owner alerts.
- Full Service: R3,500/month (+ R3,500 setup) -> Professional + 20 IG captions, 2 SEO blogs (800 words), 1 newsletter, full Google Business Profile management.

OPERATIONAL RULES:
- Tone: Professional, approachable, direct, practical, and tailored to South African business owners.
- Return output strictly as raw JSON without markdown formatting blocks.
"""

def run_business_cycle():
    prompt = """Execute an operational update for Fixrest Marketing:
    1. Write a short promotional snippet signed by Craig van Niekerk highlighting one of our packages (Starter R800, Professional R1,800, or Full Service R3,500).
    2. Draft a cold WhatsApp outreach template for a prospective South African small business owner.
    3. Generate a 3-word visual prompt for marketing image generation.

    Return JSON in this format:
    {
        "headline": "Service or Package Headline",
        "promo_text": "Short promotional copy for the website",
        "wa_outreach": "WhatsApp cold outreach message",
        "image_prompt": "3 word English description of a professional tech/marketing image"
    }"""

    # Model routing: claude-3-5-haiku keeps operational costs at ~$0.001 per run
    response = anthropic.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    data = json.loads(response.content[0].text)
    image_url = f"https://pollinations.ai/p/{data['image_prompt'].replace(' ', '_')}?width=800&height=600"

    # Save state/content locally for auto-deployment
    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fixrest Marketing | AI Automation & Digital Presence</title>
    <style>
        body {{ font-family: system-ui, sans-serif; line-height: 1.6; padding: 40px; max-width: 800px; margin: auto; background: #f9f9fb; color: #222; }}
        .card {{ background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-top: 20px; }}
        .btn {{ display: inline-block; background: #25D366; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Fixrest Marketing</h1>
    <p><strong>Operations Manager:</strong> Craig van Niekerk</p>
    <div class="card">
        <h2>{data['headline']}</h2>
        <img src="{image_url}" alt="Fixrest Asset" style="width:100%; border-radius:6px;">
        <p>{data['promo_text']}</p>
        <a href="https://wa.me/27123456789" class="btn">Enquire on WhatsApp</a>
    </div>
</body>
</html>"""

    with open("index.html", "w") as f:
        f.write(page_html)

    print("Agent execution completed successfully.")

if __name__ == "__main__":
    run_business_cycle()

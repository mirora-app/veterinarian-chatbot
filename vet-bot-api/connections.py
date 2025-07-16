import os
from dotenv import load_dotenv

load_dotenv()

#USE_LOCAL = True  # Set False to use Groq
USE_LOCAL = False  # Set True to use Mistral LLM Locally

GROQ_API_KEY = None
GROQ_ENDPOINT = None
MODEL = None

if USE_LOCAL:
    GROQ_API_KEY = None
    GROQ_ENDPOINT = "http://192.168.1.202:8080/v1/completions"
    MODEL = "local"
if not USE_LOCAL:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "llama3-8b-8192"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def build_prompt(user_message, pricing_data):
    pricing_info = "\n".join(
        [
            f"{k.replace('_', ' ').title()}: ${v['price']} – {v['description']}"
            if 'price' in v else f"{k.replace('_', ' ').title()}: {v}"
            for k, v in pricing_data.items()
        ]
    )

    system_prompt = (
        "**Your Role**\n"
        "You are a veterinary informational assistant for Goodknight Mobile Vet.\n\n"
        "**Context**\n"
        "Only answer questions using the pricing and service information provided below. "
        "**Do not make up services, discounts, or policies. Do not guess.**\n"
        "**Do not recommend medical treatments or medications unless explicitly listed.**\n"
        "If a question is outside the scope of this information, respond with:\n"
        "\"I'm not sure, please contact our team directly.\"\n\n"
        "**If the user asks a question unrelated to veterinarian information, or Goodknight Mobile Vet, respond with:**\n"
        "\"I'm not sure I understand, please contact our team directly.\"\n\n"
        "In both of the above cases, simply end the message, do not continue.\n\n"
        f"**Additional Information:**\n"
        f"You may also answer general veterinary questions as long as the topic is common knowledge for licensed veterinarians (e.g., wellness, aging, behavioral tips). If uncertain, defer to contacting the clinic.\n\n"
        f"**Pricing and Service Information:**\n"
        f"{pricing_info}\n\n"
        f"**User Message:**\n"
        f"User: {user_message}\n\n"
        f"**Your Response:**\n"
        f"Respond in a succinct, professional, and non-repetitive tone.\n\n"
        f"A:"
    )
    return system_prompt

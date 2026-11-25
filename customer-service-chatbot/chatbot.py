"""
Customer Service Chatbot (rule-based NLP)
-----------------------------------------
A chatbot for a fictional online store, "ShopEasy".
Uses only Python's standard library - nothing to install.

How it works:
  1. Clean the user's message (lowercase, remove punctuation)
  2. Compare the words with keywords for each topic ("intent")
  3. Fuzzy matching (difflib) forgives small spelling mistakes
  4. The topic with the highest score gives the reply
  5. The bot remembers context, e.g. it asks for an order ID and
     understands your next message as that ID

Run:  python chatbot.py
"""

import random
import re
from difflib import get_close_matches

STORE = "ShopEasy"

# Sample orders so the bot can "look up" an order status
ORDERS = {
    "1001": "Delivered on 20 Nov.",
    "1002": "Shipped, arriving in 2 days.",
    "1003": "Being packed, ships tomorrow.",
    "1004": "Out for delivery today.",
}

# Each topic has keywords (single words or phrases) and possible replies
INTENTS = {
    "greeting": {
        "keywords": ["hi", "hello", "hey", "good morning", "good evening", "namaste"],
        "replies": [f"Hello! Welcome to {STORE}. How can I help you today?",
                    "Hi there! What can I do for you?"],
    },
    "goodbye": {
        "keywords": ["bye", "goodbye", "see you", "exit", "quit"],
        "replies": ["Goodbye! Thanks for shopping with us."],
    },
    "thanks": {
        "keywords": ["thanks", "thank you", "thx", "great", "awesome"],
        "replies": ["You're welcome! Anything else I can help with?"],
    },
    "order_status": {
        "keywords": ["track", "tracking", "status", "where is my", "order status", "track order", "delivery status"],
        "replies": [],  # handled in code (needs an order ID)
    },
    "shipping": {
        "keywords": ["shipping", "delivery time", "how long", "deliver", "shipping cost", "delivery charge"],
        "replies": ["Standard delivery takes 3-5 working days and is free above Rs.500. "
                    "Express delivery (1-2 days) costs Rs.99."],
    },
    "returns": {
        "keywords": ["return", "refund", "exchange", "money back", "replace", "damaged", "wrong item"],
        "replies": ["You can return any item within 7 days of delivery. "
                    "Go to My Orders > Return Item. Refunds reach you in 5-7 working days."],
    },
    "cancel": {
        "keywords": ["cancel", "cancel order", "cancellation"],
        "replies": ["Orders can be cancelled before they ship. Go to My Orders > Cancel. "
                    "If it has already shipped, please use the return option after delivery."],
    },
    "payment": {
        "keywords": ["payment", "pay", "upi", "card", "cash on delivery", "cod", "emi", "payment failed"],
        "replies": ["We accept UPI, credit/debit cards, net banking and cash on delivery. "
                    "If money was deducted but the order failed, it is refunded in 3-5 days."],
    },
    "offers": {
        "keywords": ["discount", "offer", "coupon", "promo", "sale", "deal"],
        "replies": ["Use code WELCOME10 for 10% off your first order! "
                    "Check the Offers page for ongoing sales."],
    },
    "account": {
        "keywords": ["password", "login", "log in", "account", "sign up", "register", "forgot password"],
        "replies": ["To reset your password, click 'Forgot Password' on the login page. "
                    "A reset link will be sent to your email."],
    },
    "hours": {
        "keywords": ["hours", "open", "timing", "working hours", "available"],
        "replies": ["Our support team is available Monday to Saturday, 9 AM to 6 PM. "
                    "This chatbot works 24/7."],
    },
    "human": {
        "keywords": ["human", "agent", "representative", "call", "phone", "contact", "support", "complaint"],
        "replies": ["You can reach our team at support@shopeasy.example or call 1800-123-456 "
                    "(Mon-Sat, 9 AM - 6 PM)."],
    },
}

FALLBACKS = [
    "Sorry, I didn't quite get that. I can help with orders, shipping, returns, "
    "payments, offers and accounts.",
    "I'm not sure about that. Could you rephrase? Try asking about your order, "
    "returns or payments.",
]


def clean(text):
    """Lowercase and remove punctuation."""
    return re.sub(r"[^a-z0-9\s]", " ", text.lower()).strip()


def score_intent(words, text, keywords):
    """Count how many of an intent's keywords appear in the message."""
    score = 0
    for kw in keywords:
        if " " in kw:                       # phrase: must appear as-is
            if kw in text:
                score += 2                  # phrases are stronger evidence
        elif kw in words:                   # exact word match
            score += 1
        elif len(kw) >= 5 and get_close_matches(kw, words, n=1, cutoff=0.8):
            score += 1                      # spelling mistake, e.g. "refnd"
    return score


def detect_intent(message):
    text = clean(message)
    words = text.split()
    best_intent, best_score = None, 0
    for name, data in INTENTS.items():
        s = score_intent(words, text, data["keywords"])
        if s > best_score:
            best_intent, best_score = name, s
    return best_intent


def find_order_id(message):
    """Look for a 4-digit order number such as 1002 or ORD1002."""
    match = re.search(r"\b(?:ord)?(\d{4})\b", message.lower())
    return match.group(1) if match else None


def order_reply(order_id):
    if order_id in ORDERS:
        return f"Order {order_id}: {ORDERS[order_id]}"
    return f"I couldn't find order {order_id}. Please check the number and try again."


def get_response(message, state):
    """Return the bot's reply. `state` remembers what the bot is waiting for."""
    order_id = find_order_id(message)

    # Context: the bot previously asked for an order ID
    if state.get("awaiting_order") and order_id:
        state["awaiting_order"] = False
        return order_reply(order_id)

    intent = detect_intent(message)

    if intent == "order_status" or (order_id and intent is None):
        if order_id:
            return order_reply(order_id)
        state["awaiting_order"] = True
        return "Sure! Please share your 4-digit order ID (try 1001 to 1004)."

    if intent == "goodbye":
        state["done"] = True

    if intent:
        state["awaiting_order"] = False
        return random.choice(INTENTS[intent]["replies"])

    return random.choice(FALLBACKS)


def main():
    print(f"=== {STORE} Customer Service Bot ===")
    print("Ask about orders, shipping, returns, payments, offers or your account.")
    print("Type 'bye' to exit.\n")
    state = {}
    while not state.get("done"):
        try:
            message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not message:
            continue
        print("Bot:", get_response(message, state), "\n")


if __name__ == "__main__":
    main()

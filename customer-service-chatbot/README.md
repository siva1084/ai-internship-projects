# Customer Service Chatbot

A rule-based NLP chatbot for a fictional online store ("ShopEasy") that answers common customer queries. Built with **pure Python - no external libraries required**.

## What it can do
- Track orders (asks for an order ID and remembers the context)
- Answer questions on shipping, returns/refunds, cancellations, payments, offers, account/password help and support hours
- Understand small spelling mistakes (e.g. "refnd" is read as "refund")
- Reply politely when it doesn't understand

## How it works
1. **Clean** the message - lowercase, remove punctuation
2. **Match** the words against keywords for each topic (intent)
3. **Fuzzy matching** (`difflib`) tolerates typing errors
4. **Score** every intent - phrases count more than single words - and pick the highest
5. **Context memory** - after asking for an order ID, the next message is treated as the ID
6. **Fallback** reply when no intent matches

## Run in VS Code
No installation needed - just Python 3.
```bash
python chatbot.py          # start chatting
python test_chatbot.py     # run automated tests (11 checks)
```

## Example
```
You: where is my order
Bot: Sure! Please share your 4-digit order ID (try 1001 to 1004).
You: 1002
Bot: Order 1002: Shipped, arriving in 2 days.
You: how do I get a refund
Bot: You can return any item within 7 days of delivery. ...
```

## Files
- `chatbot.py` - the chatbot
- `test_chatbot.py` - automated tests

## Tech
Python standard library only (`re`, `random`, `difflib`)

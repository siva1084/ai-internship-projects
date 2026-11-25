"""Quick automated checks. Run:  python test_chatbot.py"""
from chatbot import detect_intent, get_response

cases = [
    ("Hello there", "greeting"),
    ("How do I return a damaged item?", "returns"),
    ("I want a refnd", "returns"),                 # spelling mistake
    ("Is cash on delivery available?", "payment"),
    ("Any discount coupons?", "offers"),
    ("I forgot my password", "account"),
    ("how long does delivery take", "shipping"),
    ("Please cancel my order", "cancel"),
    ("bye", "goodbye"),
    ("what is the weather on mars", None),
]

passed = 0
for message, expected in cases:
    got = detect_intent(message)
    ok = got == expected
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] {message!r:42} -> {got}")

# Context test: bot asks for order ID, then understands the next message
state = {}
get_response("where is my order", state)
reply = get_response("1002", state)
ok = "Shipped" in reply
passed += ok
print(f"[{'PASS' if ok else 'FAIL'}] order-ID follow-up -> {reply}")

total = len(cases) + 1
print(f"\n{passed}/{total} tests passed")

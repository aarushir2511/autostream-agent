import json
from langchain.memory import ConversationBufferMemory

with open("knowledge_base.json", "r") as f:
    kb = json.load(f)

memory = ConversationBufferMemory(return_messages=True)

state = {
    "intent": None,
    "awaiting": None,
    "name": None,
    "email": None,
    "platform": None
}

def detect_intent(text):
    text = text.lower()

    if any(w in text for w in ["pro", "basic", "need", "want", "try", "subscribe"]):
        return "high_intent"

    if any(w in text for w in ["price", "pricing", "cost"]):
        return "pricing"

    if any(w in text for w in ["hi", "hello", "hey"]):
        return "greeting"

    return "other"


def answer_pricing():
    b = kb["pricing"]["Basic"]
    p = kb["pricing"]["Pro"]
    pol = kb["policies"]

    return f"""
**Pricing Plans**

**Basic**
- Price: {b['price']}
- {b['videos']}
- Resolution: {b['resolution']}

**Pro**
- Price: {p['price']}
- {p['videos']}
- Resolution: {p['resolution']}
- Features: {", ".join(p['features'])}

**Policies**
- Refund: {pol['refund']}
- Support: {pol['support']}
"""


def next_question():
    if state["name"] is None:
        state["awaiting"] = "name"
        return "Great choice! May I know your name?"

    if state["email"] is None:
        state["awaiting"] = "email"
        return "Thanks! What's your email address?"

    if state["platform"] is None:
        state["awaiting"] = "platform"
        return "Which platform do you create content on?"

    return None


def update_state(user_input):
    if state["awaiting"] == "name":
        state["name"] = user_input.title()
        state["awaiting"] = None

    elif state["awaiting"] == "email" and "@" in user_input:
        state["email"] = user_input
        state["awaiting"] = None

    elif state["awaiting"] == "platform":
        state["platform"] = user_input.title()
        state["awaiting"] = None


def process_user_input(user_input: str) -> str:
    intent = detect_intent(user_input)

    if intent == "high_intent":
        state["intent"] = "high_intent"

    update_state(user_input)

    if state["intent"] == "high_intent":
        q = next_question()
        if q:
            return q
        else:
            response = f"Thank you {state['name']}! Our team will reach out shortly."

            # Reset
            state.update({
                "intent": None,
                "awaiting": None,
                "name": None,
                "email": None,
                "platform": None
            })
            return response

    if intent == "pricing":
        return answer_pricing()

    if intent == "greeting":
        return "Hello! How can I help you today?"

    return "Could you tell me what you're looking for?"

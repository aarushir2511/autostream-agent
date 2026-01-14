import json
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

with open("knowledge_base.json", "r") as f:
    kb = json.load(f)

def mock_lead_capture(name, email, platform):
    print("\nLEAD CAPTURED")
    print(f"Name     : {name}")
    print(f"Email    : {email}")
    print(f"Platform : {platform}\n")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
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
We offer two pricing plans:

Basic Plan
- Price: {b['price']}
- {b['videos']}
- Resolution: {b['resolution']}

Pro Plan
- Price: {p['price']}
- {p['videos']}
- Resolution: {p['resolution']}
- Features: {", ".join(p['features'])}

Policies:
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
        return "Which platform do you create content on? (YouTube, Instagram, etc.)"

    return None

def update_state(user_input):
    text = user_input.strip()

    if state["awaiting"] == "name":
        state["name"] = text.title()
        state["awaiting"] = None

    elif state["awaiting"] == "email" and "@" in text:
        state["email"] = text
        state["awaiting"] = None

    elif state["awaiting"] == "platform":
        platform_map = {
            "yt": "YouTube",
            "youtube": "YouTube",
            "ig": "Instagram",
            "instagram": "Instagram",
            "tiktok": "TikTok"
        }
        key = text.lower()
        if key in platform_map:
            state["platform"] = platform_map[key]
            state["awaiting"] = None

print("AutoStream Agent running. Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Agent: Goodbye!")
        break

    intent = detect_intent(user_input)

    # Lock high intent
    if intent == "high_intent":
        state["intent"] = "high_intent"

    # Update state if we were waiting for input
    update_state(user_input)

    if state["intent"] == "high_intent":
        q = next_question()
        if q:
            response = q
        else:
            mock_lead_capture(
                state["name"],
                state["email"],
                state["platform"]
            )
            response = f"Thank you {state['name']}! Our team will reach out shortly."

            # Reset after capture
            state.update({
                "intent": None,
                "awaiting": None,
                "name": None,
                "email": None,
                "platform": None
            })

    elif intent == "pricing":
        response = answer_pricing()

    elif intent == "greeting":
        response = "Hello! How can I help you today?"

    else:
        response = "Could you tell me what you're looking for?"

    print(f"Agent: {response}")

    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(response)


def process_user_input(user_input):
    intent = detect_intent(user_input)

    if intent == "high_intent":
        state["intent"] = "high_intent"

    update_state(user_input)

    if state["intent"] == "high_intent":
        q = next_question()
        if q:
            response = q
        else:
            mock_lead_capture(
                state["name"],
                state["email"],
                state["platform"]
            )
            response = f"Thank you {state['name']}! Our team will reach out shortly."

            state.update({
                "intent": None,
                "awaiting": None,
                "name": None,
                "email": None,
                "platform": None
            })

    elif intent == "pricing":
        response = answer_pricing()

    elif intent == "greeting":
        response = "Hello! How can I help you today?"

    else:
        response = "Could you tell me what you're looking for?"

    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(response)

    return response
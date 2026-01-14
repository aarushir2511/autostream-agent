from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def detect_intent(user_input: str) -> str:
    prompt = f"""
Classify the user intent into ONE of the following:
- greeting
- product_inquiry
- high_intent

User message: "{user_input}"

Only output the label.
"""
    return llm.invoke(prompt).content.strip()

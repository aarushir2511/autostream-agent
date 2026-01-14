import json
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

with open("knowledge_base.json") as f:
    KB = json.load(f)


def retrieve_context() -> str:
    return f"""
Pricing:
Basic Plan: $29/month, 10 videos/month, 720p
Pro Plan: $79/month, Unlimited videos, 4K, AI captions

Policies:
No refunds after 7 days
24/7 support only on Pro plan
"""


def rag_answer(user_query: str) -> str:
    context = retrieve_context()

    prompt = f"""
You are an assistant for AutoStream.
Use ONLY the context below to answer.

Context:
{context}

Question: {user_query}
Answer:
"""
    return llm.invoke(prompt).content

# AutoStream Agent

AutoStream Agent is a conversational AI system designed to convert user conversations into qualified leads.  
It simulates a real-world **sales assistant workflow** by identifying user intent, answering product questions using a knowledge base, and capturing lead details only when the user shows high purchase intent.

This project demonstrates **agent reasoning, deterministic state handling, and lead qualification logic**, aligned with real SaaS sales automation systems.

---

## Features

- Intent classification (Greeting, Pricing Inquiry, High-Intent Lead)
- Knowledge-base grounded responses (no hallucinations)
- Multi-turn lead capture (Name → Email → Platform)
- State persistence across turns
- Deterministic control flow (no random behavior)
- Streamlit-based chat UI (no terminal interaction required)
- Easily extendable to WhatsApp / Web / APIs

---

## Intent Capabilities

The agent correctly identifies and handles:

### 1. Casual Greeting
**Example:** `hi`, `hello`, `good morning`  
→ Responds politely without pushing sales.

### 2. Product / Pricing Inquiry
**Example:** `price`, `pricing`, `cost`, `plans`  
→ Responds using a **local knowledge base**.

### 3. High-Intent Lead
**Example:** `pro plan`, `want to subscribe`, `need basic`  
→ Triggers structured lead capture workflow.

---

## Architecture Overview

The system follows a **deterministic agent architecture** with explicit state management.

### Core Components

### Intent Detection Layer
Rule-based intent classification ensures predictable behavior and eliminates ambiguity during evaluation.

### State Machine (Agent State)

The agent maintains structured state:

```python
{
  "intent": None,
  "awaiting": None,
  "name": None,
  "email": None,
  "platform": None
}
```
This guarantees:

- No repeated questions  
- No premature lead capture  
- Correct order of information collection  

---

### Knowledge Base (RAG-lite)

Pricing and policy information is loaded from a local JSON file (`knowledge_base.json`).  
Responses are grounded in factual data, preventing hallucinations.

---

### Lead Capture Tool

A mock lead capture function simulates backend CRM ingestion and can be easily replaced with real APIs.

---

### Conversation Memory

`ConversationBufferMemory` stores conversation history for future LLM-based enhancements.

---

## Streamlit Chat Interface

The agent runs entirely inside a **Streamlit web app**, providing a clean chat experience:

- User messages and agent replies appear in real-time  
- Session state ensures memory persistence  
- No terminal input required  
- Ready for demo and evaluation  

---

## How to Run

### 1. Set Environment Variable in Powershell

```bash
export OPENAI_API_KEY=your_openai_key
```
```bash
setx OPENAI_API_KEY "your_openai_key"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Streamlit App
```bash
streamlit run streamlit.py
```

#### Open your browser at:
```bash
http://localhost:8501
```


## Project Structure

autostream-agent

├── agent.py (Core agent logic (state, intent, lead capture))

├── streamlit.py (Streamlit UI wrapper)

├── knowledge_base.json (Pricing & policy data)

├── requirements.txt

└── README.md

├── rag.py

├── tools.py

└── intent.py

## WhatsApp Integration

AutoStream Agent can be integrated with the **WhatsApp Business Cloud API**.

### Flow

Incoming WhatsApp messages → Webhook  
→ Message routed to agent backend  
→ Conversation state stored using Redis / Database (keyed by phone number)  
→ Agent response sent back via WhatsApp Send Message API  

### This architecture enables:

- Multi-user concurrency
- Persistent conversations
- Scalable lead capture

---

## Evaluation Notes

- Deterministic logic (no prompt guessing)
- Clear intent separation
- Proper lead qualification flow
- No hallucinated pricing
- Production-aligned agent design

This mirrors real-world AI sales agents used in modern SaaS products.


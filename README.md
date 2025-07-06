
# Carton Caps Conversational AI (Capper)

    

## Overview

  

Capper delivers instant, grounded, and on-brand support to Carton Caps users. The assistant provides product recommendations, referral program guidance, and FAQ answers, all within Carton Caps-approved content boundaries.

  

-  **Personalized:** Greets users by name and school, and provides referral benefit info.

-  **Product-aware:** Surfaces recommendations from the actual product catalog.

-  **RAG-powered:** Uses retrieval-augmented generation for reliable answers.

-  **Plug-and-play:** Integrates easily with web/mobile apps.

-  **Privacy-first:** No PII ever leaves the Carton Caps infrastructure.

  

---

  

## Features

  

- Product recommendations, prices, and descriptions

- FAQ and referral rule grounding

- Multi-turn context (conversation memory)

- Personalized welcome with dynamic referral info

- Modular backend (easy to swap LLMs)

- Fast, modern Next.js frontend

  

---


## API Contract


| Route                    | Purpose                   | Request Example                                            | Response Example           |
|--------------------------|---------------------------|------------------------------------------------------------|----------------------------|
| `POST /chat`             | Send user message, get assistant reply.         | `{ "user_id": 1, "conversation_id": null, "message": "What can you help me with?" }`                        | `{ "conversation_id": "abc123-uuid", "reply": "I can help you with products, referrals, and FAQs.!" }`    |
| `GET /users`             | List user profiles for selector.        | –                                                          | `[{"id":1,"name":"Anna"},{ "id": 2, "name": "Bob Jones" }...]` |
| `GET /welcome/{user_id}` | Return welcome/referral intro for that user.  | –                                                          | `{ "messages": ["Hi {{user}}! I'm Capper, your personal Carton Caps assistant. Your purchases from us help to fund critical school programming efforts for {{school}}. Remember that a portion of your purchase goes to {{school}}!!"] }`  |
 `GET /health` | Liveness/health check.  | –                                                          | `{ "status": "ok" }`  |

---

## System Design Architecture


[System Design for Capper](https://excalidraw.com/#json=pVshaduh8uat7MxtBVWDE,Uv-TT42t_YDxBEWMw1p6gw)


## Quick Start

  

**Backend**

```
cd cc-backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
```
  

**Frontend**
```
cd cc-frontend

npm install

npm run dev
```

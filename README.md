
# Carton Caps Conversational AI (Capper)

    

## Overview

  

Capper delivers instant, grounded, and on-brand support to Carton Caps users. The assistant provides product recommendations, referral program guidance, and FAQ answers, all within Carton Caps-approved content boundaries.

  

-  **Personalized:** Greets users by name and school, and provides referral benefit info.

-  **Product-aware:** Surfaces recommendations from the actual product catalog.

-  **RAG-powered:** Uses retrieval-augmented generation for reliable answers.


---

  

## Features

  

- Product recommendations, prices, and descriptions

- FAQ and referral rule grounding

- Multi-turn context (conversation memory)

- Personalized welcome with dynamic referral info

- React + Tailwind for UI


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


![System Design Arch](https://github.com/yatharthgarg/cartoncaps-livefront/blob/main/livefront-frontend/public/System%20Design.excalidraw.png)


## Quick Start

**Backend**

```bash
cd livefront-backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend**
```bash
cd livefront-frontend
npm install
npm run dev
```
**Testing**
```bash
cd cartoncaps-livefront/livefront-backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

pip install -e .
python -m pytest -q
```

**API Docs**
Make sure both backend server is running on local
[Swagger API Docs](http://localhost:8000/docs#/default)


## Images of the product

#### Loading the app
![Welcome](https://github.com/yatharthgarg/cartoncaps-livefront/blob/main/livefront-frontend/public/Welcome%20screen.png)

#### Asking for product recommendation
![Product Recs](https://github.com/yatharthgarg/cartoncaps-livefront/blob/main/livefront-frontend/public/Product%20recs.png)

#### Asking about referral
![Referral](https://github.com/yatharthgarg/cartoncaps-livefront/blob/main/livefront-frontend/public/FAQ.png)

#### Documentation
![Documentation](https://github.com/yatharthgarg/cartoncaps-livefront/blob/main/livefront-frontend/public/Documentation.png)

**NOTE** - 
Please go to the **?** logo on the top-right screen to access the design documentation

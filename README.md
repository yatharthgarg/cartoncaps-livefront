Carton Caps Conversational AI Assistant

Overview

This repository hosts the backend service and API implementation for CapConnect, the conversational AI assistant for Carton Caps. CapConnect provides personalized product recommendations, handles FAQs, and explains the referral program, all within a conversational user interface powered by an open-source LLM and Retrieval-Augmented Generation (RAG).

⸻

Features
	•	Conversational AI: Personalized and engaging interactions with customers.
	•	Product Recommendations: Smart, contextually relevant product suggestions.
	•	Referral Program Integration: Clear communication of benefits and rules.
	•	FAQ Handling: Accurate answers based on pre-defined FAQs and rules.
	•	Context Management: Maintains conversational context for seamless user experience.
	•	Scalable Architecture: Lightweight for prototyping with clear path for scaling in production.

⸻

Technology Stack
	•	Backend: FastAPI, Python
	•	Database: SQLite (async via aiosqlite)
	•	Embeddings & Retrieval: Sentence-Transformers (MiniLM), FAISS
	•	LLM: TinyLlama (for prototype/demo purposes)
	•	Frontend: Next.js, React, Tailwind CSS

⸻

API Contract

Route	Purpose	Request Example	Response Example
POST /chat	Send user message, get assistant reply	{ "user_id": 1, "conversation_id": null, "message": "What can you help me with?" }	{ "conversation_id": "abc123-uuid", "reply": "I can help you with products, referrals, and FAQs.", "recommendations": [/* optional */] }
GET /welcome/{user_id}	Return welcome/referral intro for user	-	{ "messages": [ "Remember: 20% of your purchase goes to Riverview Elementary!", "Hi Anna! I’m Capper…" ] }
GET /users	List user profiles	-	[ { "id": 1, "name": "Anna Spears" }, { "id": 2, "name": "Bob Jones" } ]
GET /health	Health/Liveness Check	-	{ "status": "ok" }


⸻

Setup and Running Locally

Prerequisites
	•	Python 3.9+
	•	Node.js 18+

Backend Setup

# Clone repository
git clone <repo_url>
cd carton-caps-backend

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

Frontend Setup

cd frontend
npm install
npm run dev


⸻

Key Architectural Decisions
	•	FastAPI with Async: Enables efficient non-blocking operations, suitable for real-time interaction.
	•	SQLite + aiosqlite: Ideal for lightweight prototypes and demos with async support.
	•	Sentence-Transformers + FAISS: Provides quick semantic search and retrieval.
	•	TinyLlama (Local): Chosen for quick iteration and demonstration purposes.

⸻

Privacy and Data Security
	•	User data remains local.
	•	Minimal personal information is used (first name, school name only).
	•	Conversation logs encrypted and stored temporarily.

⸻

Future Roadmap
	•	Phase 1 (Demo): TinyLlama, local FAISS & SQLite
	•	Phase 2 (Internal Beta): Cloud-hosted LLM, pgvector for embeddings
	•	Phase 3 (Production): High-scale cloud infrastructure with advanced LLM (Llama-3-70B or Mixtral)
	•	Phase 4 (Premium): Advanced personalization and state-of-the-art LLM usage (GPT-4o)

⸻

Contributing

Feel free to fork, open issues, and submit pull requests to enhance CapConnect!

⸻

© Carton Caps
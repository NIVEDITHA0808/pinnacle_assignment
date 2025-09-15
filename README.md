# 🚗 Stevens Creek Chevrolet Voice Assistant

## App Link: 
## Demo Video: https://vimeo.com/1118650209
## Technical Documentation: https://docs.google.com/document/d/1qql6GQbJ6ymxraNm1IUiLgkp3zcBatRC/edit?usp=sharing&ouid=116776730695333944730&rtpof=true&sd=true
An intelligent voice-enabled assistant for Stevens Creek Chevrolet customers.
It helps with:

1. Answering dealership-related queries.

2. Providing information on vehicles, services, and promotions.

3. Scheduling sales/service appointments.

4. Conversational AI with voice input/output.

##✨ Features

🎤 Voice Input & Output (Speech-to-Text + Text-to-Speech).

💬 Conversational AI powered by Groq API.

📑 Retrieval-Augmented Generation (RAG): Fetches latest offers from dealership website.

📅 Booking System: Secure JWT-based appointment scheduling.

🗄 SQLite Database for storing scraped dealership data.

⚡ Streamlit UI for interactive chat experience.

## 🏗 Project Structure
.
├── app.py              # Streamlit UI + Voice assistant integration
├── booking.py          # Appointment booking system (JWT, availability, scheduling)
├── groq_client.py      # Conversational AI integration with Groq API
├── rag.py              # Simple retrieval engine (SQLite keyword search)
├── scraper.py          # Web scraper to update dealership specials
├── retrieval_data.db   # SQLite DB (auto-generated after scraping)

## 🔧 Setup & Installation
1. Clone Repository
git clone https://github.com/your-repo/chevy-voice-assistant.git
cd chevy-voice-assistant

2. Create Virtual Environment & Install Dependencies
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

pip install -r requirements.txt

3. Environment Variables

Set required keys before running:

# Groq API Key
export GROQ_API_KEY="your_groq_api_key"

# JWT Secret Key
export SECRET_KEY="your_secret_key"


Windows (PowerShell):

setx GROQ_API_KEY "your_groq_api_key"
setx SECRET_KEY "your_secret_key"

4. Initialize Database
python -m scraper retrieval_data_db
python -m scraper scrape_retrieval_data

5. Run the App
streamlit run app.py

📂 Database Schema

Table: retrieval_data

Column     | 	Type	  |    Description
id         |  INTEGER	|   Primary key
category	 |  TEXT	  |   Data type (vehicle/offer)
title	     |  TEXT	  |   Title of record
description|  TEXT	  |   Description of record
url	       |  TEXT	  |   Link to details
📡 API Overview
Booking API (booking.py)

create_session(user_id: str) → Generate JWT session.

verify_session(token: str) → Validate session.

get_availability(agent_name: str) → Get next 5 slots.

book_appointment(agent_type, agent_name, time_slot) → Book appointment.

Conversational AI (groq_client.py)

chat_with_groq(user_query: str) → Generate empathetic assistant response.

Retrieval (rag.py)

search_retrieval_data(query: str) → Keyword-based DB search.

Scraper (scraper.py)

scrape_retrieval_data() → Scrape dealership offers and update DB.

📊 Architecture Overview

UI Layer: Streamlit app with chat + voice.

Voice Services: SpeechRecognition (STT), gTTS (TTS).

Conversational AI: Groq API with retrieval augmentation.

Data Layer: SQLite DB + scraper.

Booking: JWT-secured mock calendar system.

🚀 Future Improvements

Upgrade to semantic search (e.g., embeddings + vector DB).

Replace mock booking with real scheduling API.

Improve scraping selectors for production.

Add user authentication for persistent sessions.

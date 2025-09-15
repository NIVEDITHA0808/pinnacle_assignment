import os
from groq import Groq
from rag import search_retrieval_data

# -------------------------------------------------------------------
# Initialize the Groq client
# -------------------------------------------------------------------
# Reads the GROQ_API_KEY from environment variables.
# Make sure you set it either via:
#   export GROQ_API_KEY="your_api_key_here"   (Linux/macOS)
#   setx GROQ_API_KEY "your_api_key_here"     (Windows PowerShell/CMD)
#
# Or use `.env` with python-dotenv for local dev.
# The "Groq-Model-Version" header ensures we always use the latest model.
# -------------------------------------------------------------------
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key, default_headers={
        "Groq-Model-Version": "latest"
    })

def chat_with_groq(user_query: str)->str:
    """
    Handles a user query by combining conversational AI with dealership knowledge.

    Workflow:
        1. Construct a system prompt that sets the assistant’s behavior 
           (empathetic, professional Chevrolet dealership assistant).
        2. Retrieve relevant dealership specials/offers dynamically 
           using `search_retrieval_data()`.
        3. Send the combined prompt + user query to Groq’s chat completion API.
        4. Return the assistant’s reply text.

    Args:
        user_query (str): The user's input question or request.

    Returns:
        str: The assistant's reply (natural language response).
    """

    # -------------------------------------------------------------------
    # Step 1: Define assistant persona and conversational style
    # -------------------------------------------------------------------
    system_prompt = (
        "You are a friendly and empathetic Chevrolet dealership assistant. "
        "You provide helpful, accurate answers about vehicles, services, promotions, and offers. "
        "Always maintain a warm, professional tone. "
        "If the user expresses concerns (e.g., car trouble), provide empathetic reassurance and suggest next steps. "
        "Gently recommend dealership services or booking an appointment when appropriate. "
        "Current dealership specials and offers are available below:\n\n"
    )
     # -------------------------------------------------------------------
    # Step 2: Add dynamic retrieval data (latest dealership specials)
    # -------------------------------------------------------------------
    system_prompt += search_retrieval_data(user_query)

    try:
        # -------------------------------------------------------------------
        # Step 3: Send query to Groq API
        # -------------------------------------------------------------------
        completion = client.chat.completions.create(
            model="groq/compound-mini",  # Selected conversational model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
            temperature=0.7,  # Adds slight creativity to responses
        )

        # -------------------------------------------------------------------
        # Step 4: Extract and return assistant reply
        # -------------------------------------------------------------------
        reply = completion.choices[0].message.content
        return reply
    except Exception as e:
        # Handle any API/connection errors gracefully
        print("❌ Error in chat:", e)
        return "Sorry, something went wrong while processing your request."

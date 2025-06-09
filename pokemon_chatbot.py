import os
import requests
from openai import Client
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class PokemonChatbot:
    def __init__(self):
        self.client = Client(
            base_url="https://models.github.ai/inference",
            api_key=os.getenv("GITHUB_TOKEN")
        )
        self.pokeapi_base_url = "https://pokeapi.co/api/v2/"
        
    def get_pokemon_info(self, pokemon_name: str) -> Dict[str, Any]:
        """Fetch Pokemon information from PokeAPI."""
        try:
            response = requests.get(f"{self.pokeapi_base_url}pokemon/{pokemon_name.lower()}")
            if response.status_code == 200:
                data = response.json()
                return {
                    "name": data["name"],
                    "types": [t["type"]["name"] for t in data["types"]],
                    "height": data["height"],
                    "weight": data["weight"],
                    "abilities": [a["ability"]["name"] for a in data["abilities"]]
                }
            return None
        except Exception as e:
            print(f"Error fetching Pokemon info: {e}")
            return None

    def generate_response(self, user_input: str) -> str:
        """Generate a response using the chatbot."""
        # First, try to extract any Pokemon names from the query
        try:
            # Create a message that includes Pokemon expertise
            messages = [
                {"role": "system", "content": "You are a Pokemon expert chatbot. You have extensive knowledge about Pokemon, their types, abilities, and characteristics. Always be enthusiastic and friendly in your responses, and try to include interesting Pokemon facts when relevant."},
                {"role": "user", "content": user_input}
            ]

            # If the query mentions a specific Pokemon, fetch its data
            pokemon_name = self._extract_pokemon_name(user_input)
            if pokemon_name:
                pokemon_info = self.get_pokemon_info(pokemon_name)
                if pokemon_info:
                    # Add Pokemon info to the context
                    messages.insert(1, {
                        "role": "system",
                        "content": f"Pokemon data: {pokemon_info}"
                    })

            # Generate response using GitHub AI
            response = self.client.chat.completions.create(
                messages=messages,
                temperature=0.7,
                top_p=1.0,
                model="openai/gpt-4.1"
            )
            
            return response.choices[0].message.content

        except Exception as e:
            return f"I encountered an error: {str(e)}"

    def _extract_pokemon_name(self, text: str) -> str:
        """
        Simple method to extract Pokemon names from text.
        This could be enhanced with better NLP techniques.
        """
        # Convert to lowercase for easier matching
        text = text.lower()
        
        # Try to find Pokemon name in the query
        try:
            # Make a test API call with words from the query
            words = text.split()
            for word in words:
                response = requests.get(f"{self.pokeapi_base_url}pokemon/{word}")
                if response.status_code == 200:
                    return word
        except:
            pass
        
        return None

if __name__ == "__main__":
    # Simple CLI for testing
    chatbot = PokemonChatbot()
    print("Pokemon Chatbot initialized! Type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        response = chatbot.generate_response(user_input)
        print(f"\nChatbot: {response}") 
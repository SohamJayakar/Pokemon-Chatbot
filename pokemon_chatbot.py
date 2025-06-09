import os
import requests
from openai import Client
from dotenv import load_dotenv
from typing import Dict, Any
from colorama import init, Fore, Style
import time
import markdown
import re

# Initialize colorama for Windows support
init(convert=True)

# ASCII Art for Pokemon
POKEMON_BANNER = """
{yellow}======================================
     ⚡  Pokemon Chatbot Master  ⚡
======================================{reset}
"""

load_dotenv()

def format_markdown_for_cli(text: str) -> str:
    """Convert markdown to colored CLI text."""
    # Store the original text
    formatted_text = text
    
    # Handle bold text with ** or __
    formatted_text = re.sub(r'\*\*(.+?)\*\*|__(.+?)__', 
                          lambda m: f"{Fore.CYAN}{m.group(1) or m.group(2)}{Style.RESET_ALL}", 
                          formatted_text)
    
    # Handle italic text with * or _
    formatted_text = re.sub(r'\*(.+?)\*|_(.+?)_',
                          lambda m: f"{Fore.YELLOW}{m.group(1) or m.group(2)}{Style.RESET_ALL}",
                          formatted_text)
    
    # Handle headers (e.g., # Header)
    formatted_text = re.sub(r'^#+ (.+)$',
                          lambda m: f"\n{Fore.GREEN}{Style.BRIGHT}{m.group(1)}{Style.RESET_ALL}",
                          formatted_text,
                          flags=re.MULTILINE)
    
    # Handle bullet points
    formatted_text = re.sub(r'^\* (.+)$',
                          lambda m: f"{Fore.YELLOW}•{Style.RESET_ALL} {m.group(1)}",
                          formatted_text,
                          flags=re.MULTILINE)
    
    # Handle numbered lists while preserving numbers
    formatted_text = re.sub(r'^(\d+\.) (.+)$',
                          lambda m: f"{Fore.YELLOW}{m.group(1)}{Style.RESET_ALL} {m.group(2)}",
                          formatted_text,
                          flags=re.MULTILINE)
    
    # Add color to key terms (like "Type:", "Ability:", etc.)
    key_terms = {
        r'Type:': f"{Fore.MAGENTA}Type:{Style.RESET_ALL}",
        r'Ability:': f"{Fore.MAGENTA}Ability:{Style.RESET_ALL}",
        r'Appearance:': f"{Fore.MAGENTA}Appearance:{Style.RESET_ALL}",
        r'Fun Fact:': f"{Fore.MAGENTA}Fun Fact:{Style.RESET_ALL}",
        r'Stats:': f"{Fore.MAGENTA}Stats:{Style.RESET_ALL}",
    }
    
    for term, replacement in key_terms.items():
        formatted_text = formatted_text.replace(term, replacement)
    
    return formatted_text

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
            print(f"{Fore.RED}Error fetching Pokemon info: {e}{Style.RESET_ALL}")
            return None

    def generate_response(self, user_input: str, for_cli: bool = True) -> str:
        """Generate a response using the chatbot."""
        try:
            # Create a message that includes Pokemon expertise
            messages = [
                {"role": "system", "content": "You are a Pokemon expert chatbot. You have extensive knowledge about Pokemon, their types, abilities, and characteristics. Always be enthusiastic and friendly in your responses, and try to include interesting Pokemon facts when relevant. Format important terms in bold using ** and use bullet points where appropriate."},
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

            # Show typing indicator
            print(f"{Fore.CYAN}Thinking...{Style.RESET_ALL}", end='\r')

            # Generate response using GitHub AI
            response = self.client.chat.completions.create(
                messages=messages,
                temperature=0.7,
                top_p=1.0,
                model="openai/gpt-4.1"
            )
            
            # Clear the typing indicator
            print(" " * 20, end='\r')
            
            # Format the markdown response for CLI
            if for_cli:
                return format_markdown_for_cli(response.choices[0].message.content)
            else:
                return response.choices[0].message.content

        except Exception as e:
            return f"{Fore.RED}I encountered an error: {str(e)}{Style.RESET_ALL}"

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

def print_welcome_message():
    """Print a welcoming message with instructions."""
    banner = POKEMON_BANNER.format(yellow=Fore.YELLOW, reset=Style.RESET_ALL)
    print(banner)
    print(f"{Fore.GREEN}Welcome to the Pokemon Chatbot!{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}You can ask me anything about Pokemon, such as:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}• Information about specific Pokemon")
    print("• Pokemon types and abilities")
    print("• Battle strategies")
    print(f"• Evolution chains{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Type 'quit' to exit the chat{Style.RESET_ALL}")
    print("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    # Simple CLI for testing
    chatbot = PokemonChatbot()
    print_welcome_message()
    
    while True:
        try:
            user_input = input(f"{Fore.GREEN}You:{Style.RESET_ALL} ")
            if user_input.lower() == 'quit':
                print(f"\n{Fore.YELLOW}Thanks for chatting! See you next time!{Style.RESET_ALL}\n")
                break
            
            response = chatbot.generate_response(user_input)
            print(f"\n{Fore.BLUE}Chatbot:{Style.RESET_ALL} {response}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Chat ended by user. Goodbye!{Style.RESET_ALL}\n")
            break
        except Exception as e:
            print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}\n") 
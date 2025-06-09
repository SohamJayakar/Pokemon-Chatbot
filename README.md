# Pokémon Chatbot

A specialized chatbot that can answer questions about Pokémon, powered by GitHub's AI model inference and the PokeAPI.

## Features

- Natural language conversations about Pokémon
- Access to detailed Pokémon information through PokeAPI integration
- Web-based interface for easy interaction
- Responsive design that works on both desktop and mobile

## Setup

1. Clone this repository

2. Create a GitHub Personal Access Token (PAT):
   - Go to GitHub Settings > Developer Settings > Personal Access Tokens
   - Create a new token with `models:read` permission
   - Copy your token

3. Set up your environment:
   - Create a `.env` file in the root directory
   - Add your GitHub token:
     ```
     GITHUB_TOKEN=your_github_token_here
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`
3. Start chatting with the bot!

You can ask questions like:
- "Tell me about Pikachu"
- "What are the different types of Pokémon?"
- "What are Charizard's abilities?"
- "Which Pokémon are strong against water types?"

## Technical Details

The chatbot uses:
- GitHub's AI model inference (GPT-4.1) for natural language understanding and generation
- PokeAPI for accurate Pokémon data
- Flask for the web server
- HTML/CSS/JavaScript for the frontend interface

## Note

You'll need a GitHub Personal Access Token with `models:read` permission to use this chatbot. The free tier has rate limits - for production use, consider using Azure AI Foundry. 
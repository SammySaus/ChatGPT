from flask import Flask, render_template, request
import requests
from requests.exceptions import RequestException
import os
from dotenv import load_dotenv

app = Flask(__name__)
# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("CHATGPT_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

def generate_response(prompt, system_message=None):
    if system_message is None:
        system_message = "You are a helpful assistant."
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": system_message},
                     {"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for any HTTP errors (4xx or 5xx)

        return response.json()["choices"][0]["message"]["content"]

    except RequestException as e:
        # Handle any request exceptions (e.g., connection error, timeout, etc.)
        return f"Error: {e}"

    except Exception as e:
        # Handle any other unexpected exceptions
        return f"An unexpected error occurred: {e}"


@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form["user_input"]
        system_message = request.form.get("system_message")

        if not user_input.strip():
            return "Error: User input cannot be empty."

        if system_message is not None and not system_message.strip():
            return "Error: Custom Bot Persona cannot be empty."

        response = generate_response(user_input, system_message)
        return render_template("index.html", user_input=user_input, system_message=system_message, response=response)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

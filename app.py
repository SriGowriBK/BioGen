import openai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv 
import os

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_bio', methods=['POST'])
def generate_bio():
    data = request.json  # Receive JSON data from frontend
    name = data.get('name', 'User')
    career = data.get('career', 'Unspecified Career')
    personality = data.get('personality', 'Unspecified Personality')
    interests = data.get('interests', 'Unspecified Interests')
    relationship = data.get('relationship', 'Unspecified Relationship Goals')
    beliefs = data.get('beliefs', 'Unspecified Beliefs')
    bucket_list = data.get('bucketList', 'No Bucket List Items')

    # Construct a detailed prompt for OpenAI API
    prompt = (
        f"Write a concise, creative, and engaging bio in the first person. The tone should be warm, reflective, and personal, "
        f"similar to examples like:\n\n"
        f"- Globe-trotting architect with a passion for spicy food and sustainable design. Seeking a fellow adventurer who can appreciate a good biryani and a thought-provoking conversation.\n"
        f"- Introverted writer with a love for classic literature and indie coffee shops. Looking for someone who can match my wit and charm over a cup of chai and a deep discussion about our favorite novels.\n\n"
        f"My name is {name}. I am a {career}. I would describe myself as {personality}. "
        f"My interests include {interests}. My relationship goals are {relationship}. "
        f"My beliefs and ethics are rooted in {beliefs}. "
        f"On my bucket list are things like {bucket_list}. "
        f"Craft a bio that reflects my unique qualities while being creative and inspiring."
    )

    try:
        # Call OpenAI API using the newer gpt-3.5-turbo or gpt-4 model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-3.5-turbo or gpt-4
            messages=[
                {"role": "system", "content": "You are a creative bio generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8  # Increase temperature for more creative output
        )
        bio = response['choices'][0]['message']['content'].strip()
        return jsonify({"bio": bio})  # Send the generated bio back to the frontend

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

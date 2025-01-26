from dotenv import load_dotenv
import os
import openai

# Load .env file
load_dotenv()

# Get API Key
openai.api_key = os.getenv("OPENAI_API_KEY")
print("API Key Loaded:", openai.api_key)  # Debug to verify if the key is loaded

prompt = "Create a 1500-calorie meal plan for a day."
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for creating personalized meal plans."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
        temperature=0.7,
    )
    meal_plan = response['choices'][0]['message']['content'].strip()
    print("Meal Plan:", meal_plan)
except Exception as e:
    print("Error generating meal plan:", e)

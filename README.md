# AI Calorie & Meal Planner

A Streamlit app to calculate daily calorie needs and generate meal plans using OpenAI.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add your OpenAI API key to `.env`
3. Run: `streamlit run calorie_meal_planner.py`

## Activity Level Multipliers (Harris-Benedict Equation)
The activity_multipliers dictionary applies the Harris-Benedict Equation, a formula used to estimate a person’s Total Daily Energy Expenditure (TDEE). TDEE represents the total calories a person burns in a day, accounting for their basal metabolic rate (BMR) and physical activity.

# What Each Multiplier Represents:
Sedentary (1.2): Little to no exercise (e.g., desk job, minimal movement).

Lightly Active (1.375): Light exercise 1–3 days/week (e.g., walking, light workouts).

Moderately Active (1.55): Moderate exercise 3–5 days/week (e.g., jogging, cycling).

Very Active (1.725): Hard exercise 6–7 days/week (e.g., intense sports, manual labor).

Extremely Active (1.9): Very hard exercise + physical job (e.g., athletes, construction workers).

# How It Works:
Calculate BMR (calories burned at rest) using the Harris-Benedict formula.

Multiply BMR by the activity multiplier to get TDEE.

Example:
If BMR = 1,500 calories and activity level = "Moderately Active":
TDEE = 1,500 × 1.55 = 2,325 calories/day.

## 2. Goal Multipliers
The goal_multipliers dictionary adjusts TDEE based on the user’s fitness goal (weight loss, maintenance, or gain). These multipliers create a calorie deficit or surplus.

What Each Multiplier Represents:
Lose Weight (0.85): A 15% calorie deficit (consuming 85% of TDEE).
Example: For TDEE = 2,325 → 2,325 × 0.85 = 1,976 calories/day.

Maintain Weight (1.0): Eat exactly at TDEE (no deficit/surplus).

Gain Weight (1.15): A 15% calorie surplus (common for muscle gain).
Example: For TDEE = 2,325 → 2,325 × 1.15 = 2,674 calories/day.

## User Input → BMR → TDEE → Goal-Adjusted Calories → Meal Planner (Phase 2)"# MealMind-AI" 

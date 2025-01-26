import streamlit as st
import os
from dotenv import load_dotenv

# Initialize session state variables
if 'show_meal_planner' not in st.session_state:
    st.session_state.show_meal_planner = False
if 'daily_calories' not in st.session_state:
    st.session_state.daily_calories = None
if 'maintenance_calories' not in st.session_state:
    st.session_state.maintenance_calories = None

load_dotenv()

# Debugging: Check session state
st.write("Debug Info:")
st.write(f"Show Meal Planner: {st.session_state.get('show_meal_planner', False)}")
st.write(f"Daily Calories: {st.session_state.get('daily_calories', None)}")
st.write(f"Maintenance Calories: {st.session_state.get('maintenance_calories', None)}")


st.title("AI Calorie & Meal Planner 🍎")

st.header("Step 1: To Calulate Your Daily Calories ")

st.subheader("Built By prajwaldev20 ")

"""
st.info("This is an information")
st.warning("This is a warning")
st.error("This is an error")

"""
if not st.session_state.show_meal_planner:  # Only show Step 1 if Meal Planner is not active

    with st.form("calorie_form"):
        gender = st.radio("Gender",["Male","Female","Other"])
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        weight = st.number_input("Weight (Kg)", min_value=30, value=70)
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=160)
        activity_level = st.selectbox(
            "Activity Level", ["Sedentary","Lightly Active", "Moderately Active","Very Active","Extremely Active"]
        )
        goal = st.selectbox("Goal",["Lose Weight", "Maintain Weight","Gain Weight"])
        submit_button = st.form_submit_button("Calculate Calories")


    # Activity level multipliers(Harris-Benedict equation)
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active":1.375,
        "Moderately Active":1.55,
        "Very Active":1.725,
        "Extremely Active":1.9
        }

    goal_multipliers = {
        "Lose Weight":0.85, # 15% Calorie deficit
        "Maintain Weight":1.0,
        "Gain Weight":1.15 # 15% calorie surplus
        }

    def calculate_calories(gender,age,weight,height,activity_level,goal):
        """Calculate daily calories using the Mifflin-St Jeor quation."""
        if gender =="Male":
            bmr = 10 * weight + 6.25 * height -5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height -5 * age - 161

        # Adjust for activity level
        activity_factor = activity_multipliers.get(activity_level,1.0)
        maintenance_calories = bmr * activity_factor

        # Adjust for goal
        goal_factor = goal_multipliers.get(goal,1.0)
        daily_calories = maintenance_calories * goal_factor

        return round(daily_calories),  round(maintenance_calories)

    # Display results when form is submitted

    if submit_button:
        daily_cal,maintenance_cal = calculate_calories(gender, age, weight, height, activity_level, goal)
     
        # Store values in session state
        st.session_state.daily_calories = daily_cal
        st.session_state.maintenance_calories = maintenance_cal
    
    
        st.header("📊 Your Nutrition Plan")
    
        # Custom calorie card
        st.markdown(f"""
        <div style="
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
        ">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">🎯 Daily Calorie Target</h3>
            <p style="font-size: 42px; color: #e74c3c; margin: 10px 0; font-weight: 700;">
                {daily_cal}
            </p>
            <p style="color: #7f8c8d; font-size: 14px;">
                (Maintenance Calories: {maintenance_cal})
            </p>
        </div>
        """, unsafe_allow_html=True)
    
        # Divider
        st.write("---")
        # Next steps section
        st.subheader("Next Steps ➡️")
    
        # Meal planner button
    if st.button("Generate Personalized Meal Plan 🍽️"):
        st.session_state.show_meal_planner = True # Update session state


if st.session_state.show_meal_planner:
    st.header("Step 2: Generate Your AI-Powered Meal Plan 🍽️")
    st.markdown("---")

    with st.form("meal_plan_form"):
        # Split into columns for better layout
        col1, col2 = st.columns(2)

        with col1:
            dietary_prefs = st.multiselect(
                "Dietary Preferences",
                ["Vegetarian","Non Vegetarian","Vegan","Gluten-Free","Dairy-Free","Keto","Paleo"],
                help="Select all that apply"
            )

        with col2:
            cuisine = st.selectbox(
                "Preferred Cuisine",
                ["Any","Italian","Mexican","Asian","Mediterranean","Indian","American","Middle Eastern"],
                index=0
            )
        
        # Additional preferences
        protein_focus = st.slider("Protein Focus (%)", 10, 50, 20, help="Preferred protein percentage in meals")
        exclude_ingredients = st.text_input("Exclude Ingredients (comma-separated)", placeholder="e.g., mushrooms, peanuts")

        generate_button = st.form_submit_button("🚀 Generate Meal Plan")

    if generate_button:
        #st.write("Button clicked!")
        #st.write(f"Daily Calories: {st.session_state.daily_calories}")
        #st.write(f"Prompt: {prompt}")
        if not os.getenv("OPENAI_API_KEY"):
            st.error("🔑 Error: OpenAI API key not found in environment variables")
            st.stop()

        # Build dynamic prompt
        prompt = f"""
        Create a detailed daily meal plan with these requirements:
        - Target calories: {st.session_state.daily_calories} (Maintenance: {st.session_state.maintenance_calories})
        - Dietary preferences: {', '.join(dietary_prefs) if dietary_prefs else 'None'}
        - Cuisine style: {cuisine}
        - Protein focus: {protein_focus}% of macros  # Removed space before %
        - Exclude: {exclude_ingredients if exclude_ingredients else 'Nothing'}

        Include for each meal (breakfast, lunch, dinner, 2 snacks):
        1. Meal name with calorie count
        2. Macros breakdown (protein/carbs/fat)
        3. Ingredients list
        4. Step-by-step instructions
        5. Prep time estimate
        
        Format with clear headings and emojis for readability.
        """

        try:
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")

            with st.spinner("🧠 AI Chef is crafting your perfect meal plan..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                     messages=[
                    {"role": "system", "content": "You are a helpful assistant for creating personalized meal plans."},
                    {"role": "user", "content": prompt},
                    ],
                    # engine="text-davinci-003",
                    # prompt=prompt,
                    max_tokens=1500,
                    temperature=0.7,
                )

            meal_plan = response['choices'][0]['message']['content'].strip()

            # Display results with styling
            st.markdown("---")
            st.subheader("🍎 Your Personalized Nutrition Plan")

            # Custom styled output
            st.markdown(f"""
            <div style="
                background: #2c3e50;
                color: #ecf0f1;
                padding: 25px;
                border-radius: 15px;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <pre style="white-space: pre-wrap; font-family: 'Courier New', monospace; font-size: 16px;">
                {meal_plan}
                </pre>
            </div>
            """, unsafe_allow_html=True)

            # Add regeneration button outside the form
            #if st.button("🔄 Regenerate Plan"):
               # st.experimental_rerun()
                
        except Exception as e:
            st.error(f"⚠️ Failed to generate meal plan: {str(e)}")
            st.error("Please check your OpenAI API key and internet connection")

    #if st.button("← Back to Calorie Calculator"):
        #st.session_state.show_meal_planner = False
        #st.experimental_rerun()

#json_response = {"status":200, "text":"response successful!"}
#st.write(json_response)
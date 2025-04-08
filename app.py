import streamlit as st
import pandas as pd
import pickle
import os

# --- Load Model and Data ---
st.set_page_config(page_title="Diet Recommendation System", layout="centered")

# Show working directory and files for debugging
st.write("📂 Current directory:", os.getcwd())
st.write("📄 Files found:", os.listdir())

# Load ML model
try:
    with open('food_model.pickle', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("❌ 'food_model.pickle' not found. Please make sure it's in the same folder as this script.")
    st.stop()

# Load food data
try:
    food_data = pd.read_csv('done_food_data.csv')
except FileNotFoundError:
    st.error("❌ 'done_food_data.csv' not found. Please make sure it's in the same folder as this script.")
    st.stop()

# Keywords to exclude for vegetarian filtering
exclude_keywords = [
    'Egg', 'Fish', 'meat', 'beef', 'Chicken', 'Beef', 'Deer', 'lamb', 'crab', 'pork',
    'Turkey', 'flesh', 'Ostrich', 'Emu', 'cuttelfish', 'Seaweed', 'crayfish', 'shrimp', 'Octopus'
]

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🍲 Muscle Gain", "🍛 Weight Gain", "🥗 Weight Loss", "🔍 Search Foods"])

# --- Home: Prediction ---
if page == "🏠 Home":
    st.title("🔮 Food Category Prediction")

    st.write("Enter your nutritional values below to predict a suitable category:")

    input_1 = st.number_input("Input 1", value=0.0)
    input_2 = st.number_input("Input 2", value=0.0)
    input_3 = st.number_input("Input 3", value=0.0)

    if st.button("Predict"):
        try:
            inputs = [[input_1, input_2, input_3]]
            prediction = model.predict(inputs)

            category_map = {
                'Muscle_Gain': '💪 Muscle Gain',
                'Weight_Gain': '🍛 Weight Gain',
                'Weight_Loss': '🥗 Weight Loss'
            }

            result = category_map.get(prediction[0], '🥣 General Food')
            st.success(f"Predicted Category: {result}")
        except Exception as e:
            st.error(f"Prediction Error: {e}")

# --- Filter Function ---
def apply_filters(data):
    vegetarian = st.checkbox("Vegetarian only")
    iron = st.checkbox("High in Iron (>6 mg)")
    calcium = st.checkbox("High in Calcium (>150 mg)")

    if iron:
        data = data[data['Iron_mg'] > 6]
    if calcium:
        data = data[data['Calcium_mg'] > 150]
    if vegetarian:
        data = data[~data['Descrip'].str.contains('|'.join(exclude_keywords), case=False)]

    return data

def recommend_foods(category_name):
    st.title(f"{category_name} Recommendations")
    data = food_data[food_data['category'] == category_name.replace(" ", "_")]

    data = apply_filters(data)

    if st.button("Show Recommended Foods"):
        if not data.empty:
            foods = data['Descrip'].sample(n=min(5, len(data))).tolist()
            st.write("### 🍽️ Top Picks:")
            for food in foods:
                st.write(f"- {food}")
        else:
            st.warning("No food found with selected filters.")

# --- Muscle Gain Page ---
if page == "🍲 Muscle Gain":
    recommend_foods("Muscle Gain")

# --- Weight Gain Page ---
if page == "🍛 Weight Gain":
    recommend_foods("Weight Gain")

# --- Weight Loss Page ---
if page == "🥗 Weight Loss":
    recommend_foods("Weight Loss")

# --- Search Page ---
if page == "🔍 Search Foods":
    st.title("🔍 Search and Sort Foods")
    sort_by = st.selectbox("Sort by", food_data.columns.tolist(), index=food_data.columns.get_loc("Descrip"))
    sorted_data = food_data.sort_values(by=sort_by)

    st.dataframe(sorted_data.reset_index(drop=True), use_container_width=True)

import os
import pandas as pd
import pickle as pkl
import streamlit as st
from sklearn.metrics  import accuracy_score

# Set page configuration
st.set_page_config(page_title="Diabetes Prediction", layout="wide", page_icon="🧑‍⚕")

# Load the saved diabetes model
diabetes_model_path = "diabetes_model.sav"


# Try loading the model with error handling
try:
    diabetes_model = pkl.load(open(diabetes_model_path, "rb"))
    st.write("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()  # Stop the app if the model fails to load

# Page title
st.title("Diabetes Prediction using Machine Learning")

# Getting user input
col1, col2, col3 = st.columns(3)

with col1:
    pregnancies = st.text_input("Number of Pregnancies")

with col2:
    glucose = st.text_input("Glucose Level")

with col3:
    blood_pressure = st.text_input("Blood Pressure") 

with col1:
    skin_thickness = st.text_input("Skin Thickness")

with col2:
    insulin = st.text_input("Insulin Level")

with col3:
    bmi = st.text_input("BMI (Body Mass Index)")

with col1:
    diabetes_pedigree_function = st.text_input("Diabetes Pedigree Function")

with col2:
    age = st.text_input("Age")

# Variable for storing the result
diab_diagnosis = ""

# Helper function to check if input is numeric
def is_valid_input(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Creating a button to predict the output
if st.button("Diabetes Test Result"):
    # Check if all inputs are valid
    inputs = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]
    
    # Check if any input is empty or invalid
    if not all(is_valid_input(val) for val in inputs):
        diab_diagnosis = "⚠ Please enter valid numeric values for all fields."
    else:
        try:
            # Convert the user input into float
            user_input = [
                float(pregnancies),
                float(glucose),
                float(blood_pressure),
                float(skin_thickness),
                float(insulin),
                float(bmi),
                float(diabetes_pedigree_function),
                float(age),
            ]
            
            # Debug: Show the user input
            st.write(f"User input for prediction: {user_input}")
            
            # Make the Prediction
            diab_prediction = diabetes_model.predict([user_input])

            # Debug: Show the prediction result
            st.write(f"Prediction result: {diab_prediction}")
            
            # Display the result
            if diab_prediction[0] == 1:
                diab_diagnosis = "The person has Diabetes 🩸"
            else:
                diab_diagnosis = "The person does not have Diabetes ✅"

        except Exception as e:
            diab_diagnosis = f"⚠ Error in prediction: {str(e)}"

# Show the prediction result
st.subheader("Prediction Result:")
st.write(diab_diagnosis)
if st.button('show Model Accuracy'):
    test_data=pd.read_csv(r"C:\Users\Siva\OneDrive\Desktop\proj1\diabetes.csv")
    x_test=test_data.drop(columns=['Outcome'])
    y_test=test_data['Outcome']

    y_pred=diabetes_model.predict(x_test)
    accuracy=accuracy_score(y_test,y_pred)
    st.write(f"model accuracy:{accuracy*100:.2f}%")

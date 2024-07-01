import streamlit as st
import numpy as np
import pandas as pd
import pickle
import hashlib
import os

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

# Credentials file
CREDENTIALS_FILE = 'credentials.csv'

# Feature names
FEATURE_NAMES = [
    "Item_Identifier", "Item_Weight", "Item_Fat_Content", "Item_Visibility",
    "Item_Type", "Item_MRP", "Outlet_Identifier", "Outlet_Establishment_Year",
    "Outlet_Size", "Outlet_Location_Type", "Outlet_Type"
]

# Hash function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Save user credentials to a CSV file
def save_credentials(username, hashed_password):
    df = pd.read_csv(CREDENTIALS_FILE) if os.path.exists(CREDENTIALS_FILE) else pd.DataFrame(columns=["username", "password"])
    new_entry = pd.DataFrame({"username": [username], "password": [hashed_password]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(CREDENTIALS_FILE, index=False)

# Check if user credentials are valid
def validate_credentials(username, password):
    if not os.path.exists(CREDENTIALS_FILE):
        return False
    df = pd.read_csv(CREDENTIALS_FILE)
    hashed_password = hash_password(password)
    return not df[(df["username"] == username) & (df["password"] == hashed_password)].empty

# Check if username already exists
def username_exists(username):
    if not os.path.exists(CREDENTIALS_FILE):
        return False
    df = pd.read_csv(CREDENTIALS_FILE)
    return not df[df["username"] == username].empty

# Streamlit app with enhanced styling and animations
def main():
    st.set_page_config(page_title="Sales Prediction", layout="wide")

    # Animated circles with RGB colors
    st.markdown(
        """
        <style>
        @keyframes circle {
            0% {
                box-shadow: 0 0 0 0px rgba(255, 0, 0, 0.4);
            }
            25% {
                box-shadow: 0 0 0 40px rgba(255, 0, 0, 0);
            }
            50% {
                box-shadow: 0 0 0 80px rgba(0, 255, 0, 0.4);
            }
            75% {
                box-shadow: 0 0 0 120px rgba(0, 0, 255, 0.4);
            }
            100% {
                box-shadow: 0 0 0 160px rgba(255, 0, 255, 0.4);
            }
        }

        .circle {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation: circle 5s infinite;
        }
        </style>
        """
        , unsafe_allow_html=True
    )

    st.markdown('<div class="circle"></div>', unsafe_allow_html=True)

    # Overlay container with content
    st.markdown(
        """
        <style>
        .container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: rgba(0, 0, 0, 0.8); /* Semi-transparent overlay */
            color: white;
            font-family: Arial, sans-serif;
            z-index: 1; /* Ensure content is above animated circles */
        }
        .content {
            max-width: 800px;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* Light shadow */
        }
        .heading {
            text-align: center;
            font-size: 36px;
            margin-bottom: 20px;
            animation: slide-down 1s ease-out; /* Example animation */
        }
        @keyframes slide-down {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .form-container {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            animation: fade-in 1s ease-out; /* Example animation */
        }
        @keyframes fade-in {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        .form-container input {
            width: 100%;
            padding: 10px;
            margin: 5px 0 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .button-container {
            text-align: center;
            margin-top: 20px;
        }
        .button-container button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: #ffffff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease; /* Smooth hover transition */
        }
        .button-container button:hover {
            background-color: #45a049;
        }
        </style>
        """
        , unsafe_allow_html=True
    )

    # st.markdown('<div class="container">', unsafe_allow_html=True)

   #  st.markdown('<div class="content">', unsafe_allow_html=True)

    st.markdown('<div class="heading">Sales Prediction App</div>', unsafe_allow_html=True)

    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_or_signup()
    else:
        app()

    #st.markdown('</div>', unsafe_allow_html=True)

    #st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def login_or_signup():
    option = st.selectbox("Choose an option", ["Login", "Sign Up"])
    if option == "Login":
        login()
    else:
        sign_up()

def login():
    #st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    #st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Login"):
        if validate_credentials(username, password):
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def sign_up():
    #st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.subheader("Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match")
        elif username_exists(username):
            st.error("Username already exists")
        else:
            hashed_password = hash_password(password)
            save_credentials(username, hashed_password)
            st.success("Account created successfully! Please log in.")
            st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def app():
    st.sidebar.subheader("Navigation")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    st.subheader("Enter the features for prediction")
    input_features = []
    for feature_name in FEATURE_NAMES:
        feature = st.text_input(f'{feature_name}')
        input_features.append(feature)
    
    if st.button('Predict'):
        # Clean and prepare input features
        cleaned_features = []
        for feature in input_features:
            cleaned_feature = ''.join(c for c in feature if c.isdigit() or c == '.')
            cleaned_features.append(cleaned_feature)
        
        try:
            input_features_array = np.array(cleaned_features, dtype=float).reshape(1, -1)
            
            # Make prediction
            prediction = model.predict(input_features_array)[0]
            
            # Display prediction
            st.success(f'Predicted Sales: {prediction}')
        except ValueError:
            st.error("Please enter valid numerical values for all features.")

if __name__ == '__main__':
    main()

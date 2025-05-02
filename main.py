import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import re
import string
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from nltk.tokenize import RegexpTokenizer
from nltk import PorterStemmer, WordNetLemmatizer
from functions import *
import pickle

# Function for Cyberbullying Tweet Prediction (mock function, replace with your actual model)
def custom_input_prediction(tweet_input):
    # This is a placeholder function. 
    categories = ["Age", "Ethnicity", "Gender", "Religion", "Other Cyberbullying", "Not Cyberbullying"]
    # Simple logic for demo (you would integrate your prediction logic here)
    return categories[np.random.choice(len(categories))]

# Function to handle chatbot responses
def chatbot_response(user_input):
    responses = {
    "hello": "Hi! How can I help you today? Feel free to ask any questions about cyberbullying.",
    "what is cyberbullying": "Cyberbullying is the use of technology to harass, threaten, or manipulate others. It can occur through social media, text messages, or other online platforms.",
    "how can I stop cyberbullying": "If you're experiencing cyberbullying, consider reporting the abuse to the platform, seeking support from trusted individuals, or contacting a professional counselor.",
    "I need help": "I'm here for you! Please tell me more about what you're going through, and I'll do my best to assist you.",
    "contact support": "For immediate assistance, you can contact local support groups or counseling services that specialize in handling cyberbullying cases.",
    "What is the current food trend?": "Plant-based eating, superfoods, and sustainable sourcing are some of the current food trends. There’s also a rise in alternative proteins and lab-grown meat.",
    "What are the healthiest foods to eat?": "Foods like leafy greens, berries, nuts, seeds, fatty fish, and whole grains are considered some of the healthiest options.",
    "What is a vegan diet?": "A vegan diet excludes all animal products such as meat, dairy, and eggs. It focuses on plant-based foods like vegetables, fruits, grains, and legumes.",
    "What are some popular food delivery apps?": "Popular food delivery apps include Uber Eats, Grubhub, DoorDash, and Postmates.",
    "How can I start a healthy diet?": "To start a healthy diet, focus on eating a variety of fruits and vegetables, limit processed foods, and incorporate lean proteins, whole grains, and healthy fats.",
    "What are the benefits of eating organic food?": "Eating organic food may reduce exposure to pesticides, support environmental sustainability, and increase intake of antioxidants and other beneficial nutrients.",
    "What is social media?": "Social media refers to online platforms where people can create, share, and interact with content. Popular examples include Facebook, Instagram, Twitter, etc.",
    "How does social media work?": "Social media works by allowing users to create content, interact with others through likes, comments, shares, and follow or be followed by other users.",
    "What are the benefits of social media?": "Social media offers several benefits like staying connected with family and friends, networking opportunities, and access to news and information.",
    "Why is social media important?": "Social media is important for communication, entertainment, business marketing, and education. It helps build communities and connect people globally.",
    "What are the popular social media platforms?": "Some of the popular social media platforms include Facebook, Instagram, Twitter, LinkedIn, TikTok, and YouTube.",
    "Can social media affect mental health?": "Yes, excessive use of social media can sometimes lead to mental health issues such as anxiety, depression, and loneliness. It's important to manage screen time and engage positively.",
    "What is the current trend in technology?": "The current trends in technology include artificial intelligence, machine learning, blockchain, 5G, and quantum computing.",
    "What is the current trend in fashion?": "Sustainability and eco-friendly fashion are becoming the new trends, along with smart clothing, minimalism, and vintage styles.",
    "What is the current trend in healthcare?": "Telemedicine, wearable health devices, and personalized medicine are some of the leading trends in healthcare.",
    "What is the current trend in the economy?": "The current economic trends involve inflation, digital currencies, and a focus on green energy investments.",
    "What is the current trend in social media?": "Short-form video content, influencer marketing, and social commerce are leading the trends on platforms like TikTok and Instagram.",
    "What are the latest trends in AI?": "Generative AI, natural language processing advancements, and AI-driven automation are among the most notable trends in artificial intelligence."
}

    
    # Return a response based on user input or a default response
    return responses.get(user_input.lower(), "Sorry, I didn't quite understand that. Can you rephrase your question?")

# Recommendation function based on prediction
def get_recommendation(prediction):
    recommendations = {
        "Age": "Consider discussing this matter with a responsible adult or contacting a support group for guidance on handling age-related bullying.",
        "Ethnicity": "If you're facing racial discrimination or bullying, it's important to reach out to a counselor or a support group specialized in cultural diversity.",
        "Gender": "Gender-based cyberbullying is serious. Consider reporting the abuse and reaching out to organizations supporting gender equality.",
        "Religion": "Religious bullying can be hurtful. Seek support from communities that celebrate religious tolerance, and don't hesitate to report such behavior.",
        "Other Cyberbullying": "Other forms of cyberbullying can include name-calling and harassment. Seek immediate help from trusted family members or professional counseling services.",
        "Not Cyberbullying": "It looks like your tweet is not related to cyberbullying, but always ensure to promote kindness and respect online.",
        "General": "If you're unsure about the tweet's nature, consider reaching out to a friend, or counselor for a second opinion."
    }
    
    return recommendations.get(prediction, "No specific recommendation available for this category.")

# Chatbot Page
def chatbot_page():
    st.title("Cyberbullying Chatbot")

    # Display a simple welcome message
    st.write("Welcome to the Cyberbullying Chatbot! Ask me anything related to cyberbullying, and I'll try my best to assist you.")
    
    # Create a text input box for the user to type their message
    user_input = st.text_input("You:", "")

    if user_input:
        response = chatbot_response(user_input)
        st.write(f"Chatbot: {response}")

    # Optionally, you can also add a feature to store the chat history for later reference
    # You can implement a loop or use session state for maintaining conversation history
    if "history" not in st.session_state:
        st.session_state.history = []
    
    if user_input:
        st.session_state.history.append(f"You: {user_input}")
        st.session_state.history.append(f"Chatbot: {response}")

    # Display the conversation history
    for message in st.session_state.history:
        st.write(message)

# Main page for Cyberbullying Tweet Recognition
def main_page():
    image = Image.open('images/logo.png')

    st.image(image, use_column_width=True)

    st.write('''
    # Cyberbullying Tweet Recognition App

    This app predicts the nature of the tweet into 6 Categories.
    * Age
    * Ethnicity
    * Gender
    * Religion
    * Other Cyberbullying
    * Not Cyberbullying

    ***
    ''')

    # Text Box for user input (Tweet)
    st.header('Enter Tweet ')
    tweet_input = st.text_area("Tweet Input", height=150)
    st.write('''
    ***
    ''')

    # Print input on webpage
    st.header("Entered Tweet text ")
    if tweet_input:
        tweet_input
    else:
        st.write('''***No Tweet Text Entered!***''')
    
    st.write('''***
    ''')

    # Output on the page
    st.header("Prediction")
    if tweet_input:
        prediction = custom_input_prediction(tweet_input)
        recommendation = get_recommendation(prediction)

        st.write(f"**Prediction**: {prediction}")
        st.write(f"**Recommendation**: {recommendation}")

        # Show image based on prediction (Example, replace with your actual images)
        if prediction == "Age":
            st.image("images/age_cyberbullying.png", use_column_width=True)
        elif prediction == "Ethnicity":
            st.image("images/ethnicity_cyberbullying.png", use_column_width=True)
        elif prediction == "Gender":
            st.image("images/gender_cyberbullying.png", use_column_width=True)
        elif prediction == "Not Cyberbullying":
            st.image("images/not_cyberbullying.png", use_column_width=True)
        elif prediction == "Other Cyberbullying":
            st.image("images/other_cyberbullying.png", use_column_width=True)
        elif prediction == "Religion":
            st.image("images/religion_cyberbullying.png", use_column_width=True)
    else:
        st.write('''***No Tweet Text Entered!***''')

    st.write('''***''')

# Sidebar for page navigation
def sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page", ("Main", "Chatbot"))

    if page == "Main":
        main_page()
    elif page == "Chatbot":
        chatbot_page()

# Run the app
sidebar()

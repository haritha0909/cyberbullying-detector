#Page 1
from ctypes import alignment
from urllib import response
import pandas as pd
import streamlit as st
import altair as alt
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

# Page title

image = Image.open('logo.png')

st.image(image, use_container_width= True)

st.write('''
# Cyberbulling Tweet Recognition App

This app predicts the nature of the tweet into 6 Categories.
* Age
* Ethnicity
* Gender
* Religion
* Other Cyberbullying
* Not Cyberbullying
''')

# Text Box
st.header('Enter Tweet ')
tweet_input = st.text_area("Tweet Input", height= 150)
print(tweet_input)
st.write('''
''')

# print input on webpage
st.header("Entered Tweet text ")
if tweet_input:
    tweet_input
else:
    st.write('''
    No Tweet Text Entered!
    ''')
st.write('''
*
''')

# Output on the page
st.header("Prediction")
if st.button("Analyze"):
    if tweet_input:
        prediction = custom_input_prediction(tweet_input)
        if prediction == "Age":
            st.image("age_cyberbullying.png",use_container_width= True)
        elif prediction == "Ethnicity":
            st.image("ethnicity_cyberbullying.png",use_container_width= True)
        elif prediction == "Gender":
            st.image("gender_cyberbullying.png",use_container_width= True)
        elif prediction == "Not Cyberbullying":
            st.image("not_cyberbullying.png",use_container_width= True)
        elif prediction == "Other Cyberbullying" :
            st.image("other_cyberbullying.png",use_container_width= True)
        elif prediction == "Religion":
            st.image("religion_cyberbullying.png",use_container_width= True)
else:
    st.write('''
    No Tweet Text Entered!
    ''')

st.write('''*''')



#Page 2

import streamlit as st
import re

# Basic Q&A data
Basic_Q = ("What is cyberbullying")
Basic_Ans = "Cyberbullying is the act of using digital platforms like social media, messaging apps, or online forums to harass, threaten, or humiliate others. It includes harmful behaviors like spreading rumors, sending abusive messages, or sharing embarrassing content." 
Basic_Q1 = ("what are major category cyberbullying")
Basic_Ans1 = "The major categories of cyberbullying include harassment, flaming, outing & doxxing, impersonation, exclusion, trolling, and cyberstalking. These involve actions like sending threats, spreading private information, creating fake profiles, and deliberately excluding or provoking others online."

# General questions and responses
general_questions = ["hi", "hello", "how are you", "how was your day", "what's up", "good morning", "good evening"]
general_answers = {
    "hi": "Hello! How can I help you today?",
    "hello": "Hi there! How can I assist you?",
    "how are you": "I'm doing well, thank you for asking! How about you?",
    "how was your day": "My day has been great, thanks for asking! How about yours?",
    "what's up": "Not much, just here to assist you. How can I help?",
    "good morning": "Good morning! How can I assist you today?",
    "good evening": "Good evening! What can I do for you?"
}

# Social Media related questions
social_media_questions = ["What is social media?", "How does social media work?", "What are the benefits of social media?", "Why is social media important?", "What are the popular social media platforms?", "Can social media affect mental health?"]
social_media_answers = {
    "What is social media?": "Social media refers to online platforms where people can create, share, and interact with content. Popular examples include Facebook, Instagram, Twitter, etc.",
    "How does social media work?": "Social media works by allowing users to create content, interact with others through likes, comments, shares, and follow or be followed by other users.",
    "What are the benefits of social media?": "Social media offers several benefits like staying connected with family and friends, networking opportunities, and access to news and information.",
    "Why is social media important?": "Social media is important for communication, entertainment, business marketing, and education. It helps build communities and connect people globally.",
    "What are the popular social media platforms?": "Some of the popular social media platforms include Facebook, Instagram, Twitter, LinkedIn, TikTok, and YouTube.",
    "Can social media affect mental health?": "Yes, excessive use of social media can sometimes lead to mental health issues such as anxiety, depression, and loneliness. It's important to manage screen time and engage positively."
}

# Current Trend related questions
current_trend_questions = [
    "What is the current trend in technology?", 
    "What is the current trend in fashion?", 
    "What is the current trend in healthcare?", 
    "What is the current trend in the economy?", 
    "What is the current trend in social media?", 
    "What are the latest trends in AI?"
]
current_trend_answers = {
    "What is the current trend in technology?": "The current trends in technology include artificial intelligence, machine learning, blockchain, 5G, and quantum computing.",
    "What is the current trend in fashion?": "Sustainability and eco-friendly fashion are becoming the new trends, along with smart clothing, minimalism, and vintage styles.",
    "What is the current trend in healthcare?": "Telemedicine, wearable health devices, and personalized medicine are some of the leading trends in healthcare.",
    "What is the current trend in the economy?": "The current economic trends involve inflation, digital currencies, and a focus on green energy investments.",
    "What is the current trend in social media?": "Short-form video content, influencer marketing, and social commerce are leading the trends on platforms like TikTok and Instagram.",
    "What are the latest trends in AI?": "Generative AI, natural language processing advancements, and AI-driven automation are among the most notable trends in artificial intelligence."
}

# Food-related questions and answers
food_questions = [
    "What is the current food trend?", 
    "What are the healthiest foods to eat?", 
    "What is a vegan diet?", 
    "What are some popular food delivery apps?", 
    "How can I start a healthy diet?", 
    "What are the benefits of eating organic food?"
]
food_answers = {
    "What is the current food trend?": "Plant-based eating, superfoods, and sustainable sourcing are some of the current food trends. There’s also a rise in alternative proteins and lab-grown meat.",
    "What are the healthiest foods to eat?": "Foods like leafy greens, berries, nuts, seeds, fatty fish, and whole grains are considered some of the healthiest options.",
    "What is a vegan diet?": "A vegan diet excludes all animal products such as meat, dairy, and eggs. It focuses on plant-based foods like vegetables, fruits, grains, and legumes.",
    "What are some popular food delivery apps?": "Popular food delivery apps include Uber Eats, Grubhub, DoorDash, and Postmates.",
    "How can I start a healthy diet?": "To start a healthy diet, focus on eating a variety of fruits and vegetables, limit processed foods, and incorporate lean proteins, whole grains, and healthy fats.",
    "What are the benefits of eating organic food?": "Eating organic food may reduce exposure to pesticides, support environmental sustainability, and increase intake of antioxidants and other beneficial nutrients."
}

# List of offensive words to censor
offensive_words = [
    # Age-Related
    'old', 'boomer', 'immature', 'childish', 'senile', 'elderly', 'juvenile', 'fossil', 'baby', 'wrinkly', 
    'ancient', 'crone', 'granny', 'codger', 'geezer', 'fart', 'grandpa', 'grandma',

    # Gender-Related
    'bitch', 'slut', 'whore', 'cunt', 'pussy', 'feminazi', 'simp', 'crybaby', 'bossy', 'gold digger', 
    'coward', 'sissy', 'tramp', 'skank', 'ho', 'thot', 'cow', 'nag', 'shrew',

    # Race-Related
    'nigger', 'chink', 'spic', 'gook', 'honky', 'cracker', 'wetback', 'beaner', 'jigaboo', 'coon', 
    'jungle bunny', 'yellow', 'half-breed', 'paki', 'gypsy', 'dago', 'wog', 'mick', 'kike', 'redskin', 
    'injun', 'abbo', 'eskimo', 'sand nigger', 'camel jockey',

    # Religion-Related
    'terrorist', 'infidel', 'kafir', 'bible thumper', 'pagan', 'witch', 'heathen', 'zealot', 'heretic', 
    'devil worshipper', 'cultist', 'blasphemer',

    # Disability-Related
    'retard', 'cripple', 'dumb', 'mute', 'deaf', 'blind', 'handicapped', 'lame', 'moron', 'nutcase', 
    'loon', 'psycho', 'maniac', 'spaz', 'twit', 'idiot', 'imbecile',

    # Sexual Orientation-Related
    'gay', 'fag', 'lesbo', 'homo', 'dyke', 'fruit', 'sissy', 'fairy', 'queen', 'flaming', 
    'tranny', 'butch', 'flamer', 'poof', 'sodomite',

    # Common Insults and Profanity
    'fuck', 'shit', 'asshole', 'dickhead', 'prick', 'moron', 'idiot', 'dumbass', 'jackass', 'scumbag', 
    'bastard', 'douchebag', 'cocksucker', 'motherfucker', 'cumdumpster', 'pisshead', 'twat', 'arsehole', 
    'fucktard', 'fuckwit', 'wanker', 'knobhead', 'tosser', 'dipshit', 'airhead', 'bonehead', 'numbnuts', 
    'fatass', 'dick', 'prick', 'loser', 'weakling', 'trash', 'horrible', 'liar', 'fake', 'hopeless', 
    'fool', 'toxic', 'insane', 'hate', 'pathetic', 'lazy', 'disgusting', 'nasty', 'mean', 'rude', 
    'noob', 'useless', 'failure', 'scum', 'vermin', 'filth'
]


# Function to censor offensive words and highlight them in red
def censor_text(text):
    for word in offensive_words:
        # Create a regex pattern to match whole words
        pattern = r'\b' + re.escape(word) + r'\b'
        # Replace word with red-colored censored text
        text = re.sub(pattern, lambda m: f'<span style="color:red;">{m.group(0)[0]}{"*" * (len(m.group(0)) - 1)}</span>', text, flags=re.IGNORECASE)
    return text

# Custom CSS for chat interface to make it look like WhatsApp and highlight bot replies
st.markdown("""
    <style>
        /* Set background image for the entire app */
        body {
            background-image: url('https://path_to_your_background_image.jpg');
            background-size: cover;
            background-position: center;
            font-family: 'Arial', sans-serif;
        }
        .chat-container {
            max-height: 500px;
            overflow-y: scroll;
            padding: 20px;
        }
        .chat-box {
            padding: 20px;
        }
        .user-message {
            background-color: #DCF8C6;
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
            width: 70%;
            margin-left: auto;
            display: flex;
            align-items: center;
        }
        .bot-message {
            background-color: #f1f1f1;
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
            width: 70%;
            margin-right: auto;
            display: flex;
            align-items: center;
            font-weight: bold;
            border-left: 4px solid #128C7E;  /* WhatsApp-like highlight */
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for storing chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to handle responses based on input
def get_answer(user_input):
    # Check if the question is in the general questions list
    for question, answer in zip(general_questions, general_answers.values()):
        if question.lower() in user_input.lower():
            return answer

    # Check if the question is in the social media related questions list
    for question, answer in zip(social_media_questions, social_media_answers.values()):
        if question.lower() in user_input.lower():
            return answer

    # Check if the question is in the current trend related questions list
    for question, answer in zip(current_trend_questions, current_trend_answers.values()):
        if question.lower() in user_input.lower():
            return answer

    # Check if the question is in the food related questions list
    for question, answer in zip(food_questions, food_answers.values()):
        if question.lower() in user_input.lower():
            return answer
    
    # Check for other predefined questions
    if any(q.lower() in user_input.lower() for q in Basic_Q):
        return Basic_Ans
    elif any(q.lower() in user_input.lower() for q in Basic_Q1):
        return Basic_Ans1
    else:
        return "Sorry, I didn't understand that."

# Function to handle input submission and clear input
def submit_input():
    # Store the user's message and bot's response
    user_input = st.session_state.widget
    censored_user_input = censor_text(user_input)
    st.session_state.messages.insert(0, {"role": "user", "content": censored_user_input})
    
    bot_response = get_answer(user_input)
    censored_bot_response = censor_text(bot_response)
    st.session_state.messages.insert(0, {"role": "bot", "content": censored_bot_response})

    # Clear the input field
    st.session_state.widget = ""

# Display chat interface
with st.form(key='chat_form'):
    st.text_area('Chat', value='', height=300, key='widget')
    st.form_submit_button('Send', on_click=submit_input)

# Display chat history with custom CSS styling
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)

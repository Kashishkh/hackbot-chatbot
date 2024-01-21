import mysql.connector
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
import google.generativeai as genai
# Database connection details (replace with your own)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="devesh@2004",
    database="hackbot_data"
)

cursor = db.cursor()

# Gemini API key
genai.configure(api_key = "AIzaSyA1wQHoaK2sSrKwA8_KhZFJKwSFXo466BM")  # Replace with your actual API key
model=genai.GenerativeModel('gemini-pro')

# Commands and their corresponding SQL queries
commands = {
    "hackathon details": "SELECT * FROM hackathons ORDER BY date DESC LIMIT 1",
    "upcoming hackathons": "SELECT * FROM hackathons WHERE date >= CURDATE() ORDER BY date",
    "find hackathons by topic": "SELECT * FROM hackathons WHERE topic LIKE %s",
    "find hackathons by location": "SELECT * FROM hackathons WHERE venue LIKE %s",
    "find hackathons by date": "SELECT * FROM hackathons WHERE date BETWEEN %s AND %s",
    "find hackathons by skills": "SELECT * FROM hackathons WHERE skills_required LIKE %s",
    "find hackathons by sponsor": "SELECT * FROM hackathons WHERE sponsors LIKE %s",
    "find hackathons by organizer": "SELECT * FROM hackathons WHERE collaborators LIKE %s",
    "find beginner-friendly hackathons": "SELECT * FROM hackathons WHERE description LIKE '%Beginner Friendly%'",
    "find hackathons with prizes": "SELECT * FROM hackathons WHERE prizes <> ''",
    "find hackathons with specific resources": "SELECT * FROM hackathons WHERE resources LIKE %s",
    "find virtual hackathons": "SELECT * FROM hackathons WHERE venue = 'Virtual'",
    "hackathon description": "SELECT hackathon_description FROM description WHERE hackathon_name = %s",
    "hackathon faq": "SELECT faq_question, faq_ans FROM faq WHERE hackathon_name = %s",
    "sort hackathons by": "SELECT * FROM hackathons ORDER BY %s",
    "filter hackathons by": "SELECT * FROM hackathons WHERE %s = %s"
}


# Functions for greeting, handling user queries, displaying results, and interacting with Gemini
def get_time_of_day():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 17:
        return "afternoon"
    elif 17 <= current_hour < 20:
        return "evening"
    else:
        return "night"

def greet_user():
    time_of_day = get_time_of_day()
    print(f"Good {time_of_day}! Welcome to Hackbot, your personalised hackathon assistant. How can I help you today?")

def user_end_output(result):
    #TODO create the user_end_output

def handle_user_query(query):
    try:
        # Use Gemini to determine the most suitable command
        gemini_response = get_gemini_response(query)  # Call the new function
        inferred_command = gemini_response

        if inferred_command in commands:
            cursor.execute(commands[inferred_command])
            results = cursor.fetchall()

            if results:
                # Process and display results in a user-friendly format
                if query == "hackathon details":
                    display_hackathon_details(results[0])
                elif query == "upcoming hackathons":
                    display_upcoming_hackathons(results)
                # ... handle other commands similarly
                else:
                    user_end_output(results)
                    
            else:
                print("No results found for that query.")

        else:
            print("Sorry, I'm not sure I understand. Could you rephrase your query?")

    except mysql.connector.Error as err:
        print("An error occurred while accessing the database:", err)
    except requests.exceptions.RequestException as err:
        print("An error occurred while communicating with Gemini:", err)

def display_hackathon_details(hackathon_data):
    """Displays details of a single hackathon."""

    print("\n**Here are the details of the hackathon:**")
    print(f"Name: {hackathon_data['name']}")
    print(f"Date: {hackathon_data['date']}")
    print(f"Time Duration: {hackathon_data['time_duration']}")
    print(f"Topic: {hackathon_data['topic']}")
    print(f"Venue: {hackathon_data['venue']}")
    print(f"Description: {hackathon_data['description']}")
    # Add more fields as needed, e.g., prizes, collaborators, etc.

def display_upcoming_hackathons(hackathons_data):
    """Displays a list of upcoming hackathons."""

    print("\n**Here are the upcoming hackathons:**")
    for hackathon in hackathons_data:
        print(f"- {hackathon['name']} - {hackathon['date']} - {hackathon['venue']}")

def get_gemini_response(query):
#    api_key = "AIzaSyA1wQHoaK2sSrKwA8_KhZFJKwSFXo466BM"  # Replace with your actual API key
#    url = f"https://api.gemi.ai/v1/completions?prompt={query}&max_tokens=5&temperature=0.7"
#    headers = {"Authorization": f"Bearer {api_key}"}
#    response = requests.get(url, headers=headers)
#    response.raise_for_status()  # Raise an exception for non-200 status codes
#    return response.json()
    
    prompt= "I have created a chatbot and using your NLP skills I want to make my chatbot better the user has given me this input: \n {query} \n Now according to your NLP skils tell me which does the user wants to run among these commands: {commands} \n just give me the command nothing more than that, also if the user's required command is not mentioned in the command list then give no command found. Remember I just want answer in one line which is from my command list."
    response=model.generate_content(prompt)
    print(response.text)
    return response.text

# Main chatbot loop
def run_chatbot(user_input):

    while True:
        if user_input in ("quit", "exit", "goodbye"):
            break
        else:
            handle_user_query(user_input)

        ask_continue = input("Do you want to ask anything else? (yes/no): ")
        if ask_continue.lower() != "yes":
            
            break

    print("\nThanks for using the hackbot! See you next time!!!")

if __name__ == "__main__":
    greet_user()
    print("Here are some commands you can use:")
    for command in commands:
        print(f"- {command}")

    while True:
        user_input = input("\nEnter a command or type 'quit' to exit: ")
        user_input = user_input.lower()
        if user_input == "quit":
            print("Thanks for using Hackbot!!!")
            break
        else: 
            run_chatbot(user_input)
import mysql.connector
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO

# Establish a connection to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="devesh@2004",
    database="hackbot_data"
)

# Create a cursor object to interact with the database
cursor = db_connection.cursor()

# Function to get the current time of the day
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

# Function to display greetings based on the time of the day
def greet_user():
    time_of_day = get_time_of_day()
    print(f"Hello! Good {time_of_day}! I'm Hackbot, your hackathon assistant. How can I help you today?")


def display_upcoming_hackathons(hackathons_data):
    """Displays a list of upcoming hackathons with essential details and images."""

    if not hackathons_data:
        print("There are no upcoming hackathons found in the database.")
        return

    print("\n**Here are the upcoming hackathons:**")

    for i, hackathon_data in enumerate(hackathons_data, start=1):
        print(f"\n**{i}. {hackathon_data[1]}**")
        print(f"Date: {hackathon_data[2]}")
        print(f"Location: {hackathon_data[4]}")
        print(f"Theme: {hackathon_data[5]}")

        try:
            image_url = hackathon_data[7]  # Assuming image URL is stored in column 7
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            image.show()  # Display the image
        except (IndexError, requests.exceptions.RequestException):
            pass  # Gracefully handle cases where image data is unavailable

    # Direct users to explore further
    print("\nFor more details about each hackathon, please ask for specific details or visit the registration link.")


def display_hackathon_details(hackathon_data):
    """Displays detailed information about a hackathon in a visually appealing format."""

    print("\n**Here are the details of the hackathon:**")

    # Display hackathon name prominently
    print(f"\n**Name:** {hackathon_data[1]}")

    # Display other details in a structured format
    print(f"**Date:** {hackathon_data[2]}")
    print(f"**Time:** {hackathon_data[3]}")
    print(f"**Location:** {hackathon_data[4]}")
    print(f"**Theme:** {hackathon_data[5]}")
    print(f"**Registration Link:** {hackathon_data[6]}")

    # Conditionally display an image if available
    try:
        image_url = hackathon_data[7]  # Assuming image URL is stored in column 7

        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image.show()  # Display the image
    except (IndexError, requests.exceptions.RequestException):
        pass  # Handle cases where image data is not available

    # Provide a clear call to action for registration
    print("\n**Register for the hackathon now to participate!**")


# Function to handle user queries
def handle_user_query(query):
    query = query.lower()  # Convert query to lowercase for easier matching

    # Define supported commands and their corresponding SQL queries
    commands = {
        "hackathon details": "SELECT * FROM hackathons ORDER BY date DESC LIMIT 1",
        "upcoming hackathons": "SELECT * FROM hackathons WHERE date >= CURDATE() ORDER BY date",
        "find hackathons by location": "SELECT * FROM hackathons WHERE location LIKE %s",  # Use parameterized query
        # ... add more commands as needed
    }

    try:
        if query in commands:
            cursor.execute(commands[query])
            results = cursor.fetchall()

            if results:
                # Process and display results in a user-friendly format
                if query == "hackathon details":
                    display_hackathon_details(results[0])
                elif query == "upcoming hackathons":
                    display_upcoming_hackathons(results)
                # ... handle other commands similarly
            else:
                print("No results found for that query.")
        else:
            print("Sorry, I don't understand that query. Please try one of the following commands:")
            for command in commands:
                print(f"- {command}")

    except mysql.connector.Error as err:
        print("An error occurred while accessing the database:", err)
        # Add more details as needed

# Function to display a gentle goodbye message
def say_goodbye():
    print("Thank you for using Hackbot. If you have any more questions, feel free to ask. Have a great day!")

# Main function to run the chatbot
def run_chatbot():
    greet_user()

    while True:
        user_input = input("You: ").lower()

        if user_input == "exit" or user_input == "bye":
            say_goodbye()
            break

        handle_user_query(user_input)

        another_query = input("Hackbot: Do you want to ask anything else? (yes/no): ").lower()
        if another_query != "yes":
            say_goodbye()
            break

# Main function to execute the chatbot
if __name__ == "__main__":
    run_chatbot()

# Close the database connection
cursor.close()
db_connection.close()

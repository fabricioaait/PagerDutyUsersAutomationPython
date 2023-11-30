import requests
import json

# Set your PagerDuty API token here
pagerduty_api_token = "YOUR_API_TOKEN"

# Define the PagerDuty API endpoint for deleting users
api_url = "https://api.pagerduty.com/users"

# Define the headers for the API request
headers = {
    "Accept": "application/vnd.pagerduty+json;version=2",
    "Authorization": f"Token token={pagerduty_api_token}",
}

# Read user data from the createdusers.json file
with open("createdusers.json", "r") as json_file:
    users_data = json.load(json_file)

# Iterate through the JSON data and delete users based on their IDs
for user_data in users_data:
    user_id = user_data.get("ID")

    if user_id:
        # Make an API request to delete the user by ID
        response = requests.delete(f"{api_url}/{user_id}", headers=headers)

        # Check if the user was successfully deleted
        if response.status_code == 204:
            print(f"User with ID {user_id} deleted successfully")
        else:
            print(f"Failed to delete user with ID {user_id}: {response.content.decode('utf-8')}")

print("User deletion complete.")

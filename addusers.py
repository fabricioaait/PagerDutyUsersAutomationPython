import requests
import csv
import json
import time

# Replace with your PagerDuty API token
api_token = 'YOUR_API_TOKEN'

# Define the PagerDuty API endpoint
base_url = 'https://api.pagerduty.com'

# Function to create a user and add their ID to the createdusers.json file
def create_user(user_data, team_id, created_users):
    user_payload = {
        "user": {
            "type": "user",
            "name": user_data["Name"],
            "email": user_data["Email"],
            "role": user_data["Role"],  # Add the "Role" field to the user payload
            "team_role": user_data["TeamRole"]  # Add the "TeamRole" field to the user payload
        }
    }
    
    response = requests.post(
        f'{base_url}/users',
        json=user_payload,
        headers={
            'Accept': 'application/vnd.pagerduty+json;version=2',
            'Authorization': f'Token token={api_token}'
        }
    )
    
    if response.status_code == 201:
        user_id = response.json()["user"]["id"]
        print(f"User '{user_data['Name']}' created with ID: {user_id}")
        
        # Update the user entry with CountryCode and Phone values
        user_entry = {
            "ID": user_id,
            "Name": user_data["Name"],
            "Email": user_data["Email"],
            "Team": team_id,
            "CountryCode": user_data.get("CountryCode"),  # Get CountryCode from user_data
            "Phone": user_data.get("Phone"),  # Get Phone from user_data
            "Role": user_data["Role"],  # Add the "Role" field to the user entry
            "TeamRole": user_data["TeamRole"]  # Add the "TeamRole" field to the user entry
        }
        
        created_users.append(user_entry)
    elif response.status_code == 429:
        # Rate limit exceeded, wait and retry
        retry_after = int(response.headers.get('Retry-After', 10))  # Default to 10 seconds if Retry-After is not present
        print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)
        create_user(user_data, team_id, created_users)
    else:
        print(f"Failed to create user '{user_data['Name']}': {response.status_code} - {response.text}")

# Read users.csv and createdteams.json
with open('createdteams.json', 'r') as jsonfile:
    created_teams = json.load(jsonfile)

created_users = []

with open('users.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        team_name = row["Team"]
        
        if team_name in created_teams:
            team_id = created_teams[team_name]
            create_user(row, team_id, created_users)

# Write the created users to createdusers.json
with open('createdusers.json', 'w') as outfile:
    json.dump(created_users, outfile, indent=4)

print("User creation and JSON file writing completed.")

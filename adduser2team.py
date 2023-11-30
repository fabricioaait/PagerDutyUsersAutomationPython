import requests
import json

# Replace with your PagerDuty API token
api_token = 'YOUR_API_TOKEN'

# Define the PagerDuty API endpoint
base_url = 'https://api.pagerduty.com'

# Default role to assign when "TeamRole" is not specified in createdusers.json
default_role = "user"

# Function to assign a user to a team with the specified role or default role
def assign_user_to_team(team_id, user_id, role):
    payload = {
        "role": role
    }
    
    response = requests.put(
        f'{base_url}/teams/{team_id}/users/{user_id}',
        json=payload,
        headers={
            'Accept': 'application/json',
            'Authorization': f'Token token={api_token}',
            'Content-Type': 'application/json'
        }
    )
    
    if response.status_code == 204:
        print(f"User '{user_id}' added to team '{team_id}' with role '{role}'")
    else:
        print(f"Failed to add user '{user_id}' to team '{team_id}': {response.status_code} - {response.text}")

# Read createdusers.json to get user data
with open('createdusers.json', 'r') as users_file:
    users_data = json.load(users_file)
    
    for user_data in users_data:
        team_id = user_data["Team"]
        user_id = user_data["ID"]
        role = user_data.get("TeamRole", default_role)  # Use default role if "TeamRole" is not specified
        
        assign_user_to_team(team_id, user_id, role)

print("User assignment to teams completed.")

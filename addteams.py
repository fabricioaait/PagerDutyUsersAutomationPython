import requests
import csv
import json

# Replace with your PagerDuty API token
api_token = 'YOUR_API_TOKEN'

# Define the PagerDuty API endpoint
base_url = 'https://api.pagerduty.com'

# Function to create a team if it doesn't exist
def create_team_if_not_exists(team_name):
    team_payload = {
        "team": {
            "type": "team",
            "name": team_name
        }
    }

    response = requests.post(
        f'{base_url}/teams',
        json=team_payload,
        headers={
            'Accept': 'application/vnd.pagerduty+json;version=2',
            'Authorization': f'Token token={api_token}'
        }
    )

    if response.status_code == 201:
        team_id = response.json()['team']['id']
        print(f"Team '{team_name}' created with ID: {team_id}")
        return team_id
    elif response.status_code == 400 and "Name has already been taken" in response.text:
        # Team already exists, retrieve its ID
        response_data = response.json()
        team_id = response_data["team"]["id"]
        print(f"Team '{team_name}' already exists with ID: {team_id}")
        return team_id
    else:
        print(f"Failed to create team '{team_name}': {response.status_code} - {response.text}")
        return None

# Read users.csv and extract unique team names
unique_team_names = set()
with open('users.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        team_name = row.get("Team")
        if team_name:
            unique_team_names.add(team_name)

# Create teams based on unique team names and save IDs to 'createdteams' file
created_team_ids = {}
for team_name in unique_team_names:
    team_id = create_team_if_not_exists(team_name)
    if team_id:
        created_team_ids[team_name] = team_id

# Save the created team IDs to 'createdteams.json' file
with open('createdteams.json', 'w') as outfile:
    json.dump(created_team_ids, outfile)

print("Team creation completed.")

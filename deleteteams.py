import requests
import json

# Replace with your PagerDuty API token
api_token = 'YOUR_API_TOKEN'

# Define the PagerDuty API endpoint
base_url = 'https://api.pagerduty.com'

# Function to delete a team by its ID
def delete_team(team_id):
    response = requests.delete(
        f'{base_url}/teams/{team_id}',
        headers={
            'Accept': 'application/vnd.pagerduty+json;version=2',
            'Authorization': f'Token token={api_token}'
        }
    )

    if response.status_code == 204:
        print(f"Team with ID: {team_id} deleted successfully.")
    elif response.status_code == 404:
        print(f"Team with ID: {team_id} not found.")
    else:
        print(f"Failed to delete team with ID {team_id}: {response.status_code} - {response.text}")

# Load the created team IDs from 'createdteams.json' file
try:
    with open('createdteams.json', 'r') as infile:
        created_team_ids = json.load(infile)
except FileNotFoundError:
    print("No 'createdteams.json' file found. No teams to delete.")
    created_team_ids = {}

# Delete each team based on its ID
for team_name, team_id in created_team_ids.items():
    delete_team(team_id)

print("Team deletion completed.")

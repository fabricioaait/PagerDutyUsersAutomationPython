import requests
import json

# Replace with your PagerDuty API token
api_token = 'YOUR_API_TOKEN'

# Define the PagerDuty API endpoint
base_url = 'https://api.pagerduty.com'

# Read user IDs, country codes, and phone numbers from createdusers.json
with open('createdusers.json', 'r') as jsonfile:
    created_users = json.load(jsonfile)

if created_users:
    for user_data in created_users:
        user_id = user_data.get("ID")
        country_code = user_data.get("CountryCode")
        phone_number = user_data.get("Phone")

        if user_id and country_code and phone_number:
            # Define the phone contact method payload with the extracted data
            phone_contact_payload = {
                "contact_method": {
                    "type": "phone_contact_method",
                    "country_code": int(country_code),
                    "address": phone_number,
                    "label": "Phone",
                    "blacklisted": False,
                    "enabled": True
                }
            }

            # Make a POST request to update the phone contact method
            response = requests.post(
                f'{base_url}/users/{user_id}/contact_methods',
                json=phone_contact_payload,
                headers={
                    'Accept': 'application/vnd.pagerduty+json;version=2',
                    'Authorization': f'Token token={api_token}'
                }
            )

            if response.status_code == 201:
                print(f"Phone contact method added for user with ID: {user_id}")
            else:
                print(f"Failed to add phone contact method for user with ID {user_id}: {response.status_code} - {response.text}")
else:
    print("No users found in createdusers.json.")

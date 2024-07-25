
import json
from Scripts.auth import renew_api
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError
import requests
import oauthlib.oauth2.rfc6749.errors
import os
import json
import Scripts.auth.config as config

client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
access_token_url = config.access_token_url
redirect_uri = config.redirect_uri
authorization_base_url = config.authorization_base_url


headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-subdomain": config.rms_subdomain
    }

# Function to save token to a file
def save_token(token, file_path):
    with open(file_path, "w") as f:
        json.dump(token, f)

# Function to load token from a file
def load_token(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Construct the absolute path to access_token.json
dir_path = os.path.dirname(os.path.realpath(__file__))
access_token_file_path = os.path.join(dir_path, "access_token.json")

# Load the access token from a file
access_token = load_token(access_token_file_path)

# Set up the OAuth session with the stored access token
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, token=access_token)


# Function to refresh the token
def refresh_token(oauth, refresh_token_file_path):
    refresh_token = load_token(refresh_token_file_path)["refresh_token"]
    extra = {
        'client_id': client_id,
        'client_secret': client_secret,
    }
    new_token = oauth.refresh_token(access_token_url, refresh_token=refresh_token, **extra)
    save_token(new_token, access_token_file_path)
    return new_token

#List opportunity items
url1 = "https://api.current-rms.com/api/v1/opportunities"
# Try a request to the API using the access token
try:
    response = oauth.get(url1, headers=headers)
    response.raise_for_status()
    # Write the response to a file
    with open("response.json", "w") as f:
        f.write(json.dumps(response.json()))

except TokenExpiredError:
    print("Access token expired, refreshing token")
    # Refresh the token
    new_token = refresh_token(oauth, access_token_file_path)
    # Update the OAuth session with the new token
    oauth.token = new_token
    # Retry the request with the new token
    response = oauth.get(url1, headers=headers)
    response.raise_for_status()
    # Write the response to a file
    with open("response.json", "w") as f:
        f.write(json.dumps(response.json()))

except Exception as e:
    print(f"An error occurred: {e}")


# def start_oauth_session(client_id, client_secret,  redirect_uri, access_token_url, headers):

#     #List opportunity items
#     url1 = "https://api.current-rms.com/api/v1/opportunities"

    
#     # Construct the absolute path to access_token.json
#     access_token_file_path = os.path.join(dir_path, "access_token.json")

#     #read the access token from a file
#     with open(access_token_file_path, "r") as f:
#         access_token = json.loads(f.read())

#     #create a dictionary of the access token
#     access_token = {"access_token": access_token}


#     #set up the oauth session with stored access token
#     oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, token=access_token)   
#     #try a request to the API using the access token
#     try:
#         response = oauth.get(url1, headers=headers)
#         #check the response status code and raise an error if it is not successful (in the 200 range)
#         #write the access token to a text file
#         with open("response.json", "w") as f:
#             f.write(json.dumps(response.json())) 
  
#         response.raise_for_status()

#     #if the access token has expired, use the refresh token to get a new token
#     except TokenExpiredError:

#         print("Access token expired, refreshing token")
#         # Construct the absolute path to refresh_token.txt
#         refresh_token_file_path = os.path.join(dir_path, "refresh_token.txt")

#         # Read the refresh token from a file
#         with open(refresh_token_file_path, "r") as f:
#             refresh_token = f.read().strip()
#         print(f"refresh token: {refresh_token}")
#         try:
#             new_token = oauth.refresh_token(token_url=access_token_url, refresh_token=refresh_token, client_secret=client_secret)
#             access_token = new_token['access_token']



#         except requests.exceptions.HTTPError as e:
#             print(f"Failed to refresh token, HTTP error: {e.response.status_code}")
#             # Handle specific cases or re-raise the error
#         except oauthlib.oauth2.rfc6749.errors.InvalidGrantError as e:
#             print("Failed to refresh token, invalid grant: ", e.description)
#             # Call get_access_token() from renew_api.py here
#             new_access_token = renew_api.get_access_token()
#             if new_access_token:
#             # Update the OAuth session with the new access token
#                 oauth.token = {'access_token': new_access_token}
#                 print("Successfully retrieved a new access token.")
                
#             else:
#                 print("Failed to retrieve a new access token.")
#     print('oauth session started')
#     return oauth

# start_oauth_session(client_id, client_secret,  redirect_uri, access_token_url, headers)
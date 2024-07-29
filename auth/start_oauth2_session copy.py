
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

# # Debugging: Print configuration values
# print("Client ID:", client_id)
# print("Client Secret:", client_secret)
# print("Access Token URL:", access_token_url)
# print("Redirect URI:", redirect_uri)
# print("Authorization Base URL:", authorization_base_url)



# # Function to save token to a file
# def save_token(token, file_path):
#     with open(file_path, "w") as f:
#         json.dump(token, f)

# # Function to load token from a file
# def load_token(file_path):
#     with open(file_path, "r") as f:
#         return json.load(f)

# # Construct the absolute path to access_token.json
# dir_path = os.path.dirname(os.path.realpath(__file__))
# token_path = os.path.join(dir_path, "access_token.json")

# # Debugging: Print token path
# print("Token Path:", token_path)

# # Load or create OAuth2 session
# def create_oauth2_session():
#     try:
#         token = load_token(token_path)
#         # Debugging: Print loaded token
#         print("Loaded Token:", token)
#         oauth2_session = OAuth2Session(client_id, token=token)
#     except FileNotFoundError:
#         oauth2_session = OAuth2Session(client_id, redirect_uri=redirect_uri, token=token)
#         authorization_url, state = oauth2_session.authorization_url(authorization_base_url)
#         print("Please go to {} and authorize access.".format(authorization_url))
#         authorization_response = input("Enter the full callback URL: ")
#         token = oauth2_session.fetch_token(access_token_url, authorization_response=authorization_response, client_secret=client_secret)
#         save_token(token, token_path)
#     except json.JSONDecodeError:
#         print("Error decoding the token file.")
#         return None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
#     return oauth2_session

# # Create OAuth2 session
# oauth2_session = create_oauth2_session()
# print(oauth2_session)

# if oauth2_session:
#     # Example API request
#     try:
#         response = oauth2_session.get("https://heinlattaung7.current-rms.com/products", headers=headers)
#         print(response.json())
#     except TokenExpiredError:
#         print("Token has expired. Please re-authenticate.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
# else:
#     print("Failed to create OAuth2 session.")


def start_oauth_session(client_id, client_secret,  redirect_uri, access_token_url, headers):

    #List opportunity items
    url1 = "https://api.current-rms.com/api/v1/opportunities"

    
    # Construct the absolute path to access_token.json
    access_token_file_path = os.path.join(dir_path, "access_token.json")

    #read the access token from a file
    with open(access_token_file_path, "r") as f:
        access_token = json.loads(f.read())

    #create a dictionary of the access token
    access_token = {"access_token": access_token}


    #set up the oauth session with stored access token
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, token=access_token)   
    #try a request to the API using the access token
    try:
        response = oauth.get(url1, headers=headers)
        #check the response status code and raise an error if it is not successful (in the 200 range)
        #write the access token to a text file
        with open("response.json", "w") as f:
            f.write(json.dumps(response.json())) 
  
        response.raise_for_status()

    #if the access token has expired, use the refresh token to get a new token
    except TokenExpiredError:

        print("Access token expired, refreshing token")
        # Construct the absolute path to refresh_token.txt
        refresh_token_file_path = os.path.join(dir_path, "refresh_token.txt")

        # Read the refresh token from a file
        with open(refresh_token_file_path, "r") as f:
            refresh_token = f.read().strip()
        print(f"refresh token: {refresh_token}")
        try:
            new_token = oauth.refresh_token(token_url=access_token_url, refresh_token=refresh_token, client_secret=client_secret)
            access_token = new_token['access_token']



        except requests.exceptions.HTTPError as e:
            print(f"Failed to refresh token, HTTP error: {e.response.status_code}")
            # Handle specific cases or re-raise the error
        except oauthlib.oauth2.rfc6749.errors.InvalidGrantError as e:
            print("Failed to refresh token, invalid grant: ", e.description)
            # Call get_access_token() from renew_api.py here
            new_access_token = renew_api.get_access_token()
            if new_access_token:
            # Update the OAuth session with the new access token
                oauth.token = {'access_token': new_access_token}
                print("Successfully retrieved a new access token.")
                
            else:
                print("Failed to retrieve a new access token.")
    print('oauth session started')
    return oauth

start_oauth_session(client_id, client_secret,  redirect_uri, access_token_url, headers)
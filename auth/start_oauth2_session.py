
import json
from Scripts.auth import renew_api
from requests_oauthlib import OAuth2Session
import requests
import oauthlib.oauth2.rfc6749.errors
import os
import json

# Get the directory of the current script
dir_path = os.path.dirname(os.path.realpath(__file__))


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
        response.raise_for_status()

    #if the access token has expired, use the refresh token to get a new token
    except:

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


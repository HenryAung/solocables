#this is an oath application for connecting to the curent-rms API

from requests_oauthlib import OAuth2Session
import json
import Scripts.auth.config as config
import os

client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
access_token_url = config.access_token_url
redirect_uri = config.redirect_uri
authorization_base_url = config.authorization_base_url

# Get the directory of the current script
dir_path = os.path.dirname(os.path.realpath(__file__))

def get_access_token():
    #set up the oauth session
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)

    #print the authorization url
    authorization_url, state = oauth.authorization_url(authorization_base_url)
    print("Please go here and authorize,", authorization_url)

    # get the authorization verifier code from the callback url
    redirect_response = input("Paste the full redirect URL here:")

    # fetch the access token
    token = oauth.fetch_token(token_url=access_token_url, authorization_response=redirect_response, client_secret=client_secret)
    access_token_json_file_path = os.path.join(dir_path, "access_token.json")
    access_token_txt_file_path = os.path.join(dir_path, "access_token.txt")
    #write the access token to a file as json
    with open(access_token_json_file_path, "w") as f:
        f.write(json.dumps(token['access_token']))

    #write the access token to a text file
    with open(access_token_txt_file_path, "w") as f:
        f.write(token['access_token'])

    # fetch the refresh token
    # Using the [] operator
    try:
        refresh_token = token['refresh_token']
    except KeyError:
        refresh_token = None

    #write the refresh token to a file
    refresh_token_file_path = os.path.join(dir_path, "refresh_token.txt")
    with open(refresh_token_file_path, "w") as f:
        f.write(refresh_token)

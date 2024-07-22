from requests_oauthlib import OAuth2Session
import config
import json

def start_oauth_session(client_id, client_secret, redirect_uri, headers):

    #List opportunity items
    url1 = "https://api.current-rms.com/api/v1/opportunities/1"

    #read the access token from a file
    with open("access_token.json", "r") as f:
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
        print(response)

    #if the access token has expired, use the refresh token to get a new token
    except:

        print("Access token expired, refreshing token")

        # read the refresh token from a file
        with open("refresh_token.txt", "r") as f:
            refresh_token = f.read()

        token = oauth.refresh_token(token_url=access_token_url, refresh_token=refresh_token, client_secret=client_secret)
        access_token = token['access_token']

    #write the access token to a file as json
        with open("access_token.json", "w") as f:
            f.write(json.dumps(token['access_token']))
    print('oauth session started')
    return oauth

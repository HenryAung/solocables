
import json
import renew_api
from requests_oauthlib import OAuth2Session


def start_oauth_session(client_id, client_secret,  redirect_uri, access_token_url, headers):

    #List opportunity items
    url1 = "https://api.current-rms.com/api/v1/opportunities"

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

    #if the access token has expired, use the refresh token to get a new token
    except:

        print("Access token expired, refreshing token")

        # Read the refresh token from a file
        with open("refresh_token.txt", "r") as f:
            refresh_token = f.read().strip()
        print(f"refresh token: {refresh_token}")
        try:
            new_token = oauth.refresh_token(token_url=access_token_url, refresh_token=refresh_token, client_secret=client_secret)
            access_token = new_token['access_token']

        # except :

        #     renew_api.get_access_token()
        #     with open("access_token.json", "r") as f:
        #         access_token = json.loads(f.read())
        #     access_token = {"access_token": access_token}
        #     oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, token=access_token)

        except requests.exceptions.HTTPError as e:
            print(f"Failed to refresh token, HTTP error: {e.response.status_code}")
            # Handle specific cases or re-raise the error
        except oauthlib.oauth2.rfc6749.errors.InvalidGrantError as e:
            print("Failed to refresh token, invalid grant: ", e.description)
            # Additional handling like re-authenticationid, redirect_uri=redirect_uri, token=new_token)
    print('oauth session started')
    return oauth

# def main():
#     start_oauth_session(client_id, client_secret,  redirect_uri, access_token_url, headers)
#     pass
  
# if __name__ == "__main__":
#     main()

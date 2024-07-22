from requests_oauthlib import OAuth2Session
import config
import json
import start_oauth2_session
import renew_api

client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
access_token_url = config.access_token_url
redirect_uri = config.redirect_uri
authorization_base_url = config.authorization_base_url


#List opportunity items
opportunities_url = "https://api.current-rms.com/api/v1/opportunities"

#Add an item to an opportunity
job_url = "https://api.current-rms.com/api/v1/opportunities/1"

#update an opportunity item
products_url = "https://api.current-rms.com/api/v1/products"


headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "x-subdomain": config.rms_subdomain
}



def main():
    oauth = start_oauth2_session.start_oauth_session(client_id, client_secret,  redirect_uri, access_token_url, headers)
    response = oauth.get(products_url, headers=headers)
    formatted_json = json.dumps(response.json(), indent=8)  # Format the JSON content
    print(f"Test response in JSON format:\n{formatted_json}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
from requests_oauthlib import OAuth2Session
import config
import start_oauth2_session
import pandas as pd
import json

# Set pandas option to display all sequence items
pd.set_option('display.max_seq_items', None)

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

def get_all_opportunities():
    oauth = start_oauth2_session.start_oauth_session(client_id, client_secret,  redirect_uri, access_token_url, headers)
    opportunities_url = "https://api.current-rms.com/api/v1/opportunities"
    response = oauth.get(opportunities_url, headers=headers)
    return response.json()



def fetch_all_products():
    oauth = start_oauth2_session.start_oauth_session(client_id, client_secret,  redirect_uri, access_token_url, headers)
    base_url = "https://api.current-rms.com/api/v1/products"
    all_products = []
    page = 1
    per_page = 20  # Adjust based on the API's maximum allowed value

    while True:
        # Construct the URL with proper query parameters for pagination and sorting
        url = f"{base_url}?page={page}&per_page={per_page}&filtermode=all&sort=id"
        
        response = oauth.get(url, headers=headers)
        
        data = response.json()
        products = data.get('products', [])
        all_products.extend(products)

        if not products or len(products) < per_page:
            break  # Exit loop if no more products or less than per_page products are returned

        page += 1  # Increment page number for the next iteration

    df = pd.json_normalize(all_products)
    print("All Items")
    print(df)
 
    return df


def get_job_items(job_id):
    oauth = start_oauth2_session.start_oauth_session(client_id, client_secret,  redirect_uri, access_token_url, headers)
    opportunities_url = "https://api.current-rms.com/api/v1/opportunities"
    
    response = oauth.get(opportunities_url+ '/' + str(job_id)  + '/' + 'opportunity_items', headers=headers)
    
    # Convert the response to a Python dictionary 
    opportunity_items = response.json()['opportunity_items']

    # Filter items where item_type is "Product"
    product_items = [item for item in opportunity_items if item['item_type'] == "Product"]


    df = pd.json_normalize(product_items)
    df = df[['item_id', 'name', 'quantity', 'description']]
    df.rename(columns={'item_id': 'Id'}, inplace=True)
    print("Job Items")
    print(df)
    return df




def main():

    # get_job_items(1)
    pass

if __name__ == "__main__":
    main()

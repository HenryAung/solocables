import pandas as pd
import os

import Scripts.auth.config as config
from APIs import apiCall
from auth import start_oauth2_session, renew_api
from data_processing import processData
from Scripts.databases import dbQueries
from Scripts.databases import tagDbQueries
import turntable_checker



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



def job_function_display_options():
    print("  ")
    print(" ******                ********  ")
    print("Job has been loaded!")
    print("  ")
    print("1. Look all items in the job")
    print("2. Look products that need power cables")
    print("3. Look all cables in the job")
    print("4. Check cables")
    print("5. Analyze the job")
    print("6. Exit")

    choice = input("Enter your choice (1-5): ")
    return choice



def job_function_controller(job_from_api, database, column_name_to_match, oauth, headers, conn):
        
    while True:

        job_display_choise = job_function_display_options()

        choice = job_function_display_options
        
        if job_display_choise == '1':
            print(job_from_api)
            
        elif job_display_choise == '2':            
            if job_from_api is not None:
                product_with_power = processData.get_product_with_power_from_job(job_from_api, database,column_name_to_match )
                    # Print the filtered DataFrame
                print("")
                print("")
                print("\nProducts requiring mains power:")
                print(product_with_power)
                print("")
                print("")

        elif job_display_choise == '3':
            if job_from_api is not None:

                cables_from_job = processData.get_cables_from_job(job_from_api, database,column_name_to_match)
                    # Print the filtered DataFrame
                print("")
                print("")
                print("\nCables in current job:")
                print(cables_from_job)
                print("")
                print("")

        elif job_display_choise == '4':
            if job_from_api is not None:
                print("")
                print("")
                processData.check_cables(job_from_api, database,column_name_to_match )
                print("")
                print("")

        elif job_display_choise == '5':
            if job_from_api is not None:
                print("")
                print("")
                turntable_checker.check_for_turnable(job_from_api, conn)
                print("")
                print("")
        
        elif job_display_choise == '6' : 
            print("Exiting the application.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


def main_menu_display_options():
    print("  ")
    print(" ******                ********  ")
    print("Welcome to the Cable Checker application!")
    print("  ")
    print("1. Go to the specific job opportunity and explore ...")
    print("2. Update product database")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ")
    return choice

def main():
    

    base_dir = os.path.dirname(os.path.abspath(__file__))
    database_file_path = os.path.join( base_dir, './databases/business_automation.db')
    conn = dbQueries.create_connection(database_file_path)

    database = dbQueries.select_all_products(conn)

    database = pd.DataFrame(database, columns=['id_dev', 'id_live', 'name', 'description', 'mainsPowerReq', 'powerType', 'prefPwrCbl', 'isCable', 'cblLeng', 'connector1', 'connector2', 'prefPwrCbl_dev'])
    
    oauth = start_oauth2_session.start_oauth_session(client_id, client_secret, redirect_uri, access_token_url, headers)
    
    database['Id'] = database['id_dev'].copy()
   
    column_name_to_match = 'Id' 


    while True:
        choice = main_menu_display_options()
        
        if choice == '1':
            job_Id = input("Please enter the job Id: ")

            job_from_api = apiCall.get_job_items(job_Id, oauth, headers)

            job_function_controller(job_from_api, database, column_name_to_match, oauth, headers, conn)


        elif choice == '2':
            file_name = input("Please enter the file name for the new product database (e.g., new_product_database.csv): ")
            new_database_path = os.path.join(base_dir, '../databases', file_name)

            if not os.path.exists(new_database_path):
                print("The file does not exist.")
            else:
                processData.update_database(database_file_path, new_database_path)
                print(" ")
                print(" ")
                print("Database updated successfully.")

       
        elif choice == '3' : 
            print("Exiting the application.")
            break


        else:
            print("Invalid choice. Please enter a number between 1 and 4.")



if __name__ == "__main__":
    main()

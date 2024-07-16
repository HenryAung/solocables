import pandas as pd
import argparse
import os

def read_product_file(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except PermissionError as e:
        print(f"Permission denied: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


def display_options():
    print("  ")
    print(" ******                ********  ")
    print("  ")
    print("Products list file has been loaded ")
    print("1. Display all product data")
    print("2. Load and merge all products for specific job")
    print("3. Check cables for specific job")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")
    return choice

def match_data(df_product, df_to_match, column_name):
    """Match data from df_to_match against df_product."""
    
    if column_name not in df_product.columns and column_name not in df_to_match.columns:
        print(f"Column '{column_name}' does not exist in one of the DataFrames.")
        return None

    matched_df = pd.merge(df_to_match, df_product, on=column_name, how='left')
    return matched_df
   
def get_product_with_power_from_job(df_product, df_to_match, column_name): 
    # Select relevant columns
    relevant_columns = ['name', 'powerType', 'mainsPowerReq', 'Product Group', 'quantity']
    matched_df = match_data(df_product, df_to_match, df_to_match)
    filtered_matched_df = matched_df[relevant_columns]

    # Filter for products requiring mains power
    products_with_power = filtered_matched_df[filtered_matched_df['mainsPowerReq'] == 'Yes']

    return products_with_power

def get_all_cables(df_product): 

    cableGroup = ['Power Cable and Distribution - 13A', 
              'Power Cable and Distribution - 16A', 
              'Power Cable and Distribution - 32A', 
              'Power Cable and Distribution - 63A',
              'Power Cable and Distribution - Circuit Protection', 
              'Power Cable and Distribution - Adapters', 
              'Combi Cables', 
              'Power Cable and Distribution - Power Distribution',
              'Power Cable and Distribution - IEC C*',
              'Power Cable and Distribution - Powercon',
              'Power Cable and Distribution - Truecon'
              ]

    # Filter out rows where 'product_group' is in cableGroup
    all_cables = df_product[df_product['Product Group'].isin(cableGroup)]
    all_cables = all_cables[['Id', 'name', 'Product Group']]
  

    return all_cables

def get_cables_from_job(df_product, job_items, column_name):

    all_cables = get_all_cables(df_product)
    merged_df = match_data(df_product, job_items, column_name)

    cables_from_job = merged_df[merged_df['Id'].isin(all_cables['Id'])]
    cables_from_job  = cables_from_job[['Id', 'name', 'quantity']]
    cables_from_job = cables_from_job.groupby('name').sum()
    cables_from_job

    return cables_from_job



def check_cables(df_product, df_to_match, column_name):
    """
    Match data from df_to_match against df_product based on a specific column.
    Prints products requiring mains power and their power type counts.
    
    Parameters:
    - df_product: DataFrame containing product information.
    - df_to_match: DataFrame to match against df_product.
    - column_name: The name of the column to match on.
    
    Returns:
    - DataFrame of matched products requiring mains power.
    """
   

    # Filter for products requiring mains power
    products_with_power = match_data(df_product, df_to_match,column_name )

    # Calculate and print power type counts
    powerType_counts = products_with_power.groupby('powerType')['quantity'].sum().reset_index()
    print("\nPower Type Counts needed:")
    print(powerType_counts)

    cables_from_job = get_cables_from_job(df_product, df_to_match, column_name)

    print("\nCables in current job:")
    print(cables_from_job)

    return products_with_power



def main():
   

    df_product = read_product_file("C:/Users/heinl/Desktop/csv_download/Current-Product-20240709-17597-vhy5tu.csv")
    df_product.rename(columns={'Name': 'name'}, inplace=True)
    df_product = df_product[['Id', 'name', 'powerType', 'mainsPowerReq', 'Product Group']]


    job_items = read_product_file("C:/Users/heinl/Desktop/csv_download/Wedding_Grove_House_Roehampton.csv")
    column_name_to_match = 'name'

    

    if df_product is None:
        return

    while True:
        choice = display_options()
        if choice == '1':
            print("\n************************************")
            print("************************************")
            print(df_product)
            print("\n************************************")
            print("************************************")
            

        elif choice == '2':            
            if job_items is not None:
                product_with_power = match_data(df_product, job_items,column_name_to_match )
                    # Print the filtered DataFrame
                print("\n************************************")
                print("************************************")
                print("\nProducts requiring mains power:")
                print(product_with_power)
                print("\n************************************")
                print("************************************")
        elif choice == '3':
            if job_items is not None:
                print("\n************************************")
                print("************************************")
                check_cables(df_product, job_items,column_name_to_match )
                print("\n************************************")
                print("************************************")
                
       
        
        elif choice == '4' : 
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()

import pandas as pd

pd.set_option('display.max_seq_items', None)


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
   

def get_product_with_power_from_job(job_items, database, column_name): 
    # Select relevant columns
    relevant_columns = ['Id', 'Name_x', 'quantity', 'Description_x', 'Product Group', 'mainsPowerReq', 'powerType', 'prefPwrCbl_dev', 'prefPwrCbl']
    matched_df = pd.merge(job_items, database, on=column_name, how='left')
    filtered_matched_df = matched_df[relevant_columns]
    filtered_matched_df.rename(columns={'Name_x': 'Name', 'Description_x': 'Description'}, inplace=True)
    

    # Filter for products requiring mains power
    products_with_power = filtered_matched_df[filtered_matched_df['mainsPowerReq'] == 'Yes']

    return products_with_power


def get_all_cables(database): 

    # cableGroup = ['Power Cable and Distribution - 13A', 
    #           'Power Cable and Distribution - 16A', 
    #           'Power Cable and Distribution - 32A', 
    #           'Power Cable and Distribution - 63A',
    #           'Power Cable and Distribution - Circuit Protection', 
    #           'Power Cable and Distribution - Adapters', 
    #           'Combi Cables', 
    #           'Power Cable and Distribution - Power Distribution',
    #           'Power Cable and Distribution - IEC C*',
    #           'Power Cable and Distribution - Powercon',
    #           'Power Cable and Distribution - Truecon'
    #           ]

    # # Filter out rows where 'product_group' is in cableGroup
    # all_cables = database[database['Product Group'].isin(cableGroup)]
    all_cables = database[database['isCable'] == 'yes']

    all_cables = all_cables[['Id', 'Name', 'Product Group', 'connector1', 'connector2', 'cblLeng']]
    all_cables['cblLeng'] = pd.to_numeric(all_cables['cblLeng'], errors='coerce')

    all_cables = database[database['isCable'] == 'yes']
  
    return all_cables


def get_cables_from_job(job_items, database, column_name):

    all_cables = get_all_cables(database)
    matched_df = pd.merge(job_items, database, on=column_name, how='left')

    cables_from_job = matched_df[matched_df['Id'].isin(all_cables['Id'])]
    cables_from_job.rename(columns={'Name_x': 'Name', 'Description_x': 'Description'}, inplace=True)
    cables_from_job  = cables_from_job[['Id', 'Name', 'quantity', 'connector1' , 'connector2', 'cblLeng']]
    cables_from_job['quantity'] = pd.to_numeric(cables_from_job['quantity'], errors='coerce')
    cables_from_job = cables_from_job.groupby(['Id', 'Name', 'connector1', 'connector2', 'cblLeng'])['quantity'].sum().reset_index().sort_values('cblLeng', ascending=False)
    cables_from_job['Id'] = pd.to_numeric(cables_from_job['Id'], errors='coerce')
    
    # print("\nCables in current job:")
    # print(cables_from_job)

    return cables_from_job


def preffered_cable_counts(job_items, database,column_name ):
    cables = get_all_cables(database)

    # Filter for products requiring mains power
    products_with_power = get_product_with_power_from_job(job_items, database,column_name )
  
     # Convert 'quantity' column to numeric (float or int)
    products_with_power['quantity'] = pd.to_numeric(products_with_power['quantity'], errors='coerce')

     # Calculate and print power type counts
    prefered_cable_counts = products_with_power.groupby('prefPwrCbl_dev')['quantity'].sum().reset_index()
    
    # Merge prefered_cable_counts with cables on 'prefPwrCbl' and 'name' respectively
    prefered_cable = pd.merge(prefered_cable_counts, cables, left_on='prefPwrCbl_dev', right_on='Id', how='left')
    
      # Select desired columns and rename 'quantity_x' to 'quantity'
    prefferred_cable = prefered_cable[['Id', 'Name', 'connector1', 'connector2', 'cblLeng', 'quantity' ]].sort_values('cblLeng', ascending=False)
    print("\nTotal Minimum Preffered Cables:")
    print(prefferred_cable)

    return prefferred_cable

def compare_cables(cables_from_job, preffered_cable):
    compare_merged = pd.merge(cables_from_job, preffered_cable, on='Id', how='outer', suffixes=('_job', '_prefferred'))
    compare_merged['quantity_job'] = pd.to_numeric(compare_merged['quantity_job'], errors='coerce')

    # Fill missing values in quantity columns with 0
    compare_merged['quantity_job'] = compare_merged['quantity_job'].fillna(0)
    compare_merged['quantity_prefferred'] = compare_merged['quantity_prefferred'].fillna(0)

    # Calculate the difference between job and preferred quantities
    compare_merged['difference'] = compare_merged['quantity_job'] - compare_merged['quantity_prefferred']
    print("  ")
    print(" ******          ********  ")

    # Categorize the differences
    compare_merged['comparison'] = compare_merged['difference'].apply(lambda x: 'Less' if x < 0 else ('More' if x > 0 else 'Equal'))

    return compare_merged

def suggestions_for_cables(compare_merged):# Suggest cables to add or remove
    
    #listing out all extra cables in job
    job_cables_to_sub = compare_merged[compare_merged['comparison'] == 'More'].sort_values('cblLeng_prefferred', ascending=False)
    job_cables_to_sub = job_cables_to_sub.drop(['connector1_prefferred', 'connector2_prefferred', 'quantity_prefferred', 'cblLeng_prefferred'], axis=1)

    print("Extra Cables in job before substituting:")
    for index, row in job_cables_to_sub.iterrows():
        print(f"{int(row['difference'])} x {row['Name_job']}")
    print("  ")
    print("  ")


    #listing out all preffered cables not match with extra cable
    needed_preffered_cables = compare_merged[compare_merged['comparison'] == 'Less'].sort_values('cblLeng_prefferred', ascending=False)
    needed_preffered_cables = compare_merged[compare_merged['comparison'].isin(['Less'])].sort_values('cblLeng_prefferred', ascending=False)
    needed_preffered_cables = needed_preffered_cables.drop(['connector1_job', 'connector2_job', 'quantity_job', 'cblLeng_job'], axis=1)
    needed_preffered_cables['difference'] = needed_preffered_cables['difference'].abs()

    print ("  ")
    print ("  ")
    print("Preffered cables not match with extra cable before substituting  :")
    for index, row in needed_preffered_cables.iterrows():
        print(f"     {int(row['difference'])} x {row['Name_prefferred']}")
    print("  ")
    print("  ")
        

    #swaping the cables from job to preffered cables
    subtracted_items = []

    # Process the preferred items to update the job items
    total_subtracted = 0

    for p_index, p_row in needed_preffered_cables.iterrows():
        p_connector1 = p_row['connector1_prefferred']
        p_connector2 = p_row['connector2_prefferred']
        p_difference = p_row['difference']

        for j_index, j_row in job_cables_to_sub.iterrows():
            if p_connector1 == j_row['connector1_job'] and p_connector2 == j_row['connector2_job']:
                j_difference = j_row['difference']
                if j_difference >= p_difference:
                    job_cables_to_sub.at[j_index, 'difference'] -= p_difference
                    needed_preffered_cables.at[p_index, 'difference'] = 0
                    subtracted_items.append((p_row['Name_prefferred'], j_row['Name_job'], p_difference))
                    total_subtracted += p_difference
                    break
                else:
                    needed_preffered_cables.at[p_index, 'difference'] -= j_difference
                    job_cables_to_sub.at[j_index, 'difference'] = 0
                    subtracted_items.append((p_row['Name_prefferred'], j_row['Name_job'], j_difference))
                    total_subtracted += p_difference
                    p_difference -= j_difference

    # Remove zero entries from subtracted_items list
    subtracted_items = [item for item in subtracted_items if item[2] > 0]

    # Remaining items in job_cables_to_sub
    remaining_job_items = job_cables_to_sub[job_cables_to_sub['difference'] > 0]

    # Remaining items in needed_preffered_cables
    remaining_preferred_items = needed_preffered_cables[needed_preffered_cables['difference'] > 0]

    return remaining_job_items, remaining_preferred_items, subtracted_items


def check_cables(job_items, database, column_name):

    cables_from_job = get_cables_from_job(job_items, database, column_name)

    preffered_cable = preffered_cable_counts(job_items, database,column_name )

    compared_merged_cables = compare_cables(cables_from_job, preffered_cable)

    if 'Less' in compared_merged_cables['comparison'].values:
        remaining_job_items, remaining_preferred_items, subtracted_items = suggestions_for_cables(compared_merged_cables)
        print ("  ")

        if subtracted_items is not None:
            print("\nDetails of substituded cables:")
            for item in subtracted_items:
                print(f" {int(item[2])} x  {item[0]} is substituded with {item[1]})")
            
            else :
                print (" no substituded cables") 
            print ("  ")


        if remaining_job_items is not None:
            print("\nDetails of extra cables after substituting:") 
            for index, row in remaining_job_items.iterrows():
                print(f"{int(row['difference'])} x {row['Name_job']}")
            print ("  ")
   
            
        if remaining_preferred_items is not None: 
                print("\nDetails of needed preffered cables after substituting:") 
                for index, row in remaining_preferred_items.iterrows():
                   
                    print(f"{row['difference']} x {row['Name_prefferred']} is needed to be added to the job.")
                print(" These cables are needed to be added to the job.")
                print ("  ")
            

    else:
        print("  ")
        print("The job has perfect match with minimum preffered cable!! Ready to go..")
        print("  ")
        return None  



def update_database(local_db_path, remote_db_path):
    # Read the old and new product databases
    local_db = pd.read_csv(local_db_path)
    remote_db = pd.read_csv(remote_db_path)   

    # Merge the two dataframes using the 'Name' column
    merged_df = pd.merge(local_db, remote_db, on='Name', how='outer') # how = 'outer', 'inner', 'left', 'right'

    #Dropping columns that we do not need
    merged_df = merged_df[[ 'Id_y','Id_x', 'Name', 'Product Group_x', 'Description_x', 'mainsPowerReq', 'powerType', 'prefPwrCbl', 'isCable', 'cblLeng', 'connector1', 'connector2']]
    merged_df.rename(columns={'Id_y': 'Id_dev','Id_x' :'Id_live', 'Description_x' : 'Description', 'Product Group_x' : 'Product Group'}, inplace=True)
   
    # prompt: if the value of prefPwrCbl is in Id_live, fill the prefPwrCbl_dev value of that item with Id_dev value of the element when Id_live value is equal to prefPwrCbl

    merged_df['prefPwrCbl_dev'] = pd.NA
    # Iterate over the DataFrame and fill 'prefPwrCbl_dev' based on the condition
    for index, row in merged_df.iterrows():
        if row['prefPwrCbl'] in merged_df['Id_live'].values:
            merged_df.loc[index, 'prefPwrCbl_dev'] = merged_df.loc[merged_df['Id_live'] == row['prefPwrCbl'], 'Id_dev'].values[0]
    merged_df.to_csv('./databases/merged_db.csv', index=False)
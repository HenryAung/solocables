import pandas as pd
import argparse
import os

def load_data(file_path):
    """Load CSV data from the specified file path."""
    if not os.path.exists(file_path):
        print(f"The specified file was not found: {file_path}")
        return None

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
    filtered_matched_df = matched_df[['name', 'powerType', 'mainsPowerReq', 'Product Group']]

    print(filtered_matched_df)
    return filtered_matched_df

def check_cables(df_product, df_to_match, column_name):
    """Match data from df_to_match against df_product."""
    
    if column_name not in df_product.columns and column_name not in df_to_match.columns:
        print(f"Column '{column_name}' does not exist in one of the DataFrames.")
        return None

    matched_df = pd.merge(df_to_match, df_product, on=column_name, how='left')
    filtered_matched_df = matched_df[['name', 'powerType', 'mainsPowerReq', 'Product Group']]

    products_with_power = filtered_matched_df[filtered_matched_df['mainsPowerReq'] == 'Yes']
    print("      ")
    print ("      ")
    print(products_with_power); 
    print("      ")
    print ("      ")
    power_type_counts = products_with_power['powerType'].value_counts()
    print(power_type_counts)

    
    return products_with_power

def main():
    # parser = argparse.ArgumentParser(description="CSV Data Filter App")
    # parser.add_argument("product_file_path", help="Path to the product database CSV file")
    # args = parser.parse_args()

    df_product = load_data("C:/Users/heinl/Desktop/csv_download/Current-Product-20240709-17597-vhy5tu.csv")
    df_product.rename(columns={'Name': 'name'}, inplace=True)
    df_product = df_product[['name', 'powerType', 'mainsPowerReq', 'Product Group']]


    df_to_match = load_data("C:/Users/heinl/Desktop/csv_download/Wedding_Grove_House_Roehampton.csv")
    column_name_to_match = 'name'

    if df_product is None:
        return

    while True:
        choice = display_options()
        if choice == '1':
            print(df_product)

        elif choice == '2':            
            if df_to_match is not None:
                match_data(df_product, df_to_match,column_name_to_match )
        
        elif choice == '3':
            if df_to_match is not None:
                check_cables(df_product, df_to_match,column_name_to_match )
       
        
        elif choice == '4' : 
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()

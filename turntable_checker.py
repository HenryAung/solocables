
import Scripts.databases.dbQueries as dbQueries
import Scripts.databases.tagDbQueries as tagDbQueries


def add_tag_id_to_job_items(job_items, conn):
    job_items['tag_id'] = None
    job_items['tag_name'] = None

    for index, row in job_items.iterrows():
        tag_data = tagDbQueries.select_tag_by_id_dev(conn, row['Id'])
        if tag_data and isinstance(tag_data, dict):
            job_items.at[index, 'tag_id'] = tag_data.get('tag_id')
            job_items.at[index, 'tag_name'] = tag_data.get('tag_name')
        elif tag_data and isinstance(tag_data, list) and len(tag_data) > 0:
            job_items.at[index, 'tag_id'] = tag_data[0][1]  # Accessing tag_id from tuple
            job_items.at[index, 'tag_name'] = tag_data[0][2]  # Accessing tag_name from tuple

    return job_items



def check_for_turnable(job_items, conn):

    job_items_with_tags = add_tag_id_to_job_items(job_items, conn)
    
    turntable_items = job_items_with_tags[job_items_with_tags['tag_id'] == 208] # 208 is the tag_id for turntable
    cartridge_items = job_items_with_tags[job_items_with_tags['tag_id'] == 209] # 209 is the tag_id for cartridge


    if not turntable_items.empty and not cartridge_items.empty:
        turntable_quantity = turntable_items['quantity'].sum()
        turntable_quantity = int(float(turntable_quantity))
        cartridge_quantity = cartridge_items['quantity'].sum()
        cartridge_quantity = int(float(cartridge_quantity))
        
        if cartridge_quantity  >= turntable_quantity:
            print("**********")
            print(f" There are {turntable_quantity} turntables in the job and {cartridge_quantity} cartridges")
            print("The job is ready ...")
            print("")
        else:
            print("**********")
            print(f" There are {turntable_quantity} turntables in the job and {cartridge_quantity} cartridges")
            print(f"The job is missing {turntable_quantity - cartridge_quantity} cartridge(s)")
            print("")

    else:
        print("**********")
        print("No rules found for this job")
        print("")
        pass 
    

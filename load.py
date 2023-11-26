#    __                 _                    
#   / /  ___   __ _  __| |                   
#  / /  / _ \ / _` |/ _` |                   
# / /__| (_) | (_| | (_| |                   
# \____/\___/ \__,_|\__,_|                                                           
#    ___                                 _   
#   / _ \__ _ _   _ _ __ ___   ___ _ __ | |_ 
#  / /_)/ _` | | | | '_ ` _ \ / _ \ '_ \| __|
# / ___/ (_| | |_| | | | | | |  __/ | | | |_ 
# \/    \__,_|\__, |_| |_| |_|\___|_| |_|\__|
#             |___/                          
#  _____                _                    
# /__   \_ __ __ _  ___| | _____ _ __        
#   / /\/ '__/ _` |/ __| |/ / _ \ '__|       
#  / /  | | | (_| | (__|   <  __/ |          
#  \/   |_|  \__,_|\___|_|\_\___|_|          
                                   
#By Alexis
#Commercial use only through licensing. Please contact my email for details.
#2023 Copyright

# #Load Payment Tracker
# #Goals:

# 1. Open two EXCEL files
# 2. match load numbers in a function
# 3. higligth in yellow the lines that it match in the EXCEL FILES
# 4. Create a third excel file with load number from each file and ammount that the trucker calculated and the broker pay and the date from the trucker file 
# 5. Output a general output saying:
#     Loads matched:
#     Loads not matched:
# 6. Create two folders where in:
#     1st Foldeer will have all the EXCEL FILES OF THE LOADS DOCUMENTED FROM THE TRUCKER 
#     2nd Folder will have all the EXCEL FILES OF THE LOADS PAYED FROM THE BORKER
# 7. The program will automatically open all the files from those folers and match each time we run the program overriding the third excel.
# 8. The Third excel file will have a sumation of payments of what we expect and what we got from loads matched. 
# 9. The program will highlight in green the frist time a load is not matched and if a file is already marked green will mark that same line red meaning its a second run where has not payed.
# 10.the goal is just drop to the folders run program and have the correct output. 

# #This function will call all the required funcitons to run the program
import pandas as pd
import os
import numpy as np
import shutil

def generate_payments():
    
    # Define the folder paths for the trucker and broker files
    trucker_folder_path = './truckerv2'
    broker_folder_path = './broker'

    # Define the names of the columns in the excel files
    
    ####################### EDIT FOR BROKER #############################
    broker_total_amount_col = 'Line_Amt'
    broker_date_col = 'Pay_Date'
    broker_load_number_col = 'Car_Truck_ID'
    
    #############################################
    
    trucker_load_number_col = 'ORIGIN TICKET #'
    trucker_date_col = 'DATE'
    trucker_total_amount_col = 'TOTAL'
   

    root_folder ='./truckerv2'

    #changing headers
    #Ensure that all the files have the same headers to join togheter to ensure 
    #not data corruption
    
    #Replace this or remove it depenging on your needs 
    new_headers = ['CUSTOMER', 'DATE', 'BOL#', 'ORIGIN', 'ORIGIN TICKET #', 'ORIGIN WEIGHT', 'DESTINATION', 'DESTINATION TICKET #', 'DESTINATION WEIGHT', 'BUSHEL / TONS', 'FREIGH RATE', 'TOTAL']

    # loop through all the subfolders and files in the root folder
    for root, dirs, files in os.walk(root_folder):
        for file in files:
         # check if the file is an Excel file
            if file.endswith('.xlsx') or file.endswith('.xls'):
            # construct the full file path
                file_path = os.path.join(root, file)
            # read the Excel file into a DataFrame
                df = pd.read_excel(file_path, header=None , engine= 'openpyxl')
            # replace the first row with the new column headers
                df.iloc[0] = new_headers
            # save the modified DataFrame back to the Excel file
                with pd.ExcelWriter(file_path) as writer:
                    df.to_excel(writer, index=False, header=False)
    
    #End changing headers
    
    data= []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            # check if the file is an Excel file
            if file.endswith('.xlsx') or file.endswith('.xls'):
                # construct the full file path
                file_path = os.path.join(root, file)
                # read the Excel file and append its data, directory path, and file name to the list
                df = pd.read_excel(file_path)
                df['directory'] = root  # add a new column for the directory path
                df['filename'] = file  # add a new column for the file name
                data.append(df)

   
    trucker_df = pd.concat(data, ignore_index=True)   
    trucker_df.to_excel("preview.xlsx")

    broker_files = []
    
    for filename in os.listdir(broker_folder_path):
        broker_file = pd.read_excel(os.path.join(broker_folder_path, filename), usecols=[broker_load_number_col, broker_total_amount_col, broker_date_col])
        broker_files.append(broker_file)
    broker_df = pd.concat(broker_files) #Creating here a bigass excel file 


    trucker_df = trucker_df.rename(columns={trucker_load_number_col: 'Load_Number', trucker_date_col: 'Date_trucker', trucker_total_amount_col: 'Trucker_Amount'})
    broker_df = broker_df.rename(columns={broker_load_number_col: 'Load_Number', broker_total_amount_col: 'Broker_Amount' , broker_date_col: 'Date_broker'})

    broker_df.to_excel("Raw Payments.xlsx")

# ZIAD IDEA JUN 7 2023

    # anotherdf = trucker_df[['Load_Number' , 'Date_trucker' , "Trucker_Amount"]]
    
    # anotherdf = anotherdf.rename(columns={'Load_Number': 'Load_Number', 'Date_trucker' : 'Date_broker', 'Trucker_Amount' : 'Broker_Amount'})
    
    # anotherdf.to_excel("rawtrucker.xlsx")
    # broker_df.to_excel("rawbroker.xlsx")

    # thrdf = broker_df.compare(anotherdf)
    # thrdf.to_excel("Ziadidea.xlsx")
    
# END ZIAD IDEA

    #Checking if the data matches what the broker says 
    result = pd.merge(trucker_df , broker_df , on ='Load_Number', how ='inner')
    result['match'] = (abs(result['Trucker_Amount'] - result['Broker_Amount']) <= 2)
    result['result'] = np.where(result['match'] == True, 'MATCH', 'Discrepancy')

    discrepancies = result[result['result']== 'Discrepancy']

    discrepancies.to_excel("./total payment discrepancies.xlsx")

    #Creating the complete and not completed payment loads
    mask = trucker_df['Load_Number'].isin(broker_df['Load_Number'])
                              
    result3 = trucker_df[~mask]
    
    mask2 = result3['Load_Number'].notnull()
    
    result3 = result3[mask2]
              
    # 2023 NOV 25

    value_counts = result['result'].value_counts()

    # Calculate the percentage of each value
    percentages = result['result'].value_counts(normalize=True) * 100

    # Combine the counts and percentages into one DataFrame for easy viewing
    summary = pd.DataFrame({'Count': value_counts, 'Percentage': percentages})

    
    # Filter out the rows where result is 'Discrepancy'
    discrepancies = result[result['result'] == 'Discrepancy']

    # Count where Broker_Amount is greater than Trucker_Amount
    broker_greater_count = discrepancies[discrepancies['Broker_Amount'] > discrepancies['Trucker_Amount']].shape[0]

    # Count where Trucker_Amount is greater than Broker_Amount
    trucker_greater_count = discrepancies[discrepancies['Trucker_Amount'] > discrepancies['Broker_Amount']].shape[0]

    # DataFrame where Broker_Amount is greater
    broker_greater_df = discrepancies[discrepancies['Broker_Amount'] > discrepancies['Trucker_Amount']]

    # DataFrame where Trucker_Amount is greater
    trucker_greater_df = discrepancies[discrepancies['Trucker_Amount'] > discrepancies['Broker_Amount']]

    broker_greater_df.to_excel('./Payment_Discrepancies_File/Broker_discrepancies.xlsx' , index = False)

    trucker_greater_df.to_excel('./Payment_Discrepancies_File/Trucker_discrepancies.xlsx' , index = False)

    print("LOADS THAT ALREADY PAID ")
    print("*******************************************")
    print(result)
    print(summary)
    print("Number of discrepancies where Broker_Amount is greater:", broker_greater_count)
    print("Number of discrepancies where Trucker_Amount is greater:", trucker_greater_count)

    result.to_excel('Payments completed.xlsx')
    result3.to_excel('Payments NOT completed.xlsx')
    

# U _____ u _   _    ____                                                        
# \| ___"|/| \ |"|  |  _"\                                                       
#  |  _|" <|  \| |>/| | | |                                                      
#  | |___ U| |\  |uU| |_| |\                                                     
#  |_____| |_| \_|  |____/ u                                                     
#  <<   >> ||   \\,-.|||_                                                        
# (__) (__)(_")  (_/(__)_)                                                       
#    ____  U _____ u _   _   U _____ u   ____        _       _____  U _____ u    
# U /"___|u\| ___"|/| \ |"|  \| ___"|/U |  _"\ u U  /"\  u  |_ " _| \| ___"|/    
# \| |  _ / |  _|" <|  \| |>  |  _|"   \| |_) |/  \/ _ \/     | |    |  _|"      
#  | |_| |  | |___ U| |\  |u  | |___    |  _ <    / ___ \    /| |\   | |___      
#   \____|  |_____| |_| \_|   |_____|   |_| \_\  /_/   \_\  u |_|U   |_____|     
#   _)(|_   <<   >> ||   \\,-.<<   >>   //   \\_  \\    >>  _// \\_  <<   >>     
#  (__)__) (__) (__)(_")  (_/(__) (__) (__)  (__)(__)  (__)(__) (__)(__) (__)    
#   ____       _      __   __  __  __  U _____ u _   _     _____   ____          
# U|  _"\ uU  /"\  u  \ \ / /U|' \/ '|u\| ___"|/| \ |"|   |_ " _| / __"| u       
# \| |_) |/ \/ _ \/    \ V / \| |\/| |/ |  _|" <|  \| |>    | |  <\___ \/        
#  |  __/   / ___ \   U_|"|_u | |  | |  | |___ U| |\  |u   /| |\  u___) |        
#  |_|     /_/   \_\    |_|   |_|  |_|  |_____| |_| \_|   u |_|U  |____/>>       
#  ||>>_    \\    >>.-,//|(_ <<,-,,-.   <<   >> ||   \\,-._// \\_  )(  (__)      
# (__)__)  (__)  (__)\_) (__) (./  \.) (__) (__)(_")  (_/(__) (__)(__)   
    
    
################################################################################################
    

#This function will create a duplicate of trucker folder with the same files but the data inside the file will be 
#Only the loads paid from that file

def duplicates_with_only_payed_loads():
    # Define the folder paths for the trucker and broker files
    trucker_folder_path = './truckerv2'
    broker_folder_path = './broker'
    trucker_files_paid_only = './trucker_only_paid_loads'
    trucker_files_not_paid = './truckers_only_not_paid_loads'

    # Define the names of the columns in the excel files
    
    
    ####################### EDIT FOR BROKER #############################
    broker_load_number_col = 'Car_Truck_ID'
    broker_total_amount_col = 'Line_Amt'
    broker_date_col = 'Pay_Date'
    
    
    trucker_load_number_col = 'ORIGIN TICKET #'
    trucker_date_col = 'DATE'
    trucker_total_amount_col = 'TOTAL'
    
     #############################################

    entire_trucker_files = [] 
    

    data= []
    for root, dirs, files in os.walk(trucker_folder_path):
        for file in files:
                # check if the file is an Excel file
            if file.endswith('.xlsx') or file.endswith('.xls'):
                    # construct the full file path
                file_path = os.path.join(root, file)
                    # read the Excel file and append its data, directory path, and file name to the list
                df = pd.read_excel(file_path)
                df['directory'] = root  # add a new column for the directory path
                df['filename'] = file  # add a new column for the file name
                data.append(df)

   
    trucker_df = pd.concat(data, ignore_index=True)   
    trucker_df['directory'] = trucker_df['directory'].str.replace("./truckerv2/", "./load_payed/")
   
   #Debbuging code 
   # trucker_df.to_excel("preview2ndfile.xlsx")



    broker_files = []
    for filename in os.listdir(broker_folder_path):
        broker_file = pd.read_excel(os.path.join(broker_folder_path, filename), usecols=[broker_load_number_col, broker_total_amount_col, broker_date_col])
        broker_files.append(broker_file)
    broker_df = pd.concat(broker_files) #Creating here a bigass excel file 

    broker_df.to_excel("2ndbrokerdf.xlsx")
    
    trucker_df = trucker_df.rename(columns={trucker_load_number_col: 'Load_Number', trucker_date_col: 'Date_Trucker', trucker_total_amount_col: 'Trucker_Amount'})
    broker_df = broker_df.rename(columns={broker_load_number_col: 'Load_Number', broker_total_amount_col: 'Broker_Amount', broker_date_col: 'Date_Broker'})

    #print(trucker_df)
    result = pd.merge(trucker_df , broker_df , on ='Load_Number')
    result.to_excel("whatdata.xlsx")
    
    result['match'] = (abs(result['Trucker_Amount'] - result['Broker_Amount']) <= 2)
    result['result'] = np.where(result['match'] == True, 'MATCH', 'Discrepancy')
    
    grouped_df = result.groupby(['directory','filename'])
    
    #Deletes the path to dont overlay the output
    if os.path.isdir("./load_payed"):
        shutil.rmtree("./load_payed")
        
    #The following code writes the data into the excel files 
    #and stores in the corresponging folder instead of just by name
    #The completed payments
        
    for group, data in grouped_df:
        directory, filename = group
        output_path = directory + '/'
        output_file = directory + '/' + filename
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if os.path.isfile(output_file):
            # Load the existing Excel file
            existing_df = pd.read_excel(output_file)

            # Concatenate the existing data with the new data
            combined_df = pd.concat([existing_df, data], axis=0, ignore_index=True)

            # Save the combined data to the file
            combined_df.to_excel(output_file, index=False)
        else:
            # Save the new data to a new Excel file at the specified output path
            data.to_excel(output_file, index=False)
    
    #Incompleted payments
    
     #Deletes the path to dont overlay the output
    if os.path.isdir("./load_not_payed"):
        shutil.rmtree("./load_not_payed")
     
    not_completed_df = pd.read_excel("./Payments NOT completed.xlsx")
    
    not_completed_df['directory'] = not_completed_df['directory'].str.replace("./truckerv2/", "./load_not_payed/")
        
    not_grouped_df = not_completed_df.groupby(['directory','filename'])
    
    for group, data in not_grouped_df:
        directory, filename = group
        output_path = directory + '/'
        output_file = directory + '/' + filename
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if os.path.isfile(output_file):
            # Load the existing Excel file
            existing_df = pd.read_excel(output_file)

            # Concatenate the existing data with the new data
            combined_df = pd.concat([existing_df, data], axis=0, ignore_index=True)

            # Save the combined data to the file
            combined_df.to_excel(output_file, index=False)
        else:
            # Save the new data to a new Excel file at the specified output path
            data.to_excel(output_file, index=False)
    
    
    #Legacy Code
    #Relevant for the implementation of the ammenment payments functioanlity 
    
    ## Shows duplicate payments 
    local = result
    temporal = result.duplicated(subset=['Load_Number'], keep = False)
    local = local[temporal]
    local.to_excel('No Dup.xlsx')
    temporal.to_excel('Dup.xlsx')
    #End Duplicate payments 



#  _______  _        ______                                                                 
# (  ____ \( (    /|(  __  \                                                                
# | (    \/|  \  ( || (  \  )                                                               
# | (__    |   \ | || |   ) |                                                               
# |  __)   | (\ \) || |   | |                                                               
# | (      | | \   || |   ) |                                                               
# | (____/\| )  \  || (__/  )                                                               
# (_______/|/    )_)(______/                                                                
                                                                                          
#  ______            _______  _       _________ _______  _______ _________ _______  _______ 
# (  __  \ |\     /|(  ____ )( \      \__   __/(  ____ \(  ___  )\__   __/(  ____ \(  ____ \
# | (  \  )| )   ( || (    )|| (         ) (   | (    \/| (   ) |   ) (   | (    \/| (    \/
# | |   ) || |   | || (____)|| |         | |   | |      | (___) |   | |   | (__    | (_____ 
# | |   | || |   | ||  _____)| |         | |   | |      |  ___  |   | |   |  __)   (_____  )
# | |   ) || |   | || (      | |         | |   | |      | (   ) |   | |   | (            ) |
# | (__/  )| (___) || )      | (____/\___) (___| (____/\| )   ( |   | |   | (____/\/\____) |
# (______/ (_______)|/       (_______/\_______/(_______/|/     \|   )_(   (_______/\_______)
                                                                                          
#  _______  _        _                                                                      
# (  ___  )( (    /|( \   |\     /|                                                         
# | (   ) ||  \  ( || (   ( \   / )                                                         
# | |   | ||   \ | || |    \ (_) /                                                          
# | |   | || (\ \) || |     \   /                                                           
# | |   | || | \   || |      ) (                                                            
# | (___) || )  \  || (____/\| |                                                            
# (_______)|/    )_)(_______/\_/                                                            
                                                                                          
#  _______  _______           _______  ______                                               
# (  ____ )(  ___  )|\     /|(  ____ \(  __  \                                              
# | (    )|| (   ) |( \   / )| (    \/| (  \  )                                             
# | (____)|| (___) | \ (_) / | (__    | |   ) |                                             
# |  _____)|  ___  |  \   /  |  __)   | |   | |                                             
# | (      | (   ) |   ) (   | (      | |   ) |                                             
# | )      | )   ( |   | |   | (____/\| (__/  )                                             
# |/       |/     \|   \_/   (_______/(______/        




#NOTA PARA ALEXIS ESTA PARTE DEL CODIGO AHORITA ES ESTE MOMENTO SE ME HACE ETERNA SI EL CODIGO YA FUNCIONA
# MARZO 31 2023


#ALEXIS DEL FUTURO ACABA ESTA PARTE DEL CODIGO ASAP 


#NOTA  PARA ALEXIS YA LE AGARRASTE EL PEDO
#MAYO 2 2023




def fixed_payments():
    # Define the folder paths for the trucker and broker files
    trucker_paided = './trucker_only_paid_loads'
    claims = './claims_fixed'

    # Define the names of the columns in the excel files
    
    
    ####################### EDIT FOR BROKER #############################
    claims_date = 'DATE'
    claims_deposit = 'AMMOUNT DEPOSITED'
    claims_ticket = 'ORIGIN TICKET #'
 
        
    trucker_load_number_col = 'ORIGIN TICKET #'
    trucker_date_col = 'DATE'
    trucker_total_amount_col = 'TOTAL'


    #Deleted because overhaul of the entire code 


#Calling the programs 
generate_payments()
duplicates_with_only_payed_loads()
#fixed_payments()

def outsidecaller():
    generate_payments()
    duplicates_with_only_payed_loads()
    




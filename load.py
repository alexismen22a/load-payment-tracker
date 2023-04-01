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

def generate_payments():
    
    # Define the folder paths for the trucker and broker files
    trucker_folder_path = './trucker'
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
   

    # Load all the trucker and broker files into dataframes
    trucker_files = []
    for filename in os.listdir(trucker_folder_path):
        trucker_file = pd.read_excel(os.path.join(trucker_folder_path, filename), usecols=[trucker_load_number_col, trucker_date_col, trucker_total_amount_col])
    
        trucker_files.append(trucker_file)
    trucker_df = pd.concat(trucker_files) #Creating here a bigass excel file 

    broker_files = []
    for filename in os.listdir(broker_folder_path):
        broker_file = pd.read_excel(os.path.join(broker_folder_path, filename), usecols=[broker_load_number_col, broker_total_amount_col, broker_date_col])
        broker_files.append(broker_file)
    broker_df = pd.concat(broker_files) #Creating here a bigass excel file 

    #print(trucker_df)

    trucker_df = trucker_df.rename(columns={trucker_load_number_col: 'Load_Number', trucker_date_col: 'Date_trucker', trucker_total_amount_col: 'Trucker_Amount'})
    broker_df = broker_df.rename(columns={broker_load_number_col: 'Load_Number', broker_total_amount_col: 'Broker_Amount' , broker_date_col: 'Date_broker'})

    #print(trucker_df)
    #OG RESULT result = pd.merge(trucker_df , broker_df , on ='Load_Number', how ='inner')
    result = pd.merge(trucker_df , broker_df , on ='Load_Number', how ='inner')
    result['match'] = (abs(result['Trucker_Amount'] - result['Broker_Amount']) <= 2)
    result['result'] = np.where(result['match'] == True, 'MATCH', 'Discrepancy')


    mask = trucker_df['Load_Number'].isin(broker_df['Load_Number'])
                              
    result3 = trucker_df[~mask]
    
    mask2 = result3['Load_Number'].notnull()
    
    result3 = result3[mask2]
              

    print("LOADS THAT ALREADY PAID")
    print("*******************************************")
    print(result)
    result.to_excel('Payments completed.xlsx')
    result3.to_excel('Payments NOT completed.xlsx')
    
    
    

#This function will create a duplicate of trucker folder with the same files but the data inside the file will be 
#Only the loads paid from that file
def duplicates_with_only_payed_loads():
    # Define the folder paths for the trucker and broker files
    trucker_folder_path = './trucker'
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

    # Load all the trucker and broker files into dataframes
    trucker_files = []
    entire_trucker_files = [] 
    
    for filename in os.listdir(trucker_folder_path):
        trucker_file = pd.read_excel(os.path.join(trucker_folder_path, filename), usecols=[trucker_load_number_col, trucker_date_col, trucker_total_amount_col])
        entire_trucker_file = pd.read_excel(os.path.join(trucker_folder_path, filename)) #This Line stores the entire row of the excel file 
        trucker_files.append(trucker_file)
        entire_trucker_files.append((entire_trucker_file,filename))
    trucker_df = pd.concat(trucker_files) #Creating here a bigass excel file 

    broker_files = []
    for filename in os.listdir(broker_folder_path):
        broker_file = pd.read_excel(os.path.join(broker_folder_path, filename), usecols=[broker_load_number_col, broker_total_amount_col, broker_date_col])
        broker_files.append(broker_file)
    broker_df = pd.concat(broker_files) #Creating here a bigass excel file 

    
    trucker_df = trucker_df.rename(columns={trucker_load_number_col: 'Load_Number', trucker_date_col: 'Date_Trucker', trucker_total_amount_col: 'Trucker_Amount'})
    broker_df = broker_df.rename(columns={broker_load_number_col: 'Load_Number', broker_total_amount_col: 'Broker_Amount', broker_date_col: 'Date_Broker'})

    #print(trucker_df)
    result = pd.merge(trucker_df , broker_df , on ='Load_Number', how ='inner')

    local = result
    temporal = result.duplicated(subset=['Load_Number'], keep = False)
    
    local = local[temporal]
    local.to_excel('No Dup.xlsx')

    temporal.to_excel('Dup.xlsx')



    for excel_files,name in entire_trucker_files:
        excel_files = excel_files.rename(columns={trucker_load_number_col: 'Load_Number'})
        
        
        
        result2 = pd.merge(excel_files , result , on ='Load_Number', how ='inner')
        
        mask = excel_files['Load_Number'].isin(result['Load_Number'])
        
        result3 = excel_files[~mask]
        
        
        
        mask2 = result3['Load_Number'].notnull()
    
        result3 = result3[mask2]
        
        
        result2['match'] = (abs(result2['Trucker_Amount'] - result2['Broker_Amount']) <= 2)
        result2['result'] = np.where(result2['match'] == True, 'MATCH', 'Discrepancy')

        local2 = result3.duplicated(subset=['Load_Number'], keep = False)
        local2 = result3[local2]
        local2.to_excel('./test/'+name+'.xlsx')
                
        result2.to_excel(trucker_files_paid_only+"/"+name)
                        #'./trucker_only_paid_loads'/ Filename
        
        result3.to_excel(trucker_files_not_paid+"/"+name)
              

#NOTA PARA ALEXIS ESTA PARTE DEL CODIGO AHORITA ES ESTE MOMENTO SE ME HACE ETERNA SI EL CODIGO YA FUNCIONA
# MARZO 31 2023

#ALEXIS DEL FUTURO ACABA ESTA PARTE DEL CODIGO ASAP 

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


    trucker_files=[]
    entire_trucker_files=[]

    #opening the files in trucker paid loads 
    for filename in os.listdir(trucker_paided):
        trucker_file = pd.read_excel(os.path.join(trucker_paided, filename), usecols=[trucker_load_number_col, trucker_date_col, trucker_total_amount_col])
        entire_trucker_file = pd.read_excel(os.path.join(trucker_paided, filename)) #This Line stores the entire row of the excel file 
        trucker_files.append(trucker_file)
        entire_trucker_files.append((entire_trucker_file,filename))

    #Opening the files in claims fixed 

    for filename in os.listdir(claims):
        claim_file = pd.read_excel()

    




#Calling the programs 
generate_payments()
duplicates_with_only_payed_loads()
#fixed_payments()




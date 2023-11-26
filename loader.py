import subprocess
import time
import os 
from datetime import datetime
import load as loady
import Email_retriever as retriever



def run_external_code(file_path):
    try:
        subprocess.run(["python3" ,file_path], check=True)
        print(f"Successfully executed {file_path}")
    except subprocess.CalledProcessError:
        print(f"Error executing {file_path}")

def run_external_codes():
    # Specify the paths of the external code files
    code_file1 = "./Email_retriever.py"
    code_file2 = "./load.py"
    
    # Run the first external code
    current_datetime = datetime.now()
    print("Running Email Retriever at : " , current_datetime)

    retriever.stepper()

    current_datetime = datetime.now()
    print("End at : " ,current_datetime)
    time.sleep(10)
    current_datetime = datetime.now()
    # Run the second external code
    print("Running Email Retriever at : " , current_datetime)
    
    loady.outsidecaller()
    
    current_datetime = datetime.now()
    print("End at : " ,current_datetime)
    time.sleep(6 * 60 * 60)

while True:
    run_external_codes()
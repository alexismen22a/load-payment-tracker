import os
import pandas as pd
from fuzzywuzzy import process

input_folder = './notfilled'
output_folder = './filled'

# The mapping from a specific column value to the freight rate
# Replace this with your actual mapping
freight_rate_dict = {

}

# Get all csv files in the input folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

for file_name in csv_files:
    # load the data
    df = pd.read_csv(os.path.join(input_folder, file_name))

    # remove the first and the last column
    df = df.iloc[:, 1:-1]
    
    # Add three new columns to the end with default values (for now)
    df['BUSHEL / TONS'] = ""
    df['FREIGHT RATE'] = 0
    df['TOTAL'] = 0

    
    for i, row in df.iterrows():
        other_value = row['DESTINATION']
        closest_match, _ = process.extractOne(other_value, freight_rate_dict.keys())
        df.at[i, 'FREIGHT RATE'] = freight_rate_dict[closest_match]

    # Calculate the 'TOTAL' column by multiplying the 'ORIGIN WEIGHT' and 'FREIGHT RATE' columns
    df['TOTAL'] = df['ORIGIN WEIGHT'] * df['FREIGHT RATE']

    # Calculate the sum of the 'TOTAL' column
    total_sum = df['TOTAL'].sum()

    # Add a new row to the DataFrame with the total sum
    new_row = pd.Series([None]*len(df.columns), index=df.columns)
    new_row['TOTAL'] = total_sum
    df = df.append(new_row, ignore_index=True)

    # write the data back to a new csv file
    df.to_excel(os.path.join(output_folder, file_name.replace('.csv', '.xlsx')), index=False)
    
    

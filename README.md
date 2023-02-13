# Load Payment Tracker
This program will alayze two files to check if loads are paid.

This software will check two excel files to check if loads are paid and generate an 3 excel files.

First excel file will be the trucker owner with loads paid mark in yellow.

Second excel file will be the dispatcher with loads paid mark in yellow.

Third excel file will be a convination of the two files mathcing the loads and the price of tucker owner and dispacher.

## How To Use 

### Requierements

The program needs 3 folders to exist in order to work  (broker, trucker, trucker_only_paid_loads)

In order to this program to run you need to put your excel files in the folder "trucker"

The broker excel files in the folder "broker"

The folder trucker_only_paid_loads it would be empty.


### How to Run

1. Add the excel files into the specified folders 

2. Run the program with the command ./load.py

3. Wait for output 


### Expected Output

The program will generate two outputs:

First output is: "Payments completed.xlsx " that file will contain all the loads paid in one excel file. 

Second output is: The files from trucker but with only loads paids inside the excel file and keeping the original names and files  to keep control of files.




Copyright all rights reserve for contributors.

Any use of this software in comercial use without autorization is prohibited and will required writing autorization from owners.

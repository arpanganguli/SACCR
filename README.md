# SACCR
## About SACCR
SACCR is an interest rate calculator based on Basel III's [Standardised Approach (SA) for measuring Counterparty Credit Risk (CCR) exposures](https://www.bis.org/publ/bcbs279.pdf).

## How to run this repository**
First, clone the repository and then change your directory to the repository on your hard drive by typing `cd [path_to_your_repository_on_hard_drive]` at the command prompt in the Mac/Linux Terminal or in the Windows Command Window or PowerShell.

There are three components of the repository:
 - **File generation:** Type `python3 ag_random_fire_generator.py X` where X represents the number of data you want to generate. For example, if you want to generate 25 rows of data (i.e. derivatives), then you will need to type `python3 ag_random_fire_generator.py 25` at the command prompt.
 
	This file is built on top of the [random_fire_generator.py](https://github.com/SuadeLabs/fire/blob/master/random_fire_generator.py) file with some modifications.
 - **EAD Calculation:** Type `python3 ag_EAD_calculation.py`. This will calculate the EAD and will display the result that we seek through this calculator.
 - **Testing:** Go to the testing folder by typing `cd Tests`and then typing `python3 test_functions.py`.

## Assumptions
- The hedging set consists only of interest rate swaps and swaptions for derivatives and USD and GBP for currencies.
- The netting set is not subject to a margin agreement and there is no exchange of collateral (independent amount/initial margin) at inception.

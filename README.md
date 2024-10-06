Backend Assignment - 1

# Backend Assignment - 1

**Objective** - Using the below information calculate the user’s current portfolio value and portfolio XIRR. 

**How to process transactions - 
1.)** The user may have executed various transactions, such as buying or selling units at different price points over time. These transactions follow a First-In-First-Out (FIFO) approach, meaning the units purchased earliest are sold first. 
**2.**) Transactions are tagged with a scheme which can be identified with its name and its ISIN number. Example - Aditya Birla Sun Life ELSS Tax Saver Fund- (ELSS U/S 80C of IT ACT) - Growth-Direct Plan with ISIN INF209K01UN8. 
**3.)** Brokers ( like PayTm , Zerodha etc ) used for transactions can also be identified using the folio number. Each combination of Scheme-Broker has a unique folio. This impacts the FIFO calculations. FIFO is done at folio level. Meaning that if you sell something on PayTm then your transactions will get applied to units you hold in PayTm and not on Zerodha. It seems obvious but this has to be coded in the data by applying the FIFO at Folio level. 

4.) Number of Units are calculated as Transaction Amount / Purchase Price 

5.) There are 2 nested Jsons in the below Json called DTsummary , DTtransaction. Data available in DT transaction is relevant for this assignment 

**Task -** 

1.) Calculate the Total Portfolio value 

- This is calculated as sum of ( left over units X NAV of scheme )

2.) Calculate the Total Portfolio Gain 

- This is calculated as Sum of ( Current Unit Value - Unit Acquisition cost )
- Current Unit Value is the current NAV of scheme X number of units
- Unit acquisition cost is the Units X Purchase Price of Units

3.) Calculate the XIRR of the Portfolio ( optional question. You don’t need to do this unless you feel to ) 

- To calculate the XIRR you need following details
    - Date of Transaction
    - Amount of Transaction
    - Current Portfolio Value

**Resources -** 

To get the current nav (**Net Asset Value**) of a fund, mstarpy library can be used - 

https://pypi.org/project/mstarpy/

with this fund history can be found with
       fund = mstarpy.Funds(term=isin, country="in")
       
       // to get the today's date and historyical date, this can be used - 
       end_date = datetime.datetime.now()
       start_date = end_date - datetime.timedelta(days=365)  # Fetch 1 year of NAV history
       
       // to get the historical nav - 
       history = fund.nav(start_date=start_date, end_date=end_date, frequency="daily")
each transaction must be in the form of - 
{
      "trxnDate" : "13-AUG-2019",
      "scheme" : "02GZ",
      "trxnDesc" : "Purchase",
      "schemeName" : "Aditya Birla Sun Life ELSS Tax Saver Fund- (ELSS U/S 80C of IT ACT) - Growth-Direct Plan ",
      "tax" : "0.00",
      "purchasePrice" : "30.56",
      "sttTax" : "0.00",
      "postedDate" : "13-AUG-2019",
      "totalTax" : "0.00",
      "trxnMode" : "N",
      "trxnUnits" : "32.723",
      "stampDuty" : "",
      "trxnTypeFlag" : "FP",
      "amc" : "B",
      "amcName" : "Aditya Birla Sun Life Mutual Fund",
      "trxnAmount" : "1000.00",
      "folio" : "1039101537",
      "checkDigit" : "",
      "email" : "dummy@gmail.com",
      "isin" : "INF209K01UN8",
      "trxnCharge" : "0.00"
    }
where `trxnUnits` defines the unit purchase and purchasePrice is the `nav`  of the fund on the purchase date, positive `trxnUnits` means buy and negative means sell

now as a part of this assignment, share a working code which can be run on the any input transaction file, it will be a json file with a sample input file will be provided with the assignment and in the output expecting the net unit of each fund, net value as of today for each fund and total value

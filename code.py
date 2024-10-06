import json
import datetime
import mstarpy
from collections import defaultdict
from xirr import xirr  # If using for XIRR calculation

# Helper function to fetch current NAV
def fetch_current_nav(isin):
    fund = mstarpy.Funds(term=isin, country="in")
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)
    history = fund.nav(start_date=start_date, end_date=end_date, frequency="daily")
    # Assuming NAV on the latest available date
    return history[-1]['nav']

# Process JSON file and calculate portfolio value
def process_portfolio(json_file):
    # Load the JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    transactions = data["DTtransaction"]
    
    # Portfolio data structure
    portfolio = defaultdict(lambda: {"units": 0, "cost": 0, "transactions": []})
    
    # Process transactions
    for trxn in transactions:
        folio = trxn['folio']
        scheme_name = trxn['schemeName']
        isin = trxn['isin']
        nav = float(trxn['purchasePrice'])
        units = float(trxn['trxnUnits'])
        amount = float(trxn['trxnAmount'])
        date = datetime.datetime.strptime(trxn['trxnDate'], "%d-%b-%Y")
        
        # Add transaction to portfolio folio
        portfolio[folio]["transactions"].append({
            "date": date,
            "units": units,
            "amount": amount,
            "nav": nav
        })
        
        if units > 0:
            # Buying units
            portfolio[folio]["units"] += units
            portfolio[folio]["cost"] += amount
        else:
            # Selling units using FIFO
            remaining_units_to_sell = abs(units)
            transactions = sorted(portfolio[folio]["transactions"], key=lambda x: x['date'])
            
            for t in transactions:
                if t['units'] > remaining_units_to_sell:
                    t['units'] -= remaining_units_to_sell
                    portfolio[folio]["units"] -= remaining_units_to_sell
                    remaining_units_to_sell = 0
                    break
                else:
                    remaining_units_to_sell -= t['units']
                    portfolio[folio]["units"] -= t['units']
                    t['units'] = 0
    
    # Calculate total portfolio value and gain
    total_portfolio_value = 0
    total_gain = 0
    for folio, details in portfolio.items():
        remaining_units = details["units"]
        current_nav = fetch_current_nav(details['transactions'][0]['isin'])  # Assuming ISIN is same for a folio
        current_value = remaining_units * current_nav
        acquisition_cost = details["cost"]
        gain = current_value - acquisition_cost
        
        total_portfolio_value += current_value
        total_gain += gain
    
    return total_portfolio_value, total_gain

# Example usage
json_file = 'path_to_transaction_file.json'
portfolio_value, portfolio_gain = process_portfolio(json_file)

print(f"Total Portfolio Value: {portfolio_value}")
print(f"Total Portfolio Gain: {portfolio_gain}")

# XIRR Calculation (Optional)
# You can calculate XIRR if needed by passing the transactions to the xirr function:
# cashflows = [(trxn['date'], -trxn['amount']) for folio in portfolio for trxn in portfolio[folio]["transactions"]]
# cashflows.append((datetime.datetime.now(), portfolio_value))  # Current portfolio value as positive cashflow
# portfolio_xirr = xirr(cashflows)
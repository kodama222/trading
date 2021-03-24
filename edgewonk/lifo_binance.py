"""
Created on Sat Dec 26 14:25:06 2020

@author: daniel.royo
"""

from collections import deque
import pandas as pd
import numpy as np
import datetime as dt
from openpyxl import load_workbook
from datetime import datetime, timedelta

# round to N decimal places
# def myRound(num,N):
#     return float( round( num * (10**N) ) ) / (10**N)

ID = 1

# Trade class
# properties: date, type (BUY/SELL), symbol, price, quantity, fees
class trade_class:
    def __init__(self, date:datetime, type_trade:str, symbol:str,  price:np.float64, quantity:np.float64, fees:np.float64):
        self.date = date
        self.type = type_trade
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.fees = fees
        # self.id = ID #id number of transaction
        # ID += 1
        
    def get_date(self):
        return self.date
    def get_symbol(self):
        return self.symbol
    def get_quant(self):
        return self.quantity
    def get_price(self):
        return self.price
    def get_fees(self):
        return self.fees

transactions = []

# holding class
# properties: date, symbol, price, quantity, fees, pnl
class holding_class:
    def __init__(self, date:datetime, symbol:str, price:np.float64, quantity:np.float64, fees:np.float64, pnl:np.float64):
        # self.id = ???
        self.date = date
        self.symbol = symbol
        self.quantity = quantity 
        self.price = price
        self.fees = fees 
        self.pnl = pnl

    def get_date(self):
        return self.date
    def get_symbol(self):
        return self.symbol
    def get_quant(self):
        return self.quantity
    def get_price(self):
        return self.price
    def get_fees(self):
        return self.fees
    def get_pnl(self):
        return self.pnl
    
    def set_pnl(self, pnl):
        self.pnl += pnl
    def set_quant(self,newQuant):
        #self.quantity = myRound(float(newQuant),8)
        self.quantity = newQuant
    def substract_x(self,toSubtract): # ONLY USE WHEN AMOUNT SUBTRACTING IS LESS THAN self.quantity
        self.quantity -= toSubtract
        #self.quantity -= myRound(float(toSubtract),8)
        # Optionally include some validation

holdings_lifo = [] # [list of holdings], gain/loss

# edgewonk_df = pd.Dataframe(index=[0],)

# Add trade to holding list of lists (holdings_lifo) as holding class object
def add_to_holdings(t):
    date = t.get_date()
    symbol = t.get_symbol()
    quantity = t.get_quant()
    price = t.get_price()
    fees = t.get_fees()
    pnl = 0
    h = holding_class(date, symbol, price, quantity, fees, pnl) # Re-initialize to append new object, rather than reference to original
    holdings_lifo.append(h)
    
# Create dataframe of clsoed trades    
columns_closed = ['Opening Time', 'Type [buy/sell]', 'Symbol', 'Size / Quantity', 'Closing Time', 'Entry Price',  'Closing Price', 'Swap', 'Comission', 'Net Profit']
columns_open = ['Opening Time', 'Type [buy/sell]', 'Symbol', 'Size / Quantity', 'Entry Price', 'Swap', 'Comission', 'Net Profit']

#df_closed_trades = pd.DataFrame(index=[0], columns=columns)

class closed_trades:
    def __init__(self):
        self.main_dataframe = pd.DataFrame(data=None, columns=columns_closed)
        
    def append_dataframe(self, df_tmp):
        self.main_dataframe = self.main_dataframe.append(df_tmp)
    
    def to_file(self):
         self.main_dataframe.to_excel(r'C:\Users\danie\OneDrive\Desktop\daniel\edgewonk\edgewonk_data\edgewonk_data.xlsx', index=False)
         
class open_trades:
    def __init__(self):
        self.main_dataframe = pd.DataFrame(data=None, columns=columns_open)
        
    def append_dataframe(self, df_tmp):
        self.main_dataframe = self.main_dataframe.append(df_tmp)
    
    def to_file(self):
         self.main_dataframe.to_excel(r'C:\Users\danie\OneDrive\Desktop\daniel\edgewonk\edgewonk_data\open_trades.xlsx', index=False)
           
            
def remove_from_holdings_lifo(t):
    date = t.get_date()
    symbol = t.get_symbol()
    quantity = t.get_quant()
    price = t.get_price()
    fees = t.get_fees()
    
    
    x = 1
    len_holdings_lifo = len(holdings_lifo)
    
    #while len_holdings_lifo > x and len_holdings_lifo > tic:
    while len_holdings_lifo > x:
        #for holding in reversed(list(holdings_lifo)):
        #transaction_fully_accounted_for = False    
        holding_symbol = holdings_lifo[-x].get_symbol()
        
        #if t.symbol == holding_symbol:
        while t.symbol == holding_symbol:
            #while transaction_fully_accounted_for != True and x < len(holdings_lifo):
            #while transaction_fully_accounted_for != True and t.symbol == holding_symbol:
            # Check if there are enough in first holding
            # if exactly enough, remove first holding & done w/ removing holdings
            holding_date = holdings_lifo[-x].get_date()
            holding_quant = holdings_lifo[-x].get_quant()
            holding_price = holdings_lifo[-x].get_price()
            holding_fees = holdings_lifo[-x].get_fees()
            holding_pnl = holdings_lifo[-x].get_pnl()
            if holding_quant == quantity: #  Quantity is equal to that of the first remaining holding
                holding_pnl = (price - holding_price)*quantity
                data = {'Opening Time':holding_date, 
                        'Type [buy/sell]':'BUY',
                        'Symbol': symbol,
                        'Size / Quantity':holding_quant,
                        'Closing Time':date,
                        'Entry Price':holding_price,
                        'Closing Price':price,
                        'Swap':np.nan,
                        # Implement fee*BNB/BTC vale
                        # In the meantime fee=0
                        #'Comission': holding_fees + fees,
                        'Comission': 0,
                        'Net Profit':holding_pnl,}
                df_loop = pd.DataFrame(data, index=[0])
                df_closed_trades.append_dataframe(df_loop)
                #transaction_fully_accounted_for = True
                holdings_lifo.pop(-x)
                len_holdings_lifo -= 1
                holding_symbol = holdings_lifo[-x].get_symbol()
                return df_closed_trades
                #holdings_lifo.remove(holding)
                
                
            elif quantity < holding_quant: # Quantity is smaller than in first correspondent holding ...
                holding_pnl = (price - holding_price)*quantity
                data = {'Opening Time':holding_date, 
                        'Type [buy/sell]':'BUY',
                        'Symbol': symbol,
                        'Size / Quantity':quantity,
                        'Closing Time':date,
                        'Entry Price':holding_price,
                        'Closing Price':price,
                        'Swap':np.nan,
                        # Implement fee*BNB/BTC vale
                        # In the meantime fee=0
                        #'Comission': holding_fees + fees,
                        'Comission': 0,
                        'Net Profit':holding_pnl,}
                df_loop = pd.DataFrame(data, index=[0])
                df_closed_trades.append_dataframe(df_loop)
                #holdings_lifo[x].substract_x(quantity)
                holdings_lifo[-x].set_quant(holding_quant-quantity)
                #transaction_fully_accounted_for = True
                return df_closed_trades
                
                
                
            elif quantity > holding_quant:  # Quantity sold exceeds value of the first remaining holding
            #else:
                holding_pnl = (price - holding_price)*quantity
                data = {'Opening Time':holding_date, 
                        'Type [buy/sell]':'BUY',
                        'Symbol': symbol,
                        'Size / Quantity':holding_quant,
                        'Closing Time':date,
                        'Entry Price':holding_price,
                        'Closing Price':price,
                        'Swap':np.nan,
                        # Implement fee*BNB/BTC vale
                        # In the meantime fee=0
                        #'Comission': holding_fe es + fees,
                        'Comission': 0,
                        'Net Profit':holding_pnl,}
                df_loop = pd.DataFrame(data, index=[0])
                df_closed_trades.append_dataframe(df_loop)
                quantity -= holding_quant
                holdings_lifo.pop(-x)
                len_holdings_lifo -= 1
                holding_symbol = holdings_lifo[-x].get_symbol()
                #holdings_lifo.remove(holding)
        #else: 
        x += 1                
    return df_closed_trades
            
                    
                    
# EXECUTION
       
df = pd.read_excel(r'C:\Users\danie\OneDrive\Desktop\daniel\edgewonk\edgewonk_data\binance_trade_history_24012021_31012021.xlsx', engine='openpyxl')
old_open_trades = pd.read_excel(r'C:\Users\danie\OneDrive\Desktop\daniel\edgewonk\edgewonk_data\open_trades.xlsx', engine='openpyxl')

i = 0

while i < old_open_trades.shape[0]:
    open_trade = trade_class(old_open_trades.iloc[i,0], old_open_trades.iloc[i,1], old_open_trades.iloc[i,2], old_open_trades.iloc[i,4], old_open_trades.iloc[i,3], old_open_trades.iloc[i,6])
    add_to_holdings(open_trade)
    i += 1
    
# Rename some columns
c = {'Date(UTC)':'Opening Time', 'Market':'Symbol', 'Type':'Type [buy/sell]', 'Amount':'Size / Quantity', 'Fee':'Comission'}
df = df.rename(columns=c)

# Change df['Opening Time'] type from string object to datetime type
df['Opening Time'] = pd.to_datetime(df['Opening Time'], infer_datetime_format=True)
df_tmp = df

# Create shifted columns for time, ticker and type
df_tmp['time(i-1)'] = df['Opening Time'].shift(+1)-timedelta(minutes=5)
df_tmp['ticker(i-1)'] = df['Symbol'].shift(+1)
df_tmp['type(i-1)'] = df['Type [buy/sell]'].shift(+1)

# Compare if datetime(i) is less than datetime(i+1)+5minutes 
df_tmp['time_bool'] = df['Opening Time'] >= df['time(i-1)']
# Compare if name of row i and i+1 is the same 
df_tmp['ticker_bool'] = df['Symbol'] == df['ticker(i-1)']
# Compare if type (buy/sell) of row i and i+1 is the same 
df_tmp['type_bool'] = df['Type [buy/sell]'] == df['type(i-1)']

# Create mask column if 3 conditions above are met
df_tmp['mask'] = df_tmp['time_bool'] & df_tmp['ticker_bool'] & df_tmp['type_bool']
# Create inverse mask column
df_tmp['inversed_mask'] = ~df_tmp['mask']
# Create inverse mask cumsum column
df_tmp['inversed_mask_cumsum'] = (~df_tmp['mask']).cumsum()

# group same trades using inversed_mask_cumsum column
g = df_tmp.groupby(df_tmp['inversed_mask_cumsum'])

# Create dataframe of trades using groups created above

columns = ['Opening Time', 'Type [buy/sell]', 'Symbol', 'Price', 'Size / Quantity', 'Comission']
df_trades = pd.DataFrame(index=[0], columns=columns)

for k, v in g:
    d = g.get_group(k)
    d_price = d.Price.mean()
    d_size = d['Size / Quantity'].sum()
    d_comission = d.Comission.sum()
    data = {'Opening Time':d.iloc[0,0], 
        'Type [buy/sell]': d.iloc[0,2],
        'Symbol':d.iloc[0,1],
        'Price':d_price,
        'Size / Quantity':d_size,
        'Comission':d_comission}
    df_loop = pd.DataFrame(data, index=[0])
    df_trades = df_trades.append(df_loop)

df_trades = df_trades.dropna()
df_trades = df_trades.iloc[::-1]
print(df_trades)


transaction_num = 1


df_closed_trades = closed_trades()
df_open_trades = open_trades()

for i in range(len(df_trades)):
    if ('BUY' == df_trades.iloc[i]).any():
        print ('Transaction #{} is a buy. Adding to HOLDINGS ...'.format(str(transaction_num)))
        print('Date: {}, Type: {}, Symbol: {}, Price: {}, Quantity: {}, Fees: {}'.format(df_trades.iloc[i,0], df_trades.iloc[i,1], df_trades.iloc[i,2], df_trades.iloc[i,3], df_trades.iloc[i,4], df_trades.iloc[i,5]))
        buy_trade = trade_class(df_trades.iloc[i,0], df_trades.iloc[i,1], df_trades.iloc[i,2], df_trades.iloc[i,3], df_trades.iloc[i,4], df_trades.iloc[i,5])
        add_to_holdings(buy_trade)
    elif ('SELL' == df_trades.iloc[i]).any():
        print ('Transaction #{} is a sell. Removing from HOLDINGS ...'.format(str(transaction_num)))
        print('Date: {}, Type: {}, Symbol: {}, Price: {}, Quantity: {}, Fees: {}'.format(df_trades.iloc[i,0], df_trades.iloc[i,1], df_trades.iloc[i,2], df_trades.iloc[i,3], df_trades.iloc[i,4], df_trades.iloc[i,5]))
        sell_trade = trade_class(df_trades.iloc[i,0], df_trades.iloc[i,1], df_trades.iloc[i,2], df_trades.iloc[i,3], df_trades.iloc[i,4], df_trades.iloc[i,5])
        remove_from_holdings_lifo(sell_trade)
    else:
        print('Transaction #{} is not a valid trade'.format(str(transaction_num)))
        
    transaction_num += 1

df_closed_trades.to_file()

columns = ['Opening Time', 'Type [buy/sell]', 'Symbol', 'Size / Quantity', 'Entry Price', 'Comission', 'Net Profit']
data = {'Opening Time':np.nan, 
                'Type [buy/sell]':'BUY',
                'Symbol': np.nan,
                'Size / Quantity':np.nan,
                'Entry Price':np.nan,
                'Swap':np.nan,
                # Implement fee*BNB/BTC vale
                # In the meantime fee=0
                #'Comission': holding_fees + fees,
                'Comission': np.nan,
                'Net Profit':np.nan,}
df_open_trades2 = pd.DataFrame(columns=columns)


len_holdings_lifo = len(holdings_lifo)
i = 1

# while len_holdings_lifo > i:
#     holding_symbol = holdings_lifo[-i].get_symbol()
#     holding_date = holdings_lifo[-i].get_date()
#     holding_quant = holdings_lifo[-i].get_quant()
#     holding_price = holdings_lifo[-i].get_price()
#     holding_fees = holdings_lifo[-i].get_fees()
#     holding_pnl = holdings_lifo[-i].get_pnl()
#     #if holding_quant > 0.0000000001:
#     data = {'Opening Time':holding_date, 
#             'Type [buy/sell]':'BUY',
#             'Symbol': holding_symbol,
#             'Size / Quantity':holding_quant,
#             'Entry Price':holding_price,
#             'Swap':np.nan,
#             # Implement fee*BNB/BTC vale
#             # In the meantime fee=0
#             #'Comission': holding_fees + fees,
#             'Comission': 0,
#             'Net Profit':holding_pnl,}
#     df_loop_open = pd.DataFrame(data, index=[0])
#     df_open_trades.append_dataframe(df_loop_open)
#     df_open_trades2 = df_open_trades2.append(df_loop_open)
#     #holdings_lifo.pop(-i)
#     i += 1
                    #holdings_lifo.remove(holding)
                    
for holding in holdings_lifo:
    holding_symbol = holdings_lifo[-i].get_symbol()
    holding_date = holdings_lifo[-i].get_date()
    holding_quant = holdings_lifo[-i].get_quant()
    holding_price = holdings_lifo[-i].get_price()
    holding_fees = holdings_lifo[-i].get_fees()
    holding_pnl = holdings_lifo[-i].get_pnl()
    #if holding_quant > 0.000000001:
    data = {'Opening Time':holding_date, 
            'Type [buy/sell]':'BUY',
            'Symbol': holding_symbol,
            'Size / Quantity':holding_quant,
            'Entry Price':holding_price,
            'Swap':np.nan,
            # Implement fee*BNB/BTC vale
            # In the meantime fee=0
            #'Comission': holding_fees + fees,
            'Comission': 0,
            'Net Profit':holding_pnl,}
    df_loop_open = pd.DataFrame(data, index=[0])
    df_open_trades.append_dataframe(df_loop_open)
    df_open_trades2 = df_open_trades2.append(df_loop_open)
    #holdings_lifo.pop(-i)
    i += 1
        
        
df_open_trades.to_file() 
df_open_trades2.to_excel(r'C:\Users\danie\OneDrive\Desktop\daniel\edgewonk\edgewonk_data\open_trades2.xlsx')


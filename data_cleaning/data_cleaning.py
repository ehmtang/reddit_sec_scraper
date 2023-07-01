import pandas as pd

# Clean and read active tickers as dataframe
with open('./exports/active_tickers_2023-04-26.txt', 'r+') as file:
    text = file.read().replace('\n', ', ').strip(', ')
    list_of_ticker = text.split(', ')
    list_of_ticker = [list_of_ticker[i:i+2] for i in range(0, len(list_of_ticker), 2)]    
    file.close()
df = pd.DataFrame(list_of_ticker)
print(df)

# Clean and read form4 as dataframe
with open('exports/form4_0001067983_2023-03-23.txt', '+r') as file:
    text = file.read().replace('\n', ', ').strip(', ')
    list_of_form4 = text.split(', ')
    list_of_form4 = [list_of_form4[i:i+8] for i in range(0, len(list_of_form4), 8)][:-1]    
    file.close()
df = pd.DataFrame(list_of_form4)
print(df)

# Read json file as a dataframe
df = pd.read_json('exports/wallstreetbets_headlines_2023-04-24.json')
print(df)
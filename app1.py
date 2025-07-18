# -- coding: utf-8 --
"""upstox-instrument-key.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SD0Y-lsU_o_ObalZlnyEaSPkfLkT5FJ4
"""

import pandas as pd

"""## json --> CSV"""

import json
import csv
import gzip
import requests
import base64


# URL to download the .json.gz file
url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.json.gz"
gz_filename = "complete.json.gz"
json_filename = "complete.json"
csv_filename = "output.csv"

# Step 1: Download the GZ file
response = requests.get(url)
with open(gz_filename, 'wb') as f:
    f.write(response.content)

# Step 2: Extract the GZ file
with gzip.open(gz_filename, 'rb') as f_in:
    with open(json_filename, 'wb') as f_out:
        f_out.write(f_in.read())

# Step 3: Load JSON data from the extracted file
with open(json_filename, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Step 4: Ensure data is a list
if isinstance(data, dict):
    data = [data]

# Step 5: Collect all unique keys across all dictionaries
all_keys = set()
for item in data:
    all_keys.update(item.keys())

# Convert set to list for CSV header
header = list(all_keys)

# Step 6: Write to CSV
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)

print(f"✅ Conversion complete! Saved as '{csv_filename}'")

"""# rest"""

import pandas as pd

# Read the CSV file
df = pd.read_csv('output.csv', low_memory=False)

# Convert expiry to datetime if needed
df['expiry'] = pd.to_datetime(df['expiry'], unit='ms')

# Filter only the required segments
allowed_segments = ['NSE_EQ', 'NSE_INDEX', 'NSE_FO', 'BSE_EQ', 'BSE_INDEX', 'BSE_FO']
df = df[df['segment'].isin(allowed_segments)].copy()

# Select only the required columns
required_columns = ['trading_symbol', 'name', 'instrument_key', 'expiry', 'exchange',
                    'instrument_type', 'lot_size', 'segment']
df = df[required_columns].copy()

# Create separate DataFrames for each segment
nse_eq_df = df[df['segment'] == 'NSE_EQ'].copy()
nse_index_df = df[df['segment'] == 'NSE_INDEX'].copy()
nse_fo_df = df[df['segment'] == 'NSE_FO'].copy()
bse_eq_df = df[df['segment'] == 'BSE_EQ'].copy()
bse_index_df = df[df['segment'] == 'BSE_INDEX'].copy()
bse_fo_df = df[df['segment'] == 'BSE_FO'].copy()

# Process NSE_EQ - instrument_key == option
nse_eq_df['option'] = nse_eq_df['instrument_key']

"""# nse + bse"""

# First handle NSE indices with more specific patterns first
nse_mappings = [
    ('NIFTY100 QUALTY30', 'NSE_INDEX|NIFTY100 Qualty30'),
    ('HANGSENG BEES-NAV', 'NSE_INDEX|HangSeng BeES-NAV'),
    ('NIFTY CONSUMPTION', 'NSE_INDEX|Nifty Consumption'),
    ('NIFTY RURAL', 'NSE_INDEX|Nifty Rural'),
    ('NIFTY COREHOUSING', 'NSE_INDEX|Nifty CoreHousing'),
    ('NIFTY REALTY', 'NSE_INDEX|Nifty Realty'),
    ('NIFTY100 ESG', 'NSE_INDEX|NIFTY100 ESG'),
    ('NIFTY EV', 'NSE_INDEX|Nifty EV'),
    ('NIFTY IT', 'NSE_INDEX|Nifty IT'),
    ('NIFTY PSE', 'NSE_INDEX|Nifty PSE'),
    ('NIFTY NEXT 50', 'NSE_INDEX|Nifty Next 50'),
    ('NIFTY IPO', 'NSE_INDEX|Nifty IPO'),
    ('INDIA VIX', 'NSE_INDEX|India VIX'),
    ('NIFTY MNC', 'NSE_INDEX|Nifty MNC'),
    ('NIFTY IND DIGITAL', 'NSE_INDEX|NIFTY IND DIGITAL'),
    ('NIFTY MICROCAP250', 'NSE_INDEX|NIFTY MICROCAP250'),
    ('NIFTY SML250 Q50', 'NSE_INDEX|Nifty Sml250 Q50'),
    ('NIFTY50 VALUE 20', 'NSE_INDEX|Nifty50 Value 20'),
    ('NIFTYM150MOMNTM50', 'NSE_INDEX|NiftyM150Momntm50'),
    ('NIFTY500 LMS EQL', 'NSE_INDEX|Nifty500 LMS Eql'),
    ('NIFTY500 QLTY50', 'NSE_INDEX|Nifty500 Qlty50'),
    ('NIFTY INDIA MFG', 'NSE_INDEX|NIFTY INDIA MFG'),
    ('NIFTY50 TR 2X LEV', 'NSE_INDEX|Nifty50 TR 2x Lev'),
    ('NIFTY100ESGSECLDR', 'NSE_INDEX|Nifty100ESGSecLdr'),
    ('NIFTY MULTI MQ 50', 'NSE_INDEX|Nifty Multi MQ 50'),
    ('NIFTY AQL 30', 'NSE_INDEX|Nifty AQL 30'),
    ('NIFTY500 LOWVOL50', 'NSE_INDEX|Nifty500 LowVol50'),
    ('NIFTY HIGHBETA 50', 'NSE_INDEX|Nifty HighBeta 50'),
    ('NIFTY200 ALPHA 30', 'NSE_INDEX|Nifty200 Alpha 30'),
    ('NIFTY FINSRV25 50', 'NSE_INDEX|Nifty FinSrv25 50'),
    ('NIFTY PVT BANK', 'NSE_INDEX|Nifty Pvt Bank'),
    ('NIFTY CONSR DURBL', 'NSE_INDEX|NIFTY CONSR DURBL'),
    ('NIFTY NEW CONSUMP', 'NSE_INDEX|Nifty New Consump'),
    ('NIFTY IND DEFENCE', 'NSE_INDEX|Nifty Ind Defence'),
    ('NIFTY100 LIQ 15', 'NSE_INDEX|Nifty100 Liq 15'),
    ('NIFTY LOW VOL 50', 'NSE_INDEX|Nifty Low Vol 50'),
    ('NIFTY GS 8 13YR', 'NSE_INDEX|Nifty GS 8 13Yr'),
    ('NIFTY OIL AND GAS', 'NSE_INDEX|NIFTY OIL AND GAS'),
    ('NIFTY TOP 10 EW', 'NSE_INDEX|Nifty Top 10 EW'),
    ('NIFTY CAPITAL MKT', 'NSE_INDEX|Nifty Capital Mkt'),
    ('NIFTY QLTY LV 30', 'NSE_INDEX|Nifty Qlty LV 30'),
    ('INDEX1 NSETEST', 'NSE_INDEX|INDEX1 NSETEST'),
    ('INDEX2 NSETEST', 'NSE_INDEX|INDEX2 NSETEST'),
    ('NIFTY PHARMA', 'NSE_INDEX|Nifty Pharma'),
    ('NIFTY GS 10YR CLN', 'NSE_INDEX|Nifty GS 10Yr Cln'),
    ('NIFTY AQLV 30', 'NSE_INDEX|Nifty AQLV 30'),
    ('NIFTYSML250MQ 100', 'NSE_INDEX|NiftySml250MQ 100'),
    ('NIFTY50 EQL WGT', 'NSE_INDEX|NIFTY50 EQL Wgt'),
    ('NIFTY TRANS LOGIS', 'NSE_INDEX|Nifty Trans Logis'),
    ('NIFTY500 MQVLV50', 'NSE_INDEX|Nifty500 MQVLv50'),
    ('NIFTY COMMODITIES', 'NSE_INDEX|Nifty Commodities'),
    ('NIFTY50 PR 1X INV', 'NSE_INDEX|Nifty50 PR 1x Inv'),
    ('NIFTY PSU BANK', 'NSE_INDEX|Nifty PSU Bank'),
    ('NIFTY50 DIV POINT', 'NSE_INDEX|Nifty50 Div Point'),
    ('NIFTY ALPHALOWVOL', 'NSE_INDEX|NIFTY AlphaLowVol'),
    ('NIFTY MIDSML 400', 'NSE_INDEX|NIFTY MIDSML 400'),
    ('NIFTY SMLCAP 50', 'NSE_INDEX|NIFTY SMLCAP 50'),
    ('NIFTY CORP MAATR', 'NSE_INDEX|Nifty Corp MAATR'),
    ('NIFTY200MOMENTM30', 'NSE_INDEX|Nifty200Momentm30'),
    ('NIFTY TOTAL MKT', 'NSE_INDEX|NIFTY TOTAL MKT'),
    ('NIFTY100 ENH ESG', 'NSE_INDEX|Nifty100 Enh ESG'),
    ('NIFTY GROWSECT 15', 'NSE_INDEX|Nifty GrowSect 15'),
    ('NIFTY200 QUALTY30', 'NSE_INDEX|NIFTY200 QUALTY30'),
    ('NIFTY LARGEMID250', 'NSE_INDEX|NIFTY LARGEMID250'),
    ('NIFTY MEDIA', 'NSE_INDEX|Nifty Media'),
    ('NIFTY HOUSING', 'NSE_INDEX|Nifty Housing'),
    ('NIFTY50 SHARIAH', 'NSE_INDEX|Nifty50 Shariah'),
    ('NIFTY CPSE', 'NSE_INDEX|Nifty CPSE'),
    ('NIFTY MIDCAP 50', 'NSE_INDEX|Nifty Midcap 50'),
    ('NIFTY500 SHARIAH', 'NSE_INDEX|Nifty500 Shariah'),
    ('NIFTY AUTO', 'NSE_INDEX|Nifty Auto'),
    ('NIFTY SHARIAH 25', 'NSE_INDEX|Nifty Shariah 25'),
    ('NIFTY MULTI MFG', 'NSE_INDEX|Nifty Multi Mfg'),
    ('NIFTY INFRA', 'NSE_INDEX|Nifty Infra'),
    ('NIFTY MIDSML HLTH', 'NSE_INDEX|Nifty MidSml Hlth'),
    ('NIFTY MS IND CONS', 'NSE_INDEX|Nifty MS Ind Cons'),
    ('NIFTY BANK', 'NSE_INDEX|Nifty Bank'),
    ('NIFTY GS COMPSITE', 'NSE_INDEX|Nifty GS Compsite'),
    ('NIFTY COMMODITIES-50', 'NSE_INDEX|Nifty Commodities-50'),
    ('NIFTY MOBILITY', 'NSE_INDEX|Nifty Mobility'),
    ('NIFTY DIV OPPS 50', 'NSE_INDEX|Nifty Div Opps 50'),
    ('NIFTY200 VALUE 30', 'NSE_INDEX|Nifty200 Value 30'),
    ('NIFTY ENERGY', 'NSE_INDEX|Nifty Energy'),
    ('NIFTY NONCYC CONS', 'NSE_INDEX|Nifty NonCyc Cons'),
    ('NIFTY MID SELECT', 'NSE_INDEX|NIFTY MID SELECT'),
    ('NIFTYMS400 MQ 100', 'NSE_INDEX|NiftyMS400 MQ 100'),
    ('NIFTY IND TOURISM', 'NSE_INDEX|Nifty Ind Tourism'),
    ('NIFTY500MOMENTM50', 'NSE_INDEX|Nifty500Momentm50'),
    ('BHARATBOND-APR31', 'NSE_INDEX|BHARATBOND-APR31'),
    ('BHARATBOND-APR32', 'NSE_INDEX|BHARATBOND-APR32'),
    ('BHARATBOND-APR30', 'NSE_INDEX|BHARATBOND-APR30'),
    ('BHARATBOND-APR33', 'NSE_INDEX|BHARATBOND-APR33'),
    ('NIFTY FIN SERVICE', 'NSE_INDEX|Nifty Fin Service'),
    ('NIFTY METAL', 'NSE_INDEX|Nifty Metal'),
    ('NIFTY500 EW', 'NSE_INDEX|Nifty500 EW'),
    ('NIFTY50 PR 2X LEV', 'NSE_INDEX|Nifty50 PR 2x Lev'),
    ('NIFTY MIDCAP 100', 'NSE_INDEX|NIFTY MIDCAP 100'),
    ('NIFTY MIDCAP 150', 'NSE_INDEX|NIFTY MIDCAP 150'),
    ('NIFTY 100', 'NSE_INDEX|Nifty 100'),
    ('NIFTY100 LOWVOL30', 'NSE_INDEX|NIFTY100 LowVol30'),
    ('NIFTY 200', 'NSE_INDEX|Nifty 200'),
    ('NIFTY MID LIQ 15', 'NSE_INDEX|Nifty Mid Liq 15'),
    ('NIFTY 500', 'NSE_INDEX|Nifty 500'),
    ('NIFTY MULTI INFRA', 'NSE_INDEX|Nifty Multi Infra'),
    ('NIFTY GS 15YRPLUS', 'NSE_INDEX|Nifty GS 15YrPlus'),
    ('NIFTY FINSEREXBNK', 'NSE_INDEX|Nifty FinSerExBnk'),
    ('NIFTY SERV SECTOR', 'NSE_INDEX|Nifty Serv Sector'),
    ('NIFTY100 ALPHA 30', 'NSE_INDEX|Nifty100 Alpha 30'),
    ('NIFTY TOP 20 EW', 'NSE_INDEX|Nifty Top 20 EW'),
    ('NIFTY500 VALUE 50', 'NSE_INDEX|Nifty500 Value 50'),
    ('NIFTY GS 10YR', 'NSE_INDEX|Nifty GS 10Yr'),
    ('NIFTY TATA 25 CAP', 'NSE_INDEX|Nifty Tata 25 Cap'),
    ('NIFTY SMLCAP 100', 'NSE_INDEX|NIFTY SMLCAP 100'),
    ('NIFTY SMLCAP 250', 'NSE_INDEX|NIFTY SMLCAP 250'),
    ('NIFTY FMCG', 'NSE_INDEX|Nifty FMCG'),
    ('NIFTY MS FIN SERV', 'NSE_INDEX|Nifty MS Fin Serv'),
    ('NIFTY TOP 15 EW', 'NSE_INDEX|Nifty Top 15 EW'),
    ('NIFTY500 MULTICAP', 'NSE_INDEX|NIFTY500 MULTICAP'),
    ('NIFTY HEALTHCARE', 'NSE_INDEX|NIFTY HEALTHCARE'),
    ('NIFTY GS 4 8YR', 'NSE_INDEX|Nifty GS 4 8Yr'),
    ('NIFTY M150 QLTY50', 'NSE_INDEX|NIFTY M150 QLTY50'),
    ('NIFTY100 EQL WGT', 'NSE_INDEX|NIFTY100 EQL Wgt'),
    ('NIFTY MS IT TELCM', 'NSE_INDEX|Nifty MS IT Telcm'),
    ('NIFTY GS 11 15YR', 'NSE_INDEX|Nifty GS 11 15Yr'),
    ('NIFTY50 TR 1X INV', 'NSE_INDEX|Nifty50 TR 1x Inv'),
    ('NIFTY ALPHA 50', 'NSE_INDEX|NIFTY Alpha 50'),
    ('NIFTY 50', 'NSE_INDEX|Nifty 50'),
]

# Now handle BSE indices with more specific patterns first
bse_mappings = [
    ('SENSEX50', 'BSE_INDEX|SENSEX50'),
    ('SENSEX', 'BSE_INDEX|SENSEX'),
    ('BANKEX', 'BSE_INDEX|BANKEX'),
    ('REALTY', 'BSE_INDEX|REALTY'),
    ('SNSX60', 'BSE_INDEX|SNSX60'),
    ('BS1000', 'BSE_INDEX|BS1000'),
    ('INTECO', 'BSE_INDEX|INTECO'),
    ('MFG', 'BSE_INDEX|MFG'),
    ('FOCMID', 'BSE_INDEX|FOCMID'),
    ('MIDCAP', 'BSE_INDEX|MIDCAP'),
    ('BSEDSI', 'BSE_INDEX|BSEDSI'),
    ('BSE500', 'BSE_INDEX|BSE500'),
    ('MID150', 'BSE_INDEX|MID150'),
    ('POWENE', 'BSE_INDEX|POWENE'),
    ('BSE100', 'BSE_INDEX|BSE100'),
    ('BSE200', 'BSE_INDEX|BSE200'),
    ('FOCIT', 'BSE_INDEX|FOCIT'),
    ('200EQW', 'BSE_INDEX|200EQW'),
    ('SS6535', 'BSE_INDEX|SS6535'),
    ('ESG100', 'BSE_INDEX|ESG100'),
    ('LRGCAP', 'BSE_INDEX|LRGCAP'),
    ('INDSTR', 'BSE_INDEX|INDSTR'),
    ('PSUBNK', 'BSE_INDEX|PSUBNK'),
    ('BHRT22', 'BSE_INDEX|BHRT22'),
    ('SMLCAP', 'BSE_INDEX|SMLCAP'),
    ('POWER', 'BSE_INDEX|POWER'),
    ('SNXT50', 'BSE_INDEX|SNXT50'),
    ('SML250', 'BSE_INDEX|SML250'),
    ('SNXN30', 'BSE_INDEX|SNXN30'),
    ('CONDIS', 'BSE_INDEX|CONDIS'),
    ('DFRGRI', 'BSE_INDEX|DFRGRI'),
    ('AUTO', 'BSE_INDEX|AUTO'),
    ('ENERGY', 'BSE_INDEX|ENERGY'),
    ('CAPINS', 'BSE_INDEX|CAPINS'),
    ('SELIPO', 'BSE_INDEX|SELIPO'),
    ('BSEPBI', 'BSE_INDEX|BSEPBI'),
    ('MSL400', 'BSE_INDEX|MSL400'),
    ('BSEPSU', 'BSE_INDEX|BSEPSU'),
    ('BSEQUI', 'BSE_INDEX|BSEQUI'),
    ('MIDSEL', 'BSE_INDEX|MIDSEL'),
    ('BSESER', 'BSE_INDEX|BSESER'),
    ('BSEEVI', 'BSE_INDEX|BSEEVI'),
    ('BSEFMC', 'BSE_INDEX|BSEFMC'),
    ('BSEIPO', 'BSE_INDEX|BSEIPO'),
    ('COMDTY', 'BSE_INDEX|COMDTY'),
    ('BSELVI', 'BSE_INDEX|BSELVI'),
    ('BSEMOI', 'BSE_INDEX|BSEMOI'),
    ('SMEIPO', 'BSE_INDEX|SMEIPO'),
    ('LCTMCI', 'BSE_INDEX|LCTMCI'),
    ('METAL', 'BSE_INDEX|METAL'),
    ('TECK', 'BSE_INDEX|TECK'),
    ('PRECON', 'BSE_INDEX|PRECON'),
    ('CPSE', 'BSE_INDEX|CPSE'),
    ('LMI250', 'BSE_INDEX|LMI250'),
    ('BBGEFS', 'BSE_INDEX|BBGEFS'),
    ('UTILS', 'BSE_INDEX|UTILS'),
    ('INFRA', 'BSE_INDEX|INFRA'),
    ('OILGAS', 'BSE_INDEX|OILGAS'),
    ('SMLSEL', 'BSE_INDEX|SMLSEL'),
    ('SENEQW', 'BSE_INDEX|SENEQW'),
    ('BSEHC', 'BSE_INDEX|BSEHC'),
    ('BSEIT', 'BSE_INDEX|BSEIT'),
    ('BSECG', 'BSE_INDEX|BSECG'),
    ('BSECD', 'BSE_INDEX|BSECD'),
    ('TELCOM', 'BSE_INDEX|TELCOM'),
    ('FINSER', 'BSE_INDEX|FINSER'),
]

"""# restt"""

for pattern, value in nse_mappings:
    mask = nse_index_df['name'].str.contains(pattern, case=False, na=False, regex=False)
    nse_index_df.loc[mask, 'option'] = value

# Map NSE_EQ names to instrument_keys
nse_eq_map = nse_eq_df.set_index('name')['instrument_key'].to_dict()
nse_fo_df['option'] = nse_fo_df['name'].map(nse_eq_map)

# Handle special index cases first (most specific to least specific)
nse_fo_df.loc[nse_fo_df['name'].str.contains('banknifty', case=False, na=False), 'option'] = 'NSE_INDEX|Nifty Bank'
nse_fo_df.loc[nse_fo_df['name'].str.contains('finnifty', case=False, na=False), 'option'] = 'NSE_INDEX|Nifty Fin Service'
nse_fo_df.loc[nse_fo_df['name'].str.contains('MIDCPNIFTY', case=False, na=False), 'option'] = 'NSE_INDEX|NIFTY MID SELECT'
nse_fo_df.loc[nse_fo_df['name'].str.contains('NIFTYNXT50', case=False, na=False), 'option'] = 'NSE_INDEX|Nifty Next 50'

# Only apply generic 'NIFTY' rule where not already assigned
nse_fo_df.loc[
    nse_fo_df['option'].isna() & nse_fo_df['name'].str.contains(r'\bNIFTY\b', case=False, na=False),
    'option'
] = 'NSE_INDEX|NIFTY 50'

# Process BSE_EQ - instrument_key == option
bse_eq_df['option'] = bse_eq_df['instrument_key']

bse_index_df['option'] = ''
for pattern, value in bse_mappings:
    mask = bse_index_df['name'].str.contains(pattern, case=True, na=True, regex=True)
    bse_index_df.loc[mask, 'option'] = value

# Process BSE_FO
bse_eq_map = bse_eq_df.set_index('name')['instrument_key'].to_dict()
bse_fo_df['option'] = bse_fo_df['name'].map(bse_eq_map)

# ✅ Special BSE_FO cases: Bankex and Sensex
bse_fo_df.loc[bse_fo_df['name'].str.contains('Bankex', case=False, na=False), 'option'] = 'BSE_INDEX|BANKEX'
bse_fo_df.loc[bse_fo_df['name'].str.contains('Sensex', case=False, na=False), 'option'] = 'BSE_INDEX|SENSEX'

import pandas as pd


# Combine all DataFrames
final_df = pd.concat([
    nse_eq_df, nse_index_df, nse_fo_df,
    bse_eq_df, bse_index_df, bse_fo_df
], ignore_index=True)

# Sort by expiry
final_df = final_df.sort_values(by='expiry')
final_df = final_df[['trading_symbol', 'name', 'instrument_key','expiry' ,'exchange', 'instrument_type', 'option','lot_size']]
# Save to single CSV file
final_df.to_csv('data.csv', index=False)

# Download the combined file
#files.download('data.csv')

"""# currency"""

df3 = pd.read_csv('output.csv', low_memory=False)
df3 = df3[df3['underlying_type'].fillna('') == 'CUR']

# Add 'option' column
df3['option'] = df3['instrument_key']

# Select and reorder columns
df3 = df3[['trading_symbol', 'name', 'instrument_key', 'expiry', 'exchange', 'instrument_type', 'option', 'lot_size']]

# Save to CSV
df3.to_csv('curr.csv', index=False)

df3.shape

"""# mcx"""

import json
import csv
import gzip
import requests

# URL to download the .json.gz file
url = "https://assets.upstox.com/market-quote/instruments/exchange/MCX.json.gz"
gz_filename = "complete.json.gz"
json_filename = "complete.json"
csv_filename = "mcx.csv"

# Step 1: Download the GZ file
response = requests.get(url)
with open(gz_filename, 'wb') as f:
    f.write(response.content)

# Step 2: Extract the GZ file
with gzip.open(gz_filename, 'rb') as f_in:
    with open(json_filename, 'wb') as f_out:
        f_out.write(f_in.read())

# Step 3: Load JSON data from the extracted file
with open(json_filename, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Step 4: Ensure data is a list
if isinstance(data, dict):
    data = [data]

# Step 5: Collect all unique keys across all dictionaries
all_keys = set()
for item in data:
    all_keys.update(item.keys())

# Convert set to list for CSV header
header = list(all_keys)

# Step 6: Write to CSV
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)

print(f"✅ Conversion complete! Saved as '{csv_filename}'")

df1 = pd.read_csv('mcx.csv')
df1['option'] = df1['instrument_key']
df1 = df1 [['trading_symbol', 'name', 'instrument_key','expiry' ,'exchange', 'instrument_type', 'option','lot_size']]
df1.to_csv('mcs.csv', index = False)
#

combined_df = pd.concat([final_df, df1,df3], ignore_index=True)
combined_df.to_csv('combined.csv', index=False)
print("done")




# === Replace these values ===
import requests
import base64
import os

# === Replace these values ===
GITHUB_USERNAME = "shreyai347"
REPO = "api-data"
FILE_PATH = "in.csv"
LOCAL_FILE = "combined.csv"
COMMIT_MESSAGE = "Auto update in.csv from GitHub Actions"

# ✅ Securely get token from GitHub Action secret
GITHUB_TOKEN = os.getenv("PAT_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("❌ GitHub token not found. Set 'PAT_TOKEN' as a secret in your repository.")

# 1. Read local CSV
with open(LOCAL_FILE, "rb") as file:
    content = file.read()
    encoded_content = base64.b64encode(content).decode("utf-8")

# 2. Get current file SHA from GitHub
get_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO}/contents/{FILE_PATH}"
headers = {"Authorization": f"token {GITHUB_TOKEN}"}
get_response = requests.get(get_url, headers=headers)
get_response.raise_for_status()
file_sha = get_response.json()["sha"]

# 3. Prepare payload for update
payload = {
    "message": COMMIT_MESSAGE,
    "content": encoded_content,
    "sha": file_sha,
    "branch": "main"
}

# 4. Push update to GitHub
put_response = requests.put(get_url, headers=headers, json=payload)

if put_response.status_code in [200, 201]:
    print("✅ File updated successfully on GitHub.")
else:
    print("❌ Failed to update file:", put_response.status_code)
    print(put_response.json())

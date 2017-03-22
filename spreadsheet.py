import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('corporate_client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Corporate / Society Benefits')

worksheet = sheet.worksheet("Companies")

companies = worksheet.col_values(1)

print(companies)
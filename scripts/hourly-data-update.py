import pandas as pd
import tabula
import datetime
import os
from deta import Deta
from dotenv import load_dotenv

load_dotenv()

deta = Deta(os.environ.get("DETA_PROJECT_KEY"))

data = deta.Drive("data")

columns = [
    "Date",
    "Time",
    "Stretcher Pts hrly",
    "Stretcher Pts cum",
    "Ambulatory Pts hrly",
    "Ambulatory Pts cum",
    "Total Inflow hrly",
    "Total Inflow cum",
    "Ambulances hrly",
    "Ambulances cum",
    "FLS hrly",
    "Adm. requests cum",
    "Admissions cum",
    "Pts.waiting for admission CUM",
    "Triage hallway pts TBS",
    "Re-Oriented Nurse cum",
    "Re-Oriented MD QTrack D/C",
    "Re-Oriented MD QTrack NotD/C",
    "Resus Pts",
    "Totalpts in PODs except Psych",
    "Green Pts",
    "Green Pts TBS",
    "Yellow PTS",
    "Yellow Pts TBS",
    "Orancge Pts except psych",
    "Orange Pts TBS",
    "Consults > 2h in PODS except IM",
    "Consult for IM >4h in PODS",
    "Plain films reqs > 2 h in PODs",
    "CTs reqs > 2 h in PODs",
    "Post POD (Family room)",
    "Stretcher Pts in Vertical",
    "Stretcher Pts TBS in Vertical",
    "Stretcher Pts in Vertical on Lazyboy",
    "Vertical Pts Waiting for Results",
    "Ambulatory Pts in Vertical",
    "Ambulatory Pts TBS in Vertical",
    "QTrack Patients TBS",
    "GARAGE patient TBS",
    "Consults > 2h in Vertical Except IM",
    "Consult for IM >4h in Vertical",
    "Plain films reqs > 2 hr in Vertical",
    "CTs reqs > 2 hrs in Vertical",
    "Psych Stretcher Pts1pt",
    "Psych pts waiting for admission",
]

url = "https://www.dropbox.com/s/ckijmipu33z3feg/HourlyReport.pdf?dl=1"
output = []
first_row = tabula.read_pdf(
    url, pages=1, area=[[200, 6, 206, 1002]], silent=True)[0]
first_row = first_row.columns.tolist()
first_row_dict = dict(zip(columns, first_row))
output.append(first_row_dict)
first_row_date = first_row_dict['Date']
for row_start in [211, 223, 235, 247, 259, 271, 283]:
    try:
        new_row = tabula.read_pdf(
            url, pages=1, area=[[row_start, 0, row_start+7, 1002]], silent=True)[0]
        new_row = new_row.columns.tolist()
        new_row.insert(0, first_row_date)
        new_row_dict = dict(zip(columns, new_row))
        output.append(new_row_dict)
    except:
        break

output_df = pd.DataFrame(output)

missing_columns = []
first_row = tabula.read_pdf(
    url, pages=1, area=[[200, 308, 215, 341]], silent=True)[0]
first_row = first_row.columns.tolist()
first_row_dict = dict(
    zip(['Total Stretcher pts', 'Triage hallway pts'], first_row))
missing_columns.append(first_row_dict)
for row_start in [212, 224, 236, 248, 260, 272, 284]:
    try:
        new_row = tabula.read_pdf(
            url, pages=1, area=[[row_start, 308, row_start+8, 341]], silent=True)[0]
        new_row = new_row.columns.tolist()
        new_row_dict = dict(
            zip(['Total Stretcher pts', 'Triage hallway pts'], new_row))
        missing_columns.append(new_row_dict)
    except:
        break
missing_columns_df = pd.DataFrame(missing_columns)

output_df = pd.concat([output_df, missing_columns_df], axis=1)
output_df = output_df.dropna()

newColumns = [
    "Date",
    "Time",
    "Stretcher Pts hrly",
    "Stretcher Pts cum",
    "Ambulatory Pts hrly",
    "Ambulatory Pts cum",
    "Total Inflow hrly",
    "Total Inflow cum",
    "Ambulances hrly",
    "Ambulances cum",
    "FLS hrly",
    "Adm. requests cum",
    "Admissions cum",
    "Pts.waiting for admission CUM",
    "Total Stretcher pts",
    "Triage hallway pts",
    "Triage hallway pts TBS",
    "Re-Oriented Nurse cum",
    "Re-Oriented MD QTrack D/C",
    "Re-Oriented MD QTrack NotD/C",
    "Resus Pts",
    "Totalpts in PODs except Psych",
    "Green Pts",
    "Green Pts TBS",
    "Yellow PTS",
    "Yellow Pts TBS",
    "Orancge Pts except psych",
    "Orange Pts TBS",
    "Consults > 2h in PODS except IM",
    "Consult for IM >4h in PODS",
    "Plain films reqs > 2 h in PODs",
    "CTs reqs > 2 h in PODs",
    "Post POD (Family room)",
    "Stretcher Pts in Vertical",
    "Stretcher Pts TBS in Vertical",
    "Stretcher Pts in Vertical on Lazyboy",
    "Vertical Pts Waiting for Results",
    "Ambulatory Pts in Vertical",
    "Ambulatory Pts TBS in Vertical",
    "QTrack Patients TBS",
    "GARAGE patient TBS",
    "Consults > 2h in Vertical Except IM",
    "Consult for IM >4h in Vertical",
    "Plain films reqs > 2 hr in Vertical",
    "CTs reqs > 2 hrs in Vertical",
    "Psych Stretcher Pts1pt",
    "Psych pts waiting for admission",
]
output_df = output_df[newColumns]
for column in output_df.columns.tolist():
    if column in ['Date']:
        continue
    output_df[column] = output_df[column].astype('float').astype('int')

output_df["ds"] = pd.to_datetime(
    output_df["Date"] + " " + (output_df["Time"] - 1).astype(str) + ":00") + datetime.timedelta(hours=1)

output_df['Total Pod TBS'] = output_df['Green Pts TBS'] + \
    output_df['Yellow Pts TBS']+output_df['Orange Pts TBS'] + \
    output_df["Triage hallway pts TBS"]
output_df['Total Vertical TBS'] = output_df['Stretcher Pts TBS in Vertical'] + \
    output_df['Ambulatory Pts TBS in Vertical'] + \
    output_df['QTrack Patients TBS']+output_df['GARAGE patient TBS']
output_df['Stretcher Overflow'] = output_df["Triage hallway pts TBS"] + \
    output_df["Post POD (Family room)"]

since2020_df = pd.read_csv("data/since-2020.csv")
since2020_df.ds = pd.to_datetime(since2020_df.ds)

since2020_df = pd.concat([since2020_df, output_df], ignore_index=True)

since2020_df = since2020_df.drop_duplicates(
    subset='ds', keep="last").sort_values(by=['ds'], ascending=True)

since2020_df.to_csv("data/since-2020.csv", index=False)
# since2020_df.to_excel("data/since-2020.xlsx", index=False)
since2020_df.head(14*24).to_csv("data/recent.csv", index=False)
since2020_df.head(1).to_csv('data/current.csv', index=False)


for file in ['since-2020.csv', 'recent.csv', 'current.csv']:
    data.put(file, path='data/'+file)

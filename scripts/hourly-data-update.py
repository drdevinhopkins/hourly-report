import pandas as pd
import tabula

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

url = "https://www.dropbox.com/s/2y4xn6hbqgzop8y/HourlyReport.pdf?dl=1"
df = tabula.read_pdf(url, pages=1, area=[[190, 6, 206, 1002]])[0]
df.columns = columns

df2 = tabula.read_pdf(url, pages=1, area=[[190, 308, 215, 341]])[0]

df3 = pd.DataFrame(
    [{"Total Stretcher pts": df2.columns[0], "Triage hallway pts": df2.columns[1]}]
)

df4 = pd.concat([df, df3], axis=1)

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
df5 = df4[newColumns]

df5.to_csv("data/current.csv", index=False)

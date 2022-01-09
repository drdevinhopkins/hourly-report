import pandas as pd
import tabula
import dropbox

import os
import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata
import dropbox

dropbox_api_key = os.environ["DROPBOX_API_KEY"]
dbx = dropbox.Dropbox(dropbox_api_key)
dbx.users_get_current_account()
print("connected to dropbox")


def upload(dbx, fullname, folder, subfolder, name, overwrite=False):

    # from datetime import date, timedelta

    """Upload a file.
    Return the request response, or None in case of error.
    """
    path = "/%s/%s/%s" % (folder, subfolder.replace(os.path.sep, "/"), name)
    while "//" in path:
        path = path.replace("//", "/")
    mode = (
        dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add
    )
    mtime = os.path.getmtime(fullname)
    with open(fullname, "rb") as f:
        data = f.read()
    # with stopwatch('upload %d bytes' % len(data)):
    try:
        res = dbx.files_upload(
            data,
            path,
            mode,
            client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
            mute=True,
        )
    except dropbox.exceptions.ApiError as err:
        print("*** API error", err)
        return None
    print("uploaded as", res.name.encode("utf8"))
    return res


def download(dbx, folder, subfolder, name):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """
    path = "/%s/%s/%s" % (folder, subfolder.replace(os.path.sep, "/"), name)
    while "//" in path:
        path = path.replace("//", "/")
    try:
        md, res = dbx.files_download(path)
    except dropbox.exceptions.HttpError as err:
        print("*** HTTP error", err)
        return None
    data = res.content
    print(len(data), "bytes; md:", md)
    with open(name, "wb") as f:
        f.write(res.content)
    return data


def list_folder(dbx, folder, subfolder):
    """List a folder.
    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = "/%s/%s" % (folder, subfolder.replace(os.path.sep, "/"))
    while "//" in path:
        path = path.replace("//", "/")
    path = path.rstrip("/")
    try:
        res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print("Folder listing failed for", path, "-- assumed empty:", err)
        return {}
    else:
        # rv = {}
        # for entry in res.entries:
        #     rv[entry.name] = entry
        # return rv
        rv = []
        for entry in res.entries:
            rv.append(entry)
        return rv


download(dbx, "jgh-ed-hourly-report", "", "HourlyReport.pdf")

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

url = "HourlyReport.pdf"
df = tabula.read_pdf(url, pages=1, area=[[190, 6, 206, 1002]], silent=True)[0]
df.columns = columns

df2 = tabula.read_pdf(url, pages=1, area=[[190, 308, 215, 341]], silent=True)[0]

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

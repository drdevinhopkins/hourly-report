df = pd.read_csv("https://www.dropbox.com/s/dl8gumtaqq2vrfw/concat.csv?dl=1")
df["time"] = df["timeflg"] - 1
df["ds"] = pd.to_datetime(df.dateflg + " " + df["time"].apply(str) + ":00")
df.set_index("ds", inplace=True)
df = df[["INFLOW_STRETCHER", "INFLOW_AMBULATORY", "Inflow_Total", "INFLOW_AMBULANCES"]]
df.tail()

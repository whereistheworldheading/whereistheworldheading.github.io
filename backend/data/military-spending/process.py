import pandas as pd
import json

input_filename = "SIPRI-Milex-data-1949-2016.csv"
output_filename = "list_data"

to_print = False

log_dict = {}
areas_names = ["Middle East", "Europe", "Asia & Oceania", "Americas", "Africa"]

df = pd.read_csv(input_filename, skiprows=5)
for row in df.iterrows() :
  area_name = row[1]["Country"]
  if area_name in areas_names :
    spendings = row[1].iloc[5:-1].as_matrix().astype(float) / 1000
    log_dict[area_name] = list(spendings.astype(str))
log_dict["years"] = list(df.columns.values[5:-1])
log_dict["info"] = "2015 billion USD"

log_dict["Worldwide"] = [str(sum([float(log_dict[area][i]) for area in areas_names]))
                      for i in range(len(log_dict["years"]))]

with open(output_filename, 'w') as outfile:
    json.dump(log_dict, outfile, sort_keys=True)
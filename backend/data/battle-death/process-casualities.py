import pandas as pd
from collections import Counter
import json

input_filename = "PRIO Battle Deaths Dataset 3.1.csv"
output_filename = "list_data"

regions_mappings = {"1" : "Europe",
                    "2" : "Middle East",
                    "3": "Asia & Oceania",
                    "4" : "Africa",
                    "5":"Americas"}

to_print = False

def region_counter(df, region) :
  counter = Counter()
  for row in df.iterrows():
    if row[1]["region"] == region or region is None :
      curr_battle_deaths = row[1]["bdeadhig"]
      curr_year = row[1]["year"]
      counter[curr_year] += curr_battle_deaths
  return counter

def all_regions_counter(df):
  regions_counters = {}
  for region in range(1,6):
    region_name = regions_mappings[str(region)]
    regions_counters[region_name] = counter_to_lists(region_counter(df, region))
  return regions_counters

def counter_to_lists(counter):
  pairs = [item for item in counter.items()]
  years = [pair[0] for pair in pairs]
  values = [pair[1] for pair in pairs]
  return {"years": years, "values" : values}


def log_lists(output_filename, lists) :
  with open(output_filename, "w+") as f :
    for list in lists :
      f.write(str(list))
      f.write('\n')

def postprocess(log_dict) :
  new_dict = {}

  for key, item in log_dict.items():
    all_years, all_values = postprocess_pair(years=item["years"],
                                             values=item["values"])
    new_dict[key] = {"years": all_years,
                     "values": all_values}
  return new_dict

def compute_worldwide(values_list) :
  worldwide = [sum([values[i] for values in values_list
                    if values[i] is not "NaN"])
               for i in range(len(values_list[0]))]
  return worldwide


def add_worldwide(log_dict):
  values_list = [item["values"] for key, item in log_dict.items()]

  log_dict["Wordlwide"] = {}
  log_dict["Wordlwide"]["years"] = log_dict["Europe"]["years"]

  log_dict["Wordlwide"]["values"] = compute_worldwide(values_list)
  return log_dict

def postprocess_pair(years, values):
  all_values = []
  all_years = [year for year in range(1946, 2009)]

  year_tracker = 0
  for i in range(len(years)) :
    while years[i] != all_years[year_tracker]:
      all_values.append("NaN")
      year_tracker += 1
    all_values.append(values[i])
    year_tracker += 1
  return all_years, all_values
# postprocess_pair(years, values)

df = pd.read_csv(input_filename)
log_dict = all_regions_counter(df)
log_dict = postprocess(log_dict)
log_dict = add_worldwide(log_dict)

with open(output_filename, 'w') as outfile:
  json.dump(log_dict, outfile, sort_keys=True)




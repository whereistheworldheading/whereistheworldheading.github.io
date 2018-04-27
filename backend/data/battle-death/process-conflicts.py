import pandas as pd
import json

from collections import Counter

input_filename = "PRIO Battle Deaths Dataset 3.1.csv"
output_filename = "list_data_conflicts"

conflicts_mappings = {
  "1" : "Extrasystemic armed conflict",
  "2" : "Interstate armed conflict",
  "3": "Civil war",
  "4" : "Internationalized internal armed conflict"
    }


to_print = False

def postprocess_pair(years, values):
  all_values = []
  all_years = [year for year in range(1946, 2009)]

  year_tracker = 0
  i = 0
  while i < len(all_years) :
    if year_tracker < len(years) :
      while all_years[i] != years[year_tracker]:
        all_values.append("NaN")
        i+= 1
      all_values.append(values[year_tracker])
      year_tracker += 1
      i += 1
    else :
      all_values.append("NaN")
      i += 1
  return all_years, all_values

# years = [1947, 1955]
# values = [11, 15]
# postprocess_pair(years, values)

def global_counter(df, confilct) :
  death_counter = Counter()
  conflict_counter = Counter()

  for row in df.iterrows():
    if row[1]["type"] == confilct or confilct is None :
      curr_battle_deaths = row[1]["bdeadhig"]
      curr_year = row[1]["year"]
      death_counter[curr_year] += curr_battle_deaths
      conflict_counter[curr_year] += 1
  return death_counter, conflict_counter

def counter_to_list(counter):
  pairs = [item for item in counter.items()]
  years = [pair[0] for pair in pairs]
  values = [pair[1] for pair in pairs]
  all_years, all_values = postprocess_pair(years, values)
  return all_values

def all_conflicts_dicts(df):
  conflicts_dicts = {}
  for conflict in range(1, 5):
    conflict_dict = {}
    conflict_name = conflicts_mappings[str(conflict)]
    death_counter, conflict_counter = global_counter(df, conflict)
    conflict_dict["years"] = [year for year in range(1946, 2009)]
    conflict_dict["deaths"] = counter_to_list(death_counter)
    conflict_dict["counts"] = counter_to_list(conflict_counter)
    conflicts_dicts[conflict_name] = conflict_dict
  return conflicts_dicts

def compute_global(values_list) :
  total = [sum([values[i] for values in values_list
                    if values[i] is not "NaN"])
               for i in range(len(values_list[0]))]
  return total


def add_total(log_dict):
  values_list_deaths = [item["deaths"] for key, item in log_dict.items()]
  values_list_counts = [item["counts"] for key, item in log_dict.items()]

  log_dict["Total"] = {}
  log_dict["Total"]["years"] = log_dict[conflicts_mappings["1"]]["years"]
  log_dict["Total"]["deaths"] = compute_global(values_list_deaths)
  log_dict["Total"]["counts"] = compute_global(values_list_counts)
  return log_dict


df = pd.read_csv(input_filename)
log_dict = all_conflicts_dicts(df)
log_dict = add_total(log_dict)

with open(output_filename, 'w') as outfile:
  json.dump(log_dict, outfile, sort_keys=True)

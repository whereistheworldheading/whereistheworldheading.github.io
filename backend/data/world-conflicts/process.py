import pandas as pd
from collections import Counter

input_filename = "MainConflictTable.csv"
output_filename = "list_data"

to_print = False

df = pd.read_csv(input_filename)
years = list(df["YEAR"].as_matrix())

# Extract the number of conflicts occurences in the years
year_occurences_count = Counter(years)

# Extract the number of conflicts starting in the year
prev_id = 0
starting_conflicts_counter = Counter()
for row in df.iterrows() :
  curr_id = row[1]["ID"]
  if curr_id != prev_id :
    curr_year = row[1]["YEAR"]
    starting_conflicts_counter[curr_year] += 1
    prev_id = curr_id

# Log data
conflicts_occurences_pairs = [item for item in year_occurences_count.items()]
conflicts_occurences_years = [pair[0] for pair in conflicts_occurences_pairs]
conflicts_occurences_ongoing = [pair[1] for pair in conflicts_occurences_pairs]

with open(output_filename, "w+") as f:
  f.write(str(conflicts_occurences_years))
  f.write("\n")
  f.write(str(conflicts_occurences_ongoing))


conflicts_occurences_pairs = [item for item in starting_conflicts_counter.items()]
conflicts_occurences_years = [pair[0] for pair in conflicts_occurences_pairs]
conflicts_occurences_started = [pair[1] for pair in conflicts_occurences_pairs]

with open(output_filename, "w+") as f:
  f.write(str(conflicts_occurences_years))
  f.write("\n")
  f.write(str(conflicts_occurences_started))
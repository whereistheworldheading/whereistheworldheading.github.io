from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import csv


import itertools

import pandas as pd


def tokenize_headlines(headlines) :
  return [headline.split()
          for headline in headlines]


def filter_headlines(headlines, keywords):
  candidate_indexes = [[i for i in range(len(headlines)) if keyword in headlines[i]]
                       for keyword in keywords]
  unique_indexes = list(set().union(*candidate_indexes))
  return [headlines[i] for i in unique_indexes]


def remove_stopwords(headlines) :
  stop_words = list(get_stop_words('en'))
  nltk_words = list(stopwords.words('english'))
  stop_words.extend(nltk_words)

  return [[word for word in headline if word not in stop_words ]
          for headline in headlines]


def export(data, data_name):
  csv_filename = data_name + ".csv"
  with open(csv_filename, 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['name', 'count'])
    for row in data:
      csv_out.writerow(row)


input_filename = "abcnews-date-text.csv"
output_filename = "list_data_conflicts"

df = pd.read_csv(input_filename)
headlines = list(df["headline_text"].as_matrix())

keywords = ["refugee", "cyber"]

tokenized_headlines = tokenize_headlines(headlines)

for keyword in keywords :
  filtered_headlines = remove_stopwords(filter_headlines(tokenized_headlines, [keyword]))
  tokens = list(itertools.chain.from_iterable(filtered_headlines))
  distribution = FreqDist(tokens)
  most_common = distribution.most_common(70)
  export(data=most_common, data_name=keyword)

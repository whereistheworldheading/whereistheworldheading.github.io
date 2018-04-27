input_filenames = ["refugee/API_SM.POP.REFG.OR_DS2_en_csv_v2.csv",
                   "military-spending/SIPRI-Milex-data-1949-2016.csv"]
output_filename = "logs/" + "list_data"

to_print = False

with open("data/csv/" + input_filenames[1]) as f:
    data = [line.split(',') for line in f]

with open(output_filename, "w") as f:
    labels = str(data[5][3:-1])
    values = str(data[198][3:-1])
    if to_print :
        print(labels + "\n" + values)
    else :
        f.write(labels)
        f.write("\n")
        f.write(values)
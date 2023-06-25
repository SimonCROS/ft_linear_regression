# import seaborn
# import pandas
# import matplotlib.pyplot as plt
import csv

# res = seaborn.scatterplot(x="km", y="price", data=csv)
# plt.show()

with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]}km is for {row[1]}$.')
            line_count += 1
    print(f'Processed {line_count} lines.')

print(csv)
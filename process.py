import csv
import os

# Input files in the data folder
input_files = [
    'data/daily_sales_data_0.csv',
    'data/daily_sales_data_1.csv',
    'data/daily_sales_data_2.csv'
]

output_file = 'data/output.csv'

with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    # Write header
    writer.writerow(['sales', 'date', 'region'])

    for filepath in input_files:
        with open(filepath, 'r') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                # Only keep Pink Morsels
                if row['product'] != 'pink morsel':
                    continue
                # Calculate sales (remove $ from price first)
                price = float(row['price'].replace('$', ''))
                quantity = int(row['quantity'])
                sales = price * quantity
                writer.writerow([sales, row['date'], row['region']])

print("Done! Output written to", output_file)
import csv

def csv_to_dict(csv_file):
    slang_to_formal = {}
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            slang_to_formal[row[0].strip()] = row[1].strip()
    return slang_to_formal

def save_as_python_file(dictionary, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("slang_to_formal = {\n")
        for key, value in dictionary.items():
            file.write(f'    "{key}": "{value}",\n')
        file.write("}\n")

# Replace 'input.csv' with the path to your CSV file and 'output.py' with the desired output filename.
csv_file = 'Kamus_Baku.csv'
output_file = 'output.py'

# Convert CSV to dictionary and save as a Python file.
dictionary = csv_to_dict(csv_file)
save_as_python_file(dictionary, output_file)

print(f"Dictionary saved to {output_file}")

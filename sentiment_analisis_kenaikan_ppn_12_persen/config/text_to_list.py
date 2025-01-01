def txt_to_list(txt_file, output_file, items_per_row=10):
    with open(txt_file, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file if line.strip()]  # Read and clean each line

    # Create a formatted Python list with the specified number of items per row
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("words_list = [\n")
        for i in range(0, len(words), items_per_row):
            chunk = words[i:i + items_per_row]
            output.write("    " + ", ".join(f'"{word}"' for word in chunk) + ",\n")
        output.write("]\n")

    print(f"List saved to {output_file}")

# Replace 'input.txt' with the path to your text file and 'output.py' with the desired output filename.
txt_file = 'netral.txt'
output_file = 'output.py'

# Convert TXT to list and save as a Python file.
txt_to_list(txt_file, output_file)

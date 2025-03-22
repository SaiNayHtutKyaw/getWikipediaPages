import re

input_file = "ErrorTitle-2016-2024.txt"  # Your input file
output_file = "error_titles.txt"  # Output file to save titles

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        # Use regex to find the first column (title) before the first occurrence of numbers
        match = re.match(r"^(.*?),(?:\d+.*)$", line)
        if match:
            first_column = match.group(1)  # Extract the title
            outfile.write(first_column + "\n")  # Write to the new file

print(f"Titles saved to {output_file}")

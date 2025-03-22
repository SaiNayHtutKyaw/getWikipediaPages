import re

def filter_titles(input_file_path, output_file_path, threshold=100):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile, \
             open(output_file_path, 'w', encoding='utf-8') as outfile:

            for line in infile:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                parts = line.split(',')
                
                # The title is everything before the first number
                title_end_idx = next((i for i, part in enumerate(parts) if re.match(r"^\d+$", part)), None)
                
                if title_end_idx is None:
                    print(f"Skipping invalid line (no numeric values found): {line}")
                    continue  # Skip invalid lines
                
                title = ','.join(parts[:title_end_idx])  # Keep original title
                
                # Exclude titles containing "/"
                if "/" in title:
                    continue
                
                # Extract view counts
                view_counts = [int(x) for x in parts[title_end_idx:] if x.isdigit()]

                # Check if at least one day exceeds the threshold
                if any(count > threshold for count in view_counts):
                    outfile.write(line + '\n')  # Write the original line unchanged

        print(f"Filtered titles saved to {output_file_path}")

    except Exception as e:
        print(f"Error occurred: {e}")

# Set file paths
input_file_path = "th-dataset-2024-01-01_2024-12-31.txt"
output_file_path = "filtered_th-dataset-2024.txt"

# Run filtering function
filter_titles(input_file_path, output_file_path)

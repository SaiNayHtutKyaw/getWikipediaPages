import re

def filter_titles(input_file_path, output_file_path, excluded_file_path, threshold=100):
    passed_titles = []  # Stores titles that passed the 100 views threshold

    # Step 1: Filter titles with at least 100 views on one day in a year
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            parts = line.strip().split(',')
            
            # Identify where the view counts start
            title = None
            view_counts = []

            for i, part in enumerate(parts):
                if re.match(r"^\d+$", part):  # Find first numeric value (view count)
                    title = ','.join(parts[:i])  # Preserve original title formatting
                    view_counts = [int(x) for x in parts[i:] if x.isdigit()]
                    break
            else:
                print(f"Skipping invalid line (no numeric values found): {line.strip()}")
                continue  

            # ✅ Step 1: Keep only titles where at least one day's view count > threshold
            if any(count > threshold for count in view_counts):
                passed_titles.append(title)

    # Step 2: Separate the passed titles into two files
    with open(output_file_path, 'w', encoding='utf-8') as outfile, \
         open(excluded_file_path, 'w', encoding='utf-8') as exfile:

        for title in passed_titles:
            if "/" in title:
                exfile.write(title + '\n')  # Titles with "/"
            else:
                outfile.write(title + '\n')  # Titles without "/"

# Set file paths
input_file_path = "filtered_th-dataset-2024.txt"
output_file_path = "titles_only2.txt"  # Titles that passed & do NOT contain "/"
excluded_file_path = "excluded_titles2.txt"  # Titles that passed & DO contain "/"

# Run filtering function
filter_titles(input_file_path, output_file_path, excluded_file_path)

print(f"Filtered titles (without '/') saved to {output_file_path}")
print(f"Excluded titles (with '/') saved to {excluded_file_path}")

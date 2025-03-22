def extract_titles_from_links(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            parts = line.strip().split("\t")  # Split by tab
            if len(parts) == 2 and parts[1] != "None":  # Ensure a valid link exists
                title = parts[1].split("/")[-1]  # Extract title from URL
                outfile.write(title + "\n")  # Write to output file

# Example Usage
input_filepath = "Thai_important_titles_to_English.txt"  # Replace with your file
output_filepath = "English_titles.txt"
extract_titles_from_links(input_filepath, output_filepath)

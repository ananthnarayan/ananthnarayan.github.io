import os
import csv
import re

def extract_sukta_names(folder_path):
    output_rows = []

    for mandala_num in range(1, 11):
        filename = os.path.join(folder_path, f"mandala{mandala_num}.txt")
        if not os.path.exists(filename):
            print(f"Warning: {filename} not found.")
            continue

        seen_suktas = set()
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                match = re.search(r'(\d+)\.(\d+)\.(\d+)$', line)
                if not match:
                    continue
                m, s, mantra = match.groups()
                if mantra != '1':
                    continue  # Not the first mantra
                sukta_key = (int(m), int(s))
                if sukta_key in seen_suktas:
                    continue
                seen_suktas.add(sukta_key)

                # Remove the mantra number from the end to get the text part
                text_part = re.sub(r'\s*\d+\.\d+\.\d+$', '', line).strip()
                words = text_part.split()
                name = ' '.join(words[:3])
                if len(name) > 20:
                    name = name[:20] + '...'

                output_rows.append({'mandala': int(m), 'sukta': int(s), 'name': name})

    return output_rows

# Change this to the folder where your mandala1.txt ... mandala10.txt files are stored
folder = './'
output_csv = 'sukta_names.csv'

sukta_data = extract_sukta_names(folder)

# Write to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['mandala', 'sukta', 'name'])
    writer.writeheader()
    writer.writerows(sukta_data)

print(f"✅ Output written to {output_csv} with {len(sukta_data)} entries.")

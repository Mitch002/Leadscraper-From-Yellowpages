import csv

def filter_leads(input_file, output_file):
    leads = []
    with open(input_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['links'] == '{}' and row['email'] and row['email'] != 'yp-logo@2x.png':
                leads.append(row)

    if leads:
        with open(output_file, mode='w', newline='') as file:
            fieldnames = leads[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for lead in leads:
                writer.writerow(lead)
        print("Filtered leads written to", output_file)
    else:
        print("No leads found with {} for a website and a valid email.")


if __name__ == "__main__":
    input_file = "businesses.csv"
    output_file = "leads.csv"
    filter_leads(input_file, output_file)

from bs4 import BeautifulSoup
import pandas as pd

# Load local HTML file

country = input("Enter the code of the country you want the data(e.g. BRA, ECU, ARG, USA) ")
path = "countries/imo_results_" + country+ ".html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Locate the relevant table
table = soup.find("table")

data = []

# Define subject mapping for P1 and P4 from 2003 to 2024
subject_dict = {
    2024: ("A", "G"),
    2023: ("N", "A"),
    2022: ("C", "G"),
    2021: ("A", "G"),
    2020: ("G", "C"),
    2019: ("A", "N"),
    2018: ("G", "C"),
    2017: ("N", "G"),
    2016: ("G", "N"),
    2015: ("C", "G"),
    2014: ("A", "G"),
    2013: ("N", "G"),
    2012: ("G", "A"),
    2011: ("N", "C"),
    2010: ("A", "G"),
    2009: ("N", "G"),
    2008: ("G", "A"),
    2007: ("A", "G"),
    2006: ("G", "N"),
    2005: ("G", "N"),
    2004: ("G", "A"),
}

MIN_EXPECTED_COLUMNS = 10

while True:
    try:
        first_year = int(input("Enter the first year for analysis (e.g., 2014): "))
        last_year = int(input("Enter the last year for analysis (e.g., 2024): "))
        if first_year > last_year:
            print("First year cannot be greater than last year. Please re-enter.")
        else:
            break
    except ValueError:
        print("Invalid year input. Please enter a number.")

        
count = {
        "A": 0,
        "C": 0,
        "G": 0,
        "N": 0,
}

for year in range(first_year, last_year + 1):
    # Use .get() to safely retrieve the subjects.
    # If 'year' is not in subject_dict, subjects_tuple will be None.
    subjects_tuple = subject_dict.get(year)

    if subjects_tuple: # This condition is True if subjects_tuple is not None
        first_subject, second_subject = subjects_tuple
        count[first_subject] += 1
        count[second_subject] += 1
    else:
        # Optional: Print a warning if a year isn't found
        print(f"Warning: Year {year} not found in subject_dict. Skipping.")


# Extract all rows (skip header)
for row in table.find_all("tr")[1:]:
    cols = row.find_all("td")
    if len(cols) < MIN_EXPECTED_COLUMNS:
        continue

    year_text = cols[0].text.strip()
    try:
        year = int(year_text)
    except ValueError:
        continue

    if first_year <= year <= last_year:
        name = cols[1].text.strip()
        p1 = cols[2].text.strip()
        p4 = cols[5].text.strip()

        try:
            p1 = int(p1)
        except ValueError:
            p1 = 0

        try:
            p4 = int(p4)
        except ValueError:
            p4 = 0

        if year in subject_dict:
            subj1, subj4 = subject_dict[year]
        else:
            subj1, subj4 = ("NA", "NA")

        data.append({
            "Year": year,
            "Name": name,
            "P1": p1,
            "P1-Rama": subj1,
            "P4": p4,
            "P4-Rama": subj4
        })

# Convert to DataFrame
df = pd.DataFrame(data)

print(df)

# Subject to index mapping
subject_index = {"A": 0, "C": 1, "G": 2, "N": 3}

# Initialize subject totals: A, C, G, N
subject_sums = [0, 0, 0, 0]

# Accumulate subject-wise scores
for _, row in df.iterrows():
    p1 = row["P1"]
    p4 = row["P4"]
    subj1 = row["P1-Rama"]
    subj4 = row["P4-Rama"] 

    # Only add if the subject was successfully mapped (not "NA")
    if subj1 != "NA":
        subject_sums[subject_index[subj1]] += p1
    if subj4 != "NA": 
        subject_sums[subject_index[subj4]] += p4

# Print results
try:
    print(f"Algebra (A): {subject_sums[0]/count['A']}")
except:
    print(f"Algebra (A): No data")

try:
    print(f"Combinatorics (C): {subject_sums[1]/count['C']}")
except:
    print(f"Combinatorics (C): No data")

try:
    print(f"Geometry (G): {subject_sums[2]/count['G']}")
except:
    print(f"Geometry (G): No data")
try:
    print(f"Number Theory (N): {subject_sums[3]/count['N']}")
except:
    print(f"Number Theory (N): No data")
print("-----------------------------------------------------")
# Combine P1 and P4 into a long-form table with subject
p1_df = df[["Year", "Name", "P1", "P1-Rama"]].rename(columns={"P1": "Score", "P1-Rama": "Subject"})
p4_df = df[["Year", "Name", "P4", "P4-Rama"]].rename(columns={"P4": "Score", "P4-Rama": "Subject"})

combined_df = pd.concat([p1_df, p4_df], ignore_index=True)

# Now group by Subject and compute stats
grouped_stats = combined_df.groupby("Subject")["Score"].agg(["count", "mean", "std", "min", "max", "sum"])

grouped_stats["mean_team_score"] = grouped_stats["mean"] * 6
print(grouped_stats)

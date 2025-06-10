import requests
import os

# Define the directory where HTML files are (or will be) saved
HTML_DIR = "countries" # Make sure this matches your folder name

# Create the output directory if it doesn't exist
if not os.path.exists(HTML_DIR):
    os.makedirs(HTML_DIR)
    print(f"Created directory: '{HTML_DIR}'")

print("Welcome to the IMO Country Data Scraper!")
print("Please enter country codes one by one (e.g., USA, CAN, ECU).")
print("Codes must be exactly three letters long (ISO 3166-1 alpha-3 format).")
print("Press Enter on an empty line when you are done entering codes.")

target_countries = []
while True:
    country_code = input("Enter country code (or press Enter to finish): ").strip().upper()

    if not country_code: # User pressed Enter on an empty line
        break # Exit the input loop

    # --- NEW VALIDATION LOGIC ---
    # Check if the code is exactly 3 characters long AND all characters are alphabetic
    if len(country_code) == 3 and country_code.isalpha():
        target_countries.append(country_code)
    else:
        print(f"Invalid code '{country_code}'. Country codes must be exactly 3 letters long. Please try again.")
    # --- END NEW VALIDATION LOGIC ---

if not target_countries:
    print("No valid country codes entered. Exiting the program.")
else:
    print(f"\nInitiating scraping for the following countries: {', '.join(target_countries)}\n")

    for name in target_countries:
        # Construct the full path where the file *would* be saved
        saved_filename = os.path.join(HTML_DIR, f"imo_results_{name}.html")

        # Check if the file already exists
        if os.path.exists(saved_filename):
            print(f"Skipping {name}: File already exists at '{saved_filename}'")
            continue # Go to the next country in the loop

        # If the file doesn't exist, proceed with scraping
        url = "https://www.imo-official.org/country_individual_r.aspx?code=" + name
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }

        print(f"Fetching data for {name} from {url}...")
        try:
            response = requests.get(url, headers=headers, verify=False, timeout=10)
            response.raise_for_status()

            # Save the HTML locally in the specified directory
            with open(saved_filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Successfully saved HTML for {name} to '{saved_filename}'")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {name}: {e}")
        except IOError as e:
            print(f"Error saving file for {name}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred for {name}: {e}")

    print("\nScraping process complete.")
from bs4 import BeautifulSoup
import pandas as pd

with open("countries/imo_results.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
table = soup.find("table")

target_countries = {"Brazil", "Mexico", "Argentina", "Colombia", "Ecuador", "Costa Rica"}
data = []

for row in table.find_all("tr"):
    cols = row.find_all("td")
    if not cols:
        continue

    country_name = cols[1].text.strip()
    if country_name in target_countries:
        code = cols[0].text.strip()
        first_year = cols[2].text.strip()

        try:
            gold = int(cols[9].text.strip())
            silver = int(cols[10].text.strip())
            bronze = int(cols[11].text.strip())
            HM = int(cols[12].text.strip())
            total = gold + silver + bronze
        except (IndexError, ValueError):
            gold = silver = bronze = total= HM = None

        data.append({
            "Country": country_name,
            "Code": code,
            "First Year": first_year,
            "Gold": gold,
            "Silver": silver,
            "Bronze": bronze,
            "Honorable Mentions": HM,
            "Total Medals": total
        })

df = pd.DataFrame(data)
print(df)

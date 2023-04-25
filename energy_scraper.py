import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_energy_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}")

    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def parse_energy_data(soup):
    data = []

    table = soup.find("table", class_="energy-data")
    if not table:
        return data

    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if cells:
            entry = {
                "timestamp": cells[0].get_text().strip(),
                "power": float(cells[1].get_text().strip()),
                "energy": float(cells[2].get_text().strip()),
            }
            data.append(entry)

    return data

def save_energy_data_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    url = "https://example.com/energy-data"  # Replace this with the actual URL
    soup = fetch_energy_data(url)
    energy_data = parse_energy_data(soup)
    save_energy_data_to_csv(energy_data, "energy_data.csv")

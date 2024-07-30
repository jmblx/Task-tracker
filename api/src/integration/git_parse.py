import requests
from bs4 import BeautifulSoup as bs

username = "bybuss"
repo = "Svetlichniy_Nikita_IS_22"
url = f"https://github.com/bybuss/Svetlichniy_Nikita_IS_22/commit/8da22abaff9d4123e592b4bb018ae6d1a4bee36f"

r = requests.get(url)
soup = bs(r.text, "html.parser")

divs = soup.find_all("div", class_="file-info flex-auto min-width-0 mb-md-0 mb-2")
# Find contributor links
contributors = []
for div in divs:
    contributors.append(div.find("span", class_="sr-only"))

# Extract contributor names and URLs (if available)
for contributor in contributors:
    print(contributor.text)

import requests
from bs4 import BeautifulSoup

urls = [
    "https://www.statisticshowto.com/endogenous-variable/",
    "https://www.zippia.com/advice/exogenous-vs-endogenous/",
    "https://www.linkedin.com/pulse/exogenous-endogenous-variables-understanding-roles-1wj5f",
    "https://www.sciencedirect.com/topics/nursing-and-health-professions/exogenous-variable",
    "https://spotintelligence.com/2023/04/19/endogenous-exogenous/"
]

for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.find_all('p')

    # Sanitize the filename
    name = url.replace('/', '').replace(':', '').replace('.', '').replace('"', '')

    # Save the text content of all <p> tags to the file
    with open(f"data/extracted/{name}.txt", 'w', encoding='utf-8') as f:
        for paragraph in result:
            f.write(paragraph.get_text() + "\n\n")

    with open(f"data/html/{name}.html", 'w', encoding='utf-8') as f:
        f.write(r.text)

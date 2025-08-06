import requests
import re
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game.categories import CATEGORY_TITLES

WIKI_BASE_URL = "https://en.wikipedia.org"


def fetch_wiki_page(url): # safe way to download a Wikipedia page as HTML text.
    try:
        response = requests.get(url, timeout=7) # Tries to send an HTTP GET request to the given url. timeout=7 means: if the server doesn’t respond in 7 seconds, stop waiting
        response.raise_for_status() # Checks if the request was successful, if the server returns an error this line will raise an exception
        return response.text
    except requests.exceptions.RequestException:
        return None


def generate_question_from_infobox(title):
    """
    Check's the Wikipedia infobox for a date label and year.
    Returns (question, year, url).
    """
    url = f"{WIKI_BASE_URL}/wiki/{title}"
    html = fetch_wiki_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    infobox = soup.find("table", class_="infobox")
    if not infobox:
        return None

    labels_to_look_for = [
        "Born", "Founded", "Established", "Released", "Opening", "Release date",
        "First awarded", "Date", "Formed", "Created", "Launched", "Start", "Period"
    ]

    year = None
    label_text = None

    for row in infobox.find_all("tr"): #tr table rows contains data like html <tr> <th>Born</th> <td>14 March 1879</td> </tr>
        header = row.find("th") #th gets the header like Born, released
        data = row.find("td") #td get the actual date

    #     < tr >
    #       < th > Born < / th >
    #       < td > 14 March 1879 < / td >
    #     < / tr >

        if header and data:
            label = header.get_text(strip=True)
            if any(keyword in label for keyword in labels_to_look_for):
                text = data.get_text()
                match = re.search(r'\b(\d{3,4})\s*(BC|AD)?', text, re.IGNORECASE)
                # Uses regex to search for a 3- or 4-digit year (\d{3,4}) in the text A RegEx, or Regular Expression,
                # is a sequence of characters that forms a search pattern. RegEx can be used to check if a string contains the specified search pattern
                if match:
                    label_text = label
                    year = int(match.group(1))
                    if match.group(2) and match.group(2).upper() == 'BC':
                        year = -year
                    break

    if year is None or label_text is None:
        return None

    readable_title = title.replace("_", " ")
    question = f"In the Wikipedia article titled \"{readable_title}\", what year is listed for: \"{label_text}\"?"

    return question, year, url


#test which element is corrected retrived from wikipedia
if __name__ == "__main__":
    for category, titles in CATEGORY_TITLES.items():
        print(f"\n🔍 Checking category: {category}") # I can check a specific category for example {category} --> {"history"} and it will only check history
        for title in titles:
            result = generate_question_from_infobox(title)
            if result:
                question, year, url = result
                print(f"\n🟢 Success for: {title}")
                print(f"Question: {question}")
                print(f"Year: {year}")
                print(f"URL: {url}")
            else:
                print(f"\n🔴 Failed to extract info for: {title}")

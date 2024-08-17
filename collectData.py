import requests
import math
import re
from bs4 import BeautifulSoup
from urllib.parse import quote

def data(term, num):
    allSent = []  # Empty list to store all sentences
    key = 1

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36'
    }

    youreiURL = 'https://yourei.jp/'

    prepterm = quote(term)
    query = youreiURL + prepterm
    print("Searching: ", query)
    print()
    response = requests.get(query, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        number = soup.select_one('#sentence-frequency-line')
        if number:
            numbertext = number.get_text(strip=True)
            print(numbertext)

            clean = numbertext.replace(",", "")
            numbers = re.findall(r'\d+', clean)
            total = int(numbers[0])
        else:
            print("No element found with selector '#sentence-frequency-line'")
            total = 0

        sentences = soup.select('.sentence')

        blank = 0
        try:
            if sentences:
                for sentence in sentences:
                    txt = sentence.get_text()
                    current = "".join(re.findall(r'([^。！？?!]*{}[^。！？?!]*(?:[。！？?!]))'.format(term), txt))
                    current = current.strip()

                    if current == "":
                        blank += 1
                    else:
                        print(current)
                        allSent.append(current)  # Append current sentence to the list
                        key += 1
            else:
                print("No sentences found for the given term.")

            indexed = key - blank
            output = str(indexed) + " SENTENCES INDEXED (" + str(blank) + " blank)"
            print(output)

            pages = math.ceil(total / 30)
            print(pages, "pages of sentences")

            if num != 0:
                if num == -1:
                    print("Indexing all pages")
                elif num > 0:
                    pages = num
                currentPage = 2
                startval = 1
                ogquery = query + "?start="
                blank = 0
                while currentPage <= pages:
                    startval += 30
                    query = ogquery + str(startval)
                    response = requests.get(query, headers=headers)
                    print("Searching: ", query)
                    soup = BeautifulSoup(response.text, 'html.parser')

                    sentences = soup.select('.sentence')

                    if sentences:
                        for sentence in sentences:
                            txt = sentence.get_text()
                            current = "".join(re.findall(r'([^。！？?!]*{}[^。！？?!]*(?:[。！？?!]))'.format(term), txt))
                            current = current.strip()
                            if current == "":
                                blank += 1
                            else:
                                allSent.append(current)  # Append current sentence to the list
                                key += 1
                    else:
                        print("No sentences found for the given term.")

                    print("Page", currentPage, "completed.")
                    currentPage += 1

                    indexed = key - blank
                    output = str(indexed) + " SENTENCES INDEXED (" + str(blank) + " blank)"
                    print(output)
        except AttributeError as e:
            print("Error occurred:", e)
            return 'None'

    else:
        print("Failed to retrieve webpage. Status code:", response.status_code)

    return allSent

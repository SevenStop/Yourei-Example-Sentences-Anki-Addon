
import requests
import math
import re
from bs4 import BeautifulSoup
#import BeautifulSoup
from urllib.parse import quote
#import quote


def dispP():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36'
    }

    #url of yourei
    youreiURL = 'https://yourei.jp/'

    term = input("Enter Japanese word you're searching: ")
    term = quote(term)
    query = youreiURL + term
    print("Searching: ", query)
    print()
    response = requests.get(query, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all sentences on the page

        number = soup.select_one('#sentence-frequency-line')
        numbertext = number.get_text(strip=True)
        print(numbertext)
        #clean up the string to use for calculations
        clean = numbertext.replace(",","")
        numbers = re.findall(r'\d+', clean)
        final = [int(number) for number in numbers]
        total = final[0]

        #print the first page
        sentences = soup.select('.sentence')

        if sentences:
            # Print each sentence
            for sentence in sentences:
                print(sentence.get_text())
        else:
            print("No sentences found for the given term.")

        print("Page 1 completed.")

        #now calculate number of pages of info
        pages = math.ceil(total / 30)
        print(pages, "pages of sentences")
        #run loop until all pages are iterated through
        action = input("Press Y to see more sentences (any other key to cancel): ")
        if action == 'y' or action == 'Y':
            currentPage = 2
            startval = 1
            ogquery = query + "?start="
            while currentPage <= pages:
               #update start value
                startval += 30
                query = ogquery + str(startval)
                #scrape new webpage
                response = requests.get(query, headers=headers)
                print("Searching: ", query)
                soup = BeautifulSoup(response.text, 'html.parser')

                sentences = soup.select('.sentence')

                if sentences:
                    # Print each sentence
                    for sentence in sentences:
                        print(sentence.get_text())
                else:
                    print("No sentences found for the given term.")

                print("Page", currentPage, "completed.")
                currentPage +=1

    else:
        print("Failed to retrieve webpage. Status code:", response.status_code)
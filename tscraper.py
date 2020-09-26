import requests
from bs4 import BeautifulSoup
import csv
import time


def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print("Server responded:", response.status_code)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_detail_data(soup):
    try:
        title = soup.find("h1", class_="title--3s1R8").text
    except:
        title = ""

    try:
        date = soup.find("h3", class_="sub-title--37mkY").text
    except:
        date = ""

    try:
        price = soup.find("div", class_="amount--3NTpl").text
        price = price.split(maxsplit=1)[-1]
    except:
        price = ""

    data = {
        "title": title,
        "date": date,
        "price": price,
    }

    return data


def get_index_data(soup):
    try:
        links = soup.findAll("a", class_="card-link--3ssYv gtm-ad-item")
    except:
        links = []

    urls = ["https://tonaton.com"+item.get("href") for item in links]

    return urls


def write_csv(data, url):
    with open("tonatonoutput.csv", "a") as csvfile:
        writer = csv.writer(csvfile)

        row = [data["title"], data["date"], data["price"], url]

        writer.writerow(row)


def main():
    search_item = "cars" #change this to the item you want to search for. 
    page_num = 1 #start at page 1 of the search query
    
    flag = True #Set a flag to control how the while loop runs.
    
    while flag:
    
        url = f"https://tonaton.com/en/ads/ghana/{search_item}?page={page_num}"
        page = get_page(url)
        
        page_end = page.find('div', class_="no-result-text--16bWr") 
        
        #If you get to a page with no results, that's the end then.
        #The page_end variable will thus contain a string "No results found."
        #while empty, the page_end variable evaluates to False, and changes when the variable's content changes.
       
        
        if page_end: 
            flag = False #set flag to false once we get 'No results found so the while loop terminates'
            return 'Script finished successfully.' #This return statement prevents the code below from executing.
        
        products = get_index_data(page)
        
        for link in products:
            data = get_detail_data(get_page(link))
            write_csv(data, link)
        
        page_num += 1 #Increase page_num by 1 to go to the next page in the next iteration of the while loop.
    
    return "Script completed."

if __name__ == '__main__':
    main()
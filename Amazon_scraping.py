import requests
import csv
from bs4 import BeautifulSoup
import os


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"

accept ="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
accept_en = "gzip, deflate, br"
accept_lan = "en-US,en;q=0.9"
cache_con = "max-age=0"
cokies = ""
headers = {'accept': accept,
           'accept-encoding': accept_en,
           'accept-language': accept_lan,
           'cache-control': cache_con,
           'cache': cokies,
           'user-agent': user_agent}


os.chdir(os.path.dirname(os.path.abspath(__file__)))
links = []
name_prodact = []
price = []
rate = []

prodact = input("Put the name of the prodact: ")
i = 0 

while(i < 4):

    url = f"https://www.amazon.com/s?k={prodact}&page={i}&qid=1627730347&ref=sr_pg_2"

    reaslt = requests.get(url, headers=headers)

    # print(reaslt.text)

    soup = BeautifulSoup(reaslt.content, "html.parser")

    # print(soup.text)

    names_prodact = soup.find_all("h2", {"class":"a-size-mini"})

    # soup.find_all("h2", {"class":"a-size-mini"}).find("a").attrs["href"]



    for name in names_prodact:
        links.append("https://www.amazon.com"+name.find("a").attrs["href"])
        name_prodact.append(name.text.strip())
        
    for link in links:
        reaslt = requests.get(link, headers=headers)   
        soup = BeautifulSoup(reaslt.content, "html.parser")
        try:
            price.append(soup.find("span", {"class": "a-color-price"}).text.strip())
        except:
            try:
                price.append(soup.find("span", {"id": "price_inside_buybox"}).text.strip())
            except:
                price.append("----")
        
        rate.append(soup.find("span", {"class": "a-icon-alt"}).text.strip())

    i += 1
    print("page switched")


with open("amazon_prodact.csv", "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(['prodact name', 'price', 'Rate', 'Link'])
    for i in range(len(name_prodact)):
        try:
            wr.writerow([name_prodact[i],price[i], rate[i], links[i]])
        except:
            wr.writerow(["something wrong","something wrong", "something wrong", links[i]])

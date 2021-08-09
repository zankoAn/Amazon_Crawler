from bs4 import BeautifulSoup

import requests

import csv

import re



class Books:
    def __init__(self):
        self.url_books_com = "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg="

        self.url_books_in = "https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_1?_encoding=UTF8&pg="

        self.headers = {
            "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
        }


    def exists(self, index: int, value: str = None) -> str:
            """
                Check value exists or not
                
                
                Returns 
                --------
                    String

                        "Not Available" if index not exists else return index of list.
            """

            try:
                return value[index]

            except IndexError:
                return "Not Available"

            
    def bestـsellersـbooks(self, Pagination_Number: int = 1) -> list:
        """
            Scrap all of the information about Amazon Best Sellers books

            Returns 
            --------
                List 
                    A list contains dictionary information about books.
        """

        rows = []
        urls = [self.url_books_com, self.url_books_in]
        
        print("Start Scraping the data\n")

        for url in urls:

            for page in range(1, Pagination_Number):
                
                try : 

                    response = requests.get(url=url+str(page), headers=self.headers)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "lxml")
                        
                        for book in soup.find("ol", {"class":"a-ordered-list a-vertical"}):
                            
                            book_body = [ c.strip() for c in book.text.split("\n") if c.strip()]
                            
                                            
                            number, name, author, stars, ratings, price = ( self.exists(d, book_body) for d in range(6))

                            try:
                                # The price may not include these two symbols([$, ₹]), in which case you will receive index out of range err
                                currency_symbol = ["₹", "$", "₹", "¥", "£", "€", "лв", "₽", "₺"]
                                price = [  char + price.split(char)[1] for char in currency_symbol if len(price.split(char)) > 1 ][0] if price != "Not Available" else price
                            
                                book_url = "https://www.amazon.in/" + book.find("a").get("href")
                                book_url = re.match("(.*zg_bs_books_\d+)", book_url).group()

                                ratings =  ratings.replace(",", ".")
                                ratings = float(ratings) if ratings !=  "Not Available" else ratings

                            except IndexError:
                                raise Exception("Price does not include set symbols(You can added manually)")
                                continue

                            rows.append({"Url":book_url, "Index":number, "Name":name, "Author":author, "Stars":stars, "Ratings":ratings, "Price":price})

                            
                except Exception as err:
                    return f"<New Error> <{err}>"

        return rows




scrap = Books()

rows = scrap.bestـsellersـbooks(4)


fieldnames = ["Url", "Index", "Name", "Author", "Stars", "Ratings", "Price"]

# If you're using windows change directory /output to \\output
with open('output/BestSeller-Books.csv', 'w', encoding='UTF8', newline='\n') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


print(f"The data of {len(rows)} Amazon books was successfully scraped and saved in the BestSeller-Books.csv file")

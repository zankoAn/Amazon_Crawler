# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, sys, csv

######################################
#         AMAZON_Crawler             #
#         Code By #!z@nko...;        #
######################################

amazon = "https://www.amazon.com/"
csvData=[]
for pg in range(1, 6):
    url = 'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg=' +str(pg) 
    page = requests.get(url)
    if page.ok ==True:
        data = page.text
        soup = BeautifulSoup(data, "html.parser")        
        for num in soup.find_all('div',class_='a-section a-spacing-none aok-relative'):
            soup2=BeautifulSoup(str(num),'lxml')
            tempData = []            
            bookName = soup2.find(
                'div', class_="p13n-sc-truncate p13n-sc-line-clamp-1")
            if bookName is None:                
                tempData.append(", Name: Not Available")
            else:
                name = bookName.get_text().strip()                                                                
                tempData.append(',NAME: '+name.strip()+'\n')                

            url = soup2.find("a", class_="a-link-normal")
            if url is None:
                tempData.append("URL: Not available")
            else:
                url = "https://www.amazon.com" + url["href"]
                tempData.append('URL: '+amazon + url+'\n')
            

            bookAuthor = soup2.find('div', class_="a-row a-size-small")
            if bookAuthor is None:                
                tempData.append("Author: Not Available")
            else:                
                tempData.append('Author: '+bookAuthor.get_text().strip()+'\n')
                
            bookPrice = soup2.find('span', class_="p13n-sc-price")
            if bookPrice is None:
                tempData.append("Price: Not Available")
            else:                
                tempData.append('Price: '+bookPrice.get_text().strip()+'\n')

            numberOfRatings = soup2.find(class_="a-size-small a-link-normal")
            if numberOfRatings is None:            
                tempData.append("Ber-of-Ratings: Not Available")
            else:
                try:                    
                    tempData.append('Number_of_Ratings: '+numberOfRatings.get_text().strip()+'\n')
                except Exception:
                    tempData.append("Ber-of-Ratings: Not Available")

            bookRating = soup2.find(class_="a-icon-alt")
            if bookRating is None :
                tempData.append("Rating: Not Available")
            elif bookRating.getText().strip()=='Prime':                
                tempData.append("Rating: Not Available")
            else:                
                try:
                    tempData.append('Average_Rating: '+bookRating.get_text().strip()+'\n\n')

                except Exception:
                    tempData.append("Rating: Not Available")           
            csvData.append(tempData)
    else:
        pass
with open('./output/in_book.csv', 'w') as MyFile:    
    writer = csv.writer(MyFile, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    for i in csvData:
        i = [s for s in i]
        writer.writerows([i])

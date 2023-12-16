# scrapping imdb at 16th december 2023

from bs4 import BeautifulSoup
import requests
import csv

# header names (column name for identifying each values)
column_name = ['Entry Number', 'Name', 'Year', 'Duration', 'Movie Rating', 'Movie Score', 'Total votes']
# opening csv file
csvfile = open('movie_data.csv', 'w', newline='') # (newline='') is done so that the entries do not go to a new line after writing on the file see doc: https://docs.python.org/3/library/csv.html
csvwriter = csv.writer(csvfile)
csvwriter.writerow(column_name)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

website = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250", headers=headers).text
soup = BeautifulSoup(website, 'lxml')
movies = soup.find_all('li', class_= 'ipc-metadata-list-summary-item sc-3f724978-0 enKyEL cli-parent')
c = 0
for movie in movies:
    name = movie.find('h3', class_= 'ipc-title__text').text.split('. ')[1:]
    name = "{}".format(*name) # unpacking the list to only have the string name. (look at unpacking in python for more explanation)

    movieData = movie.find_all('span', class_= 'sc-43986a27-8 jHYIIK cli-title-metadata-item') # find all returns a list like object, where each element can be parsed individually and indexed too.

    # this is why I am indexing here as in the website there are three different spans with smae class name
    year = movieData[0].text
    duration = movieData[1].text
    # error handling was used due to number 77 record not having a rating
    try:
        movieRated = movieData[2].text
    except IndexError:
        print("value does not exist")

    rating = movie.find('span', class_= 'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating').text
    rating, count = rating.split()
    count = count.strip("()") # removing the parentheses
    
    c+=1 # to check whether we are able to properly scrape the data for all 250 movies

    
    csvwriter.writerow([c, name, year, duration, movieRated, rating, count]) # writing data to the file
    """ print(name)
    print(year)
    print(duration)
    print(movieRated)
    print(rating)
    print(count) """
   
print(f"Done writing {c} entries to the csv file!")
csvfile.close()
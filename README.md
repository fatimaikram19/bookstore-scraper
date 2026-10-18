# Bookstore Scraper
This project scrapes book data from the practice website books.toscrape.com and turns it into a clean dataset. It was made for Assignment 2 of Business Data and Text Mining.

## What it collects
- Title
- Price
- Rating (converted from words like One and Five into numbers 1 to 5)
- Availability
- Product page link

## How it works
The program has one function that scrapes a single page. A loop calls this function for every page until the website has no more pages. In total it collects 1000 books from 50 pages. The data is saved in a pandas DataFrame and then written to competitor_books.csv.

## Libraries used
requests, BeautifulSoup, pandas and matplotlib

## How to run
1. Install the libraries: pip install requests beautifulsoup4 pandas matplotlib
2. Run the program: python3 scraper.py

## Files in this repository
- scraper.py is the scraper and the analysis code
- competitor_books.csv is the dataset made by the scraper
- rating_counts.png is a bar chart of books at each star rating
- answers.txt has the output of the program
- The Word document has my answers and business recommendation

## Main findings
- 1000 books were scraped
- The average book price is 35.07 pounds
- 196 books have a 5 star rating
- All the books are in stock
- With 100 pounds, the best selection gives a total rating score of 44 for 98.68 pounds

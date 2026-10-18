import re
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Mission 1 notes (what I found by inspecting the page)
# Each book sits inside:        article with class product_pod
# Title:                        h3 > a, the full title is in the title attribute
# Price:                        p with class price_color
# Rating:                       p with class star-rating, the word is the second class (for example Three)
# Availability:                 p with class instock availability
# Product link:                 h3 > a, href attribute

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def scrape_page(page_number):
    """Scrape one page and return a list of books. Returns None if the page does not exist."""
    url = BASE_URL.format(page_number)
    response = requests.get(url)

    if response.status_code != 200:
        return None

    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("article", class_="product_pod")

    books = []
    for card in cards:
        link = card.find("h3").find("a")
        title = link["title"]
        product_url = urljoin(url, link["href"])

        price_text = card.find("p", class_="price_color").text
        price = float(re.findall(r"\d+\.\d+", price_text)[0])

        rating_word = card.find("p", class_="star-rating")["class"][1]
        rating = RATING_MAP[rating_word]

        availability = card.find("p", class_="availability").text.strip()

        books.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Availability": availability,
            "Product URL": product_url,
        })

    return books


# Mission 3 and Boss Level: loop through all pages until there are no more
all_books = []
page = 1
while True:
    result = scrape_page(page)
    if result is None:
        break
    all_books.extend(result)
    print("Scraped page", page, "total books so far:", len(all_books))
    page += 1

df = pd.DataFrame(all_books)

print()
print(df.head())
print(df.columns.tolist())

df.to_csv("competitor_books.csv", index=False)
print("Saved competitor_books.csv")

# Mission 4: Intelligence analysis
print()
print("MISSION 4 ANSWERS")

most_expensive = df.loc[df["Price"].idxmax()]
print("1. Most expensive book:", most_expensive["Title"], "-", most_expensive["Price"])

cheapest = df.loc[df["Price"].idxmin()]
print("2. Cheapest book:", cheapest["Title"], "-", cheapest["Price"])

print("3. Average price:", round(df["Price"].mean(), 2))

five_star = df[df["Rating"] == 5]
print("4. Number of 5 star books:", len(five_star))

in_stock = df["Availability"].str.contains("In stock").sum()
print("5. Percentage in stock:", round(in_stock / len(df) * 100, 2), "%")

print("6. Top 5 highest rated books:")
top5 = df.sort_values(by=["Rating", "Price"], ascending=[False, True]).head(5)
print(top5[["Title", "Price", "Rating"]].to_string(index=False))

cheapest_five = five_star.loc[five_star["Price"].idxmin()]
print("7. Cheapest 5 star book:", cheapest_five["Title"], "-", cheapest_five["Price"])

# Supporting evidence for the business recommendation
print()
print("Average price by rating:")
print(df.groupby("Rating")["Price"].mean().round(2))

# Final challenge: CEO has 100 pounds
# For every possible total rating we remember the cheapest way to reach it.
best = {0: (0.0, [])}

for i in df.index:
    price = df.loc[i, "Price"]
    rating = df.loc[i, "Rating"]
    new_best = dict(best)
    for total, (cost, items) in best.items():
        new_total = total + rating
        new_cost = round(cost + price, 2)
        if new_cost <= 100:
            if new_total not in new_best or new_cost < new_best[new_total][0]:
                new_best[new_total] = (new_cost, items + [i])
    best = new_best

best_total = max(best.keys())
best_cost, best_items = best[best_total]
chosen = df.loc[best_items]

print()
print("CEO 100 POUND CHALLENGE")
print(chosen[["Title", "Price", "Rating"]].to_string(index=False))
print("Total cost:", best_cost)
print("Total rating score:", best_total)

# Bonus 3: count of books at each star level
print()
rating_counts = df["Rating"].value_counts().sort_index()
print("Books at each star level:")
print(rating_counts)

# Bonus 4: bar chart
rating_counts.plot(kind="bar")
plt.title("Number of Books by Star Rating")
plt.xlabel("Star Rating")
plt.ylabel("Number of Books")
plt.tight_layout()
plt.savefig("rating_counts.png")
plt.show()

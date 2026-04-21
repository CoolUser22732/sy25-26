import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def search_book(title_query):
    page_url = BASE_URL

    while True:
        soup = get_soup(page_url)

        books = soup.select("article.product_pod h3 a")

        for book in books:
            title = book["title"].strip()

            if title_query.lower() in title.lower():
                relative_link = book["href"]
                book_url = urljoin(page_url, relative_link)

                return get_book_details(book_url)

        # Check if there's a next page
        next_button = soup.select_one("li.next a")
        if next_button:
            page_url = urljoin(page_url, next_button["href"])
        else:
            return None

def get_book_details(book_url):
    soup = get_soup(book_url)

    # Price
    price = soup.select_one(".price_color").text.strip()

    # Availability
    availability = soup.select_one(".availability").text.strip()

    return {
        "price": price,
        "availability": availability,
        "url": book_url
    }

def main():
    print("📚 Book Search App (BooksToScrape)")

    while True:
        title_query = input("\nEnter a book title to search: ").strip()

        if not title_query:
            print("Please enter a valid title.")
            continue

        result = search_book(title_query)

        if result:
            print("\n✅ Book Found!")
            print(f"Price: {result['price']}")
            print(f"Stock: {result['availability']}")
            print(f"Buy link: {result['url']}")
        else:
            print("\n❌ Book not found in catalog.")
            retry = input("Try another title? (y/n): ").lower()
            if retry != "y":
                break

if __name__ == "__main__":
    main()

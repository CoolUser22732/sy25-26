import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re

BASE_URL = "https://books.toscrape.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

# -------------------------------
# Request helper
# -------------------------------
def get_soup(url, retries=3, delay=1):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=5)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"❌ Failed to fetch {url}")
                return None

# -------------------------------
# Parsers
# -------------------------------
def parse_rating(tag):
    if not tag:
        return "Unknown"
    for r in RATING_MAP:
        if r in tag.get("class", []):
            return r
    return "Unknown"

def parse_price(price_text):
    try:
        return float(re.sub(r"[^\d.]", "", price_text))
    except:
        return 0.0

def parse_stock(text):
    match = re.search(r"(\d+)", text)
    return int(match.group(1)) if match else 0

# -------------------------------
# Scrape (WITH PAGE LOADING UI)
# -------------------------------
def scrape_all_books():
    books_data = []
    page_url = BASE_URL
    page_count = 1

    print("⏳ Loading books (page by page)...\n")

    while page_url:
        print(f"📄 Loading Page {page_count}...")

        soup = get_soup(page_url)
        if not soup:
            break

        books = soup.select("article.product_pod")

        for book in books:
            title_tag = book.select_one("h3 a")
            title = title_tag["title"].strip()

            relative_link = title_tag["href"]
            book_url = urljoin(page_url, relative_link)

            price_text = book.select_one(".price_color").text.strip()
            rating = parse_rating(book.select_one("p.star-rating"))

            books_data.append({
                "title": title,
                "price": parse_price(price_text),
                "rating": rating,
                "url": book_url
            })

        print(f"   ✅ Page {page_count} loaded ({len(books)} books)\n")

        next_button = soup.select_one("li.next a")
        page_url = urljoin(page_url, next_button["href"]) if next_button else None

        page_count += 1
        time.sleep(0.2)

    print(f"🎉 Finished loading {len(books_data)} books total!\n")
    return books_data

# -------------------------------
# Get details
# -------------------------------
def get_book_details(book):
    soup = get_soup(book["url"])
    if not soup:
        return None

    availability_text = soup.select_one(".availability").text.strip()
    stock = parse_stock(availability_text)

    return {
        "title": book["title"],
        "price": book["price"],
        "rating": book["rating"],
        "stock": stock
    }

# -------------------------------
# Display list
# -------------------------------
def display_list(books):
    if not books:
        print("\n❌ No books found.")
        return []

    print(f"\n📚 Showing {min(len(books),20)} of {len(books)} books:\n")

    for i, b in enumerate(books[:20], 1):
        print(f"{i}. {b['title']}")

    return books[:20]

# -------------------------------
# Display details
# -------------------------------
def show_details(book):
    details = get_book_details(book)
    if not details:
        print("❌ Could not fetch details.")
        return

    print("\n📖 DETAILS")
    print(f"Title: {details['title']}")
    print(f"Rating: {details['rating']}")
    print(f"Price: £{details['price']:.2f}")
    print(f"Amount left: {details['stock']}\n")

# -------------------------------
# Sorting helpers
# -------------------------------
def sort_by_rating(books, reverse=False):
    return sorted(books, key=lambda x: RATING_MAP.get(x["rating"], 0), reverse=reverse)

def sort_by_price(books, reverse=False):
    return sorted(books, key=lambda x: x["price"], reverse=reverse)

def sort_by_stock(books, reverse=False):
    detailed = [(b, get_book_details(b)) for b in books]
    detailed = [d for d in detailed if d[1]]
    return [b for b, d in sorted(detailed, key=lambda x: x[1]["stock"], reverse=reverse)]

# -------------------------------
# Main menu
# -------------------------------
def main():
    books = scrape_all_books()

    if not books:
        print("❌ Could not load books.")
        return

    while True:
        print("\n--- MENU ---")
        print("1. All books")
        print("2. Books by starting letter")
        print("3. Highest rating")
        print("4. Lowest rating")
        print("5. Lowest price")
        print("6. Highest price")
        print("7. Lowest stock")
        print("8. Highest stock")
        print("9. Search for exact title")
        print("10. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            results = books

        elif choice == "2":
            letter = input("Enter letter: ").lower()
            results = [b for b in books if b["title"].lower().startswith(letter)]

        elif choice == "3":
            results = sort_by_rating(books, reverse=True)

        elif choice == "4":
            results = sort_by_rating(books)

        elif choice == "5":
            results = sort_by_price(books)

        elif choice == "6":
            results = sort_by_price(books, reverse=True)

        elif choice == "7":
            results = sort_by_stock(books)

        elif choice == "8":
            results = sort_by_stock(books, reverse=True)

        elif choice == "9":
            title = input("Enter exact title: ").strip()
            results = [b for b in books if b["title"].lower() == title.lower()]

            if not results:
                print("\n❌ Book not found.")
                print("Check spelling/capitalization or it may not be available.\n")
                continue

            show_details(results[0])
            continue

        elif choice == "10":
            print("👋 Goodbye!")
            break

        else:
            print("Invalid option.")
            continue

        shown = display_list(results)

        if shown:
            pick = input("Select a book number for details: ").strip()
            if pick.isdigit():
                idx = int(pick) - 1
                if 0 <= idx < len(shown):
                    show_details(shown[idx])

if __name__ == "__main__":
    main()
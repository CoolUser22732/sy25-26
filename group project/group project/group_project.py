import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re

BASE_URL = "https://books.toscrape.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# -------------------------------
# Request helper (with retries)
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
# Rating parser
# -------------------------------
def parse_rating(tag):
    if not tag:
        return "Unknown"
    classes = tag.get("class", [])
    for r in ["One", "Two", "Three", "Four", "Five"]:
        if r in classes:
            return r
    return "Unknown"

# -------------------------------
# Safe price parser (FIXED)
# -------------------------------
def parse_price(price_text):
    try:
        return float(re.sub(r"[^\d.]", "", price_text))
    except:
        return 0.0

# -------------------------------
# FAST scrape (no heavy requests)
# -------------------------------
def scrape_all_books():
    books_data = []
    page_url = BASE_URL
    page_count = 1

    print("⏳ Loading books (fast mode)...")

    while page_url:
        print(f"📄 Page {page_count}")

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

        next_button = soup.select_one("li.next a")
        page_url = urljoin(page_url, next_button["href"]) if next_button else None
        page_count += 1

    print(f"✅ Loaded {len(books_data)} books.\n")
    return books_data

# -------------------------------
# Fetch full details (on demand)
# -------------------------------
def get_book_details(book_url):
    soup = get_soup(book_url)
    if not soup:
        return None

    try:
        availability = soup.select_one(".availability").text.strip()
        description_tag = soup.select_one("#product_description ~ p")
        description = description_tag.text.strip() if description_tag else "No description"

        return {
            "availability": availability,
            "description": description
        }
    except:
        return None

# -------------------------------
# Filters
# -------------------------------
def filter_books(books, title=None, rating=None, min_price=None, max_price=None):
    results = books

    if title:
        results = [b for b in results if title.lower() in b["title"].lower()]

    if rating:
        results = [b for b in results if b["rating"].lower() == rating.lower()]

    if min_price is not None:
        results = [b for b in results if b["price"] >= min_price]

    if max_price is not None:
        results = [b for b in results if b["price"] <= max_price]

    return results

# -------------------------------
# Display results
# -------------------------------
def display_results(results):
    if not results:
        print("\n❌ No books found. Returning to menu...")
        return []

    print(f"\n📚 Found {len(results)} books (showing up to 10):\n")

    for i, book in enumerate(results[:10], 1):
        print(f"{i}. {book['title']}")
        print(f"   💲 £{book['price']:.2f} | ⭐ {book['rating']}")
        print(f"   🔗 {book['url']}\n")

    return results[:10]

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
        print("1. Search by Title")
        print("2. Filter by Rating")
        print("3. Filter by Price Range")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            query = input("Enter title: ").strip()
            results = filter_books(books, title=query)

        elif choice == "2":
            rating = input("Enter rating (One–Five): ").strip()
            results = filter_books(books, rating=rating)

        elif choice == "3":
            try:
                min_p = float(input("Min price: ") or 0)
                max_p = float(input("Max price: ") or 1000)
            except ValueError:
                print("Invalid price input.")
                continue
            results = filter_books(books, min_price=min_p, max_price=max_p)

        elif choice == "4":
            print("👋 Goodbye!")
            break

        else:
            print("Invalid option.")
            continue

        shown = display_results(results)

        if not shown:
            continue

        # Optional: view details
        view = input("Enter number to see details (or press Enter to skip): ").strip()

        if view.isdigit():
            idx = int(view) - 1
            if 0 <= idx < len(shown):
                details = get_book_details(shown[idx]["url"])
                if details:
                    print("\n📖 DETAILS:")
                    print(f"Stock: {details['availability']}")
                    print(f"Description: {details['description']}\n")
                else:
                    print("❌ Could not fetch details.")

if __name__ == "__main__":
    main()
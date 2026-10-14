import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_books():
    url = "http://toscrape.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch webpage. Status code: {response.status_code}")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    
    data_list = []
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    
    for book in books:
        title = book.h3.a['title']
        price_text = book.find('p', class_='price_color').text
        clean_price = float(price_text.replace('£', '').strip())
        
        rating_classes = book.find('p', class_='star-rating')['class']
        rating_word = [c for c in rating_classes if c != 'star-rating'][0]
        numeric_rating = rating_map.get(rating_word, 0)
        
        availability = book.find('p', class_='instock availability').text.strip()
        
        data_list.append({
            "Product_Title": title,
            "Price_GBP": clean_price,
            "Star_Rating": numeric_rating,
            "Availability": availability
        })
    
    df = pd.DataFrame(data_list)
    df.drop_duplicates(inplace=True)
    df['Price_Tier'] = pd.cut(df['Price_GBP'], bins=[0, 20, 40, 100], labels=['Budget', 'Mid-Range', 'Premium'])
    
    output_file = "cleaned_market_data.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Successfully scraped, cleaned, and saved data to '{output_file}'!")

if __name__ == "__main__":
    scrape_books()

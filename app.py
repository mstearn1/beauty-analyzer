# simple_scraper.py
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Simple Beauty Product Scraper")
st.title("🔍 Simple Beauty Product Info Scraper")

st.markdown("""
Paste one or more beauty product URLs (from **Sephora** or **Ulta**) below. The tool will attempt to pull:
- Product image
- Description
- Ingredients
- Price
- Ounces (if found)

Just paste the URLs and click the button.
""")

urls_input = st.text_area("Paste URLs (one per line):", height=200)

if st.button("Scrape Info"):
    urls = [url.strip() for url in urls_input.splitlines() if url.strip()]

    for url in urls:
        st.subheader(url)
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")

            image_url = description = ingredients = price = ounces = "N/A"

            if "sephora.com" in url:
                img_tag = soup.find("img", class_="css-11gn9r6")
                image_url = img_tag["src"] if img_tag else ""
                desc_tag = soup.find("div", {"data-at": "product_description"})
                description = desc_tag.get_text(strip=True) if desc_tag else "N/A"
                ing_tag = soup.find("div", {"data-comp": "ProductDetailIngredients"})
                ingredients = ing_tag.get_text(strip=True) if ing_tag else "N/A"
                price_tag = soup.find("span", {"data-comp": "DisplayPrimaryPrice"})
                price = price_tag.get_text(strip=True) if price_tag else "N/A"
                oz_tag = soup.find("span", class_="css-1jcznhx")
                ounces = oz_tag.get_text(strip=True) if oz_tag else "N/A"

            elif "ulta.com" in url:
                img_tag = soup.find("img", class_="ProductMainImage")
                image_url = img_tag["src"] if img_tag else ""
                desc_tag = soup.find("div", class_="ProductDescriptionContainer")
                description = desc_tag.get_text(strip=True) if desc_tag else "N/A"
                ing_tag = soup.find("div", class_="ProductIngredientsContainer")
                ingredients = ing_tag.get_text(strip=True) if ing_tag else "N/A"
                price_tag = soup.find("span", class_="ProductPricingPanel-price")
                price = price_tag.get_text(strip=True) if price_tag else "N/A"
                ounces = "N/A"

            else:
                st.warning("Unsupported website")
                continue

            if image_url:
                st.image(image_url, width=200)

            st.markdown(f"**Description:** {description}")
            st.markdown(f"**Ingredients:** {ingredients}")
            st.markdown(f"**Price:** {price}")
            st.markdown(f"**Ounces:** {ounces}")

        except Exception as e:
            st.error(f"Error scraping {url}: {e}")

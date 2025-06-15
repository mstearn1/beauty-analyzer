import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("🔍 Simple Beauty Product Info Scraper")

st.markdown("""
Paste one or more beauty product URLs (from **Sephora** or **Ulta**) below. The tool will pull:
- Image
- Description
- Ingredients
- Price
- Ounces (if found)

Just copy & paste the URLs and press the button.
""")

urls_input = st.text_area("Paste URLs (one per line):", height=200)

if st.button("Scrape Info"):
    urls = [url.strip() for url in urls_input.splitlines() if url.strip()]

    for url in urls:
        st.subheader(url)
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.text, "html.parser")

            if "sephora.com" in url:
                image = soup.find("img", class_="css-11gn9r6")
                image_url = image['src'] if image else ""
                description = soup.find("div", {"data-at": "product_description"})
                ingredients = soup.find("div", {"data-comp": "ProductDetailIngredients"})
                price = soup.find("span", {"data-comp": "DisplayPrimaryPrice"})
                ounces = soup.find("span", class_="css-1jcznhx")

            elif "ulta.com" in url:
                image = soup.find("img", class_="ProductMainImage")
                image_url = image['src'] if image else ""
                description = soup.find("div", class_="ProductDescriptionContainer")
                ingredients = soup.find("div", class_="ProductIngredientsContainer")
                price = soup.find("span", class_="ProductPricingPanel-price")
                ounces = ""

            else:
                st.warning("Unsupported site")
                continue

            if image_url:
                st.image(image_url, width=200)

            st.markdown(f"**Description:** {description.text.strip() if description else 'N/A'}")
            st.markdown(f"**Ingredients:** {ingredients.text.strip() if ingredients else 'N/A'}")
            st.markdown(f"**Price:** {price.text.strip() if price else 'N/A'}")
            st.markdown(f"**Ounces:** {ounces.text.strip() if ounces else 'N/A'}")

        except Exception as e:
            st.error(f"Error scraping {url}: {e}")

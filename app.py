import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from urllib.parse import urlparse

st.set_page_config(page_title="Beauty Product Competitive Set Analyzer", layout="wide")
st.title("💄 Beauty Product Competitive Set Analyzer")

st.markdown("""
Paste URLs of product pages below (one per line) from beauty e-commerce sites like Sephora, Ulta, or Goop. 

This tool will attempt to scrape each product and display:
- Image
- Description
- Benefits
- Ingredients
- Price
- Ounces
""")

urls_input = st.text_area("Paste product URLs here:", height=200)

if st.button("Analyze Products") and urls_input:
    urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
    
    data = []

    for url in urls:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, 'html.parser')

            # Default values
            image = description = benefits = ingredients = price = ounces = "Not Found"

            parsed_url = urlparse(url)
            domain = parsed_url.netloc

            # Basic logic for Sephora (can be extended for other domains)
            if "sephora.com" in domain:
                try:
                    image = soup.find("img", {"class": "css-11gn9r6"})['src']
                except:
                    image = ""
                try:
                    description = soup.find("div", {"data-at": "product_description"}).text.strip()
                except:
                    pass
                try:
                    ingredients = soup.find("div", {"data-comp": "ProductDetailIngredients"}).text.strip()
                except:
                    pass
                try:
                    price = soup.find("span", {"data-comp": "DisplayPrimaryPrice"}).text.strip()
                except:
                    pass
                try:
                    ounces = soup.find("span", class_="css-1jcznhx").text.strip()
                except:
                    pass
            elif "ulta.com" in domain:
                try:
                    image = soup.find("img", {"class": "ProductMainImage"})['src']
                except:
                    image = ""
                try:
                    description = soup.find("div", class_="ProductDescriptionContainer").text.strip()
                except:
                    pass
                try:
                    ingredients = soup.find("div", class_="ProductIngredientsContainer").text.strip()
                except:
                    pass
                try:
                    price = soup.find("span", class_="ProductPricingPanel-price").text.strip()
                except:
                    pass
            else:
                description = "Unsupported site"

            data.append({
                "URL": url,
                "Image": image,
                "Description": description,
                "Benefits": benefits,
                "Ingredients": ingredients,
                "Price": price,
                "Ounces": ounces
            })

        except Exception as e:
            st.warning(f"Failed to scrape {url}: {e}")

    if data:
        for product in data:
            with st.expander(product["URL"]):
                cols = st.columns([1, 2])
                if product["Image"]:
                    cols[0].image(product["Image"], width=200)
                cols[1].markdown(f"**Description:** {product['Description']}")
                cols[1].markdown(f"**Ingredients:** {product['Ingredients']}")
                cols[1].markdown(f"**Benefits:** {product['Benefits']}")
                cols[1].markdown(f"**Price:** {product['Price']}")
                cols[1].markdown(f"**Ounces:** {product['Ounces']}")

    else:
        st.info("No data extracted. Check that the URLs are valid and supported.")

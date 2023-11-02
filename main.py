import requests
from bs4 import BeautifulSoup
import smtplib
import lxml
import os

URL = "https://www.amazon.com/gp/product/B09X5DL9S5/ref=ox_sc_saved_title_3?smid=A249FRVY0JGHJA&th=1"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
ACCEPT_LANGUAGE = "en-US,en;q=0.9"
MY_EMAIL = os.environ["MY_EMAIL"]
PASSWORD = os.environ["PASSWORD"]
TO_EMAIL = os.environ["TO_EMAIL"]
TARGET_PRICE = 30.00


headers = {
    "User-Agent": USER_AGENT,
    "Accept-Language": ACCEPT_LANGUAGE,
}

response = requests.get(url=URL, headers=headers)

sp = BeautifulSoup(response.text, "lxml")
price_position = sp.find("span", class_="a-offscreen")
price = price_position.text.split("$")[1]
full_product_name = sp.find("span", id="productTitle").text.strip()  # Strips all unnecessary spaces, symbols, chars, etc
product_name = full_product_name.split("2021")[0]

if float(price) < TARGET_PRICE:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=TO_EMAIL,
                            msg=f"Subject:{product_name} now {price_position.text}\n\n{URL}")



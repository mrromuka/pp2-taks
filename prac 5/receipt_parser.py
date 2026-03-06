import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

price_pattern = re.compile(r"\b\d{1,3}(?: \d{3})*(?:,\d{2})?\b")
prices_str = price_pattern.findall(text)
prices_float = [float(p.replace(" ", "").replace(",", ".")) for p in prices_str]

product_pattern = re.compile(r"\d+\.\s*(.+?)\s+\d+(?:,\d{2})?")
products = product_pattern.findall(text)
products = [p.strip() for p in products]

total_amount = sum(prices_float)

datetime_pattern = re.search(r"\b(\d{2}\.\d{2}\.\d{4}) (\d{2}:\d{2}:\d{2})\b", text)
date = datetime_pattern.group(1) if datetime_pattern else ""
time = datetime_pattern.group(2) if datetime_pattern else ""

payment_pattern = re.search(r"\b(Банковская карта|Cash|Card|Credit|Debit)\b", text)
payment = payment_pattern.group() if payment_pattern else ""

receipt_data = {
    "products": products,
    "prices": prices_float,
    "total_amount": total_amount,
    "date": date,
    "time": time,
    "payment_method": payment
}

print(json.dumps(receipt_data, indent=4, ensure_ascii=False))
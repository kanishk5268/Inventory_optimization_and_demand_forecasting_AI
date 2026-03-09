from data_loader import load_sales_data, get_top_selling_product, get_product_sales

df = load_sales_data()

print("Dataset shape:", df.shape)

top_product = get_top_selling_product()
product_sales = get_product_sales("Field & Stream Sportsman 16 Gun Fire Safe")

print("Top selling product:")
print(top_product)

print("**********************")
print("Product Sales")
print(product_sales)

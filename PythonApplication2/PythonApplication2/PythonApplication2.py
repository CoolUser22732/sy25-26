input("how many items are in stock")

if stock_count == 0:
    print("Out of stock")
elif stock_count <= 5:
    print("Low stock reorder soon")
else:
    print("In stock")

for i in range
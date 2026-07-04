import json
import os

os.makedirs("data", exist_ok=True)
class Product:
    def __init__(self, name, price, quantity, category):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
    def show_info(self):
        print(f"name: {self.name}")
        print(f"price: {self.price}")
        print(f"quantity: {self.quantity}")
        print(f"category: {self.category}")
    def sell(self, amount):
        if self.quantity >= amount:
            self.quantity -= amount
            print(f"{amount} {self.name} sold")
            return True
        else:
            print("Not enough stock")
            return False
    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["price"],
            data["quantity"],
            data["category"]
        )
class Customer:
    def __init__(self,name,customer_id):
        self.name = name
        self.customer_id = customer_id
        self.cart = []
        self.history = []
    def add_to_cart(self,product,amount):
        if product.sell(amount):
            self.cart.append({
                "product": product.name,
                "amount": amount
            })
            self.history.append(f"bought {product.name} x {amount}")

            print("Added to cart")
    def show_cart(self):
        print(f"{self.name} cart:")
        for item in self.cart:
            print(f"{item['product']} x {item['amount']}")

    def return_product(self, product_name, amount, products):
        for item in self.cart:
            if item['product'] == product_name:
                if item['amount'] >= amount:
                    item['amount'] -= amount
                    if item['amount'] == 0 :
                        self.cart.remove(item)
                    for product in products:
                        if product.name == product_name:
                            product.quantity += amount
                            break
                    self.history.append(f'returned {product_name} x {amount}')
                    print(f'{amount} {product_name} returned')
                    return True
                else:
                    print('You dont have this amount')
                    return False
        print('Product not in cart')
        return False

    def to_dict(self):
        return {
            "name": self.name,
            "customer_id": self.customer_id,
            "cart": self.cart,
            "history": self.history
        }
    @classmethod
    def from_dict(cls,data):
        customer = cls(
            data["name"],
            data["customer_id"]
        )
        customer.cart = data["cart"]
        customer.history = data["history"]
        return customer
    
def save_products(products):
    with open("data/products.json","w") as file:
        json.dump([p.to_dict() for p in products],file,indent=4)
def load_products():
    try:
        with open(
            "data/products.json",
            "r"
        ) as file:
            data = json.load(file)
        return [Product.from_dict(item)for item in data]
    except FileNotFoundError:
        return []

def save_customers(customers):
    with open("data/customers.json","w") as file:
        json.dump([c.to_dict() for c in customers],file,indent=4)
def load_customers():
    try:
        with open("data/customers.json", "r") as file:
            data = json.load(file)
        return [Customer.from_dict(item)for item in data]
    
    except FileNotFoundError:
        return []
    
products = load_products()
customers = load_customers()

if len(products) == 0:
    products.append(Product("Laptop",1000,5,"Tech"))
    products.append(Product("Mouse",50,20,"Tech"))
    save_products(products)

if len(customers) == 0:
    Customer = Customer('Ava',1)
    customers.append(Customer)
else:
    Customer = customers[0]

while True:
    print("\n1.Show products")
    print("2.Buy")
    print("3.Cart")
    print("4.Exit")
    print("5.Return product")
    choice = input("choice: ")
    if choice == "1":
        for product in products:
            product.show_info()
    elif choice == "2":
        name = input("product name: ")
        amount = int(input("amount: "))
        found = False
        for product in products:
            if product.name == name:
                customers.add_to_cart(product,amount)
                save_products(products)
                save_customers(customers)
                found = True
                break
        if not found:
            print('product not found')

    elif choice == "3":
        customers.show_cart()
    elif choice == "4":
        save_products(products)
        save_customers(customers)
        print("Goodbye")
        break
    elif choice == "5":
        name = input("product name: ")
        amount = int(input("amount: "))
        customers.return_product(name,amount,products)
    save_products(products)
    save_customers(customers)
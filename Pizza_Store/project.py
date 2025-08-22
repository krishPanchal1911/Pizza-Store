import datetime
import matplotlib.pyplot as plt

class Pizza:
    monthly_sales = {}
    pizza_sales = {} 
    order_history = []  

    sales_file = 'sales_data.txt'  # File to store sales data
    order_file = 'order_history.txt'  # File to store user orders

    def __init__(self):
        self.name = ""
        self.number = ""
        self.menulist = []
        self.total_price = 0  
        self.date = datetime.datetime.now().strftime("%d-%B-%Y") 
        self.month = datetime.datetime.now().strftime("%B")
        
        self.load_sales_data()  # Load previous sales data
        self.load_order_history()  # Load previous user orders
        
    def load_sales_data(self):
        try:
            with open(self.sales_file, 'r') as file:
                for line in file:
                    if line.strip():  # Skip empty lines
                        month, sales_count, pizza_sales = line.strip().split("|")
                        pizza_sales = pizza_sales.split(",")
                        pizza_sales_dict = {}
                        for pizza_sale in pizza_sales:
                            pizza, count = pizza_sale.split(":")
                            pizza_sales_dict[pizza] = int(count)
                        
                        Pizza.monthly_sales[month] = int(sales_count)
                        Pizza.pizza_sales.update(pizza_sales_dict)
        except FileNotFoundError:
            pass  

    def load_order_history(self):
        try:
            with open(self.order_file, 'r') as file:
                for line in file:
                    if line.strip():
                        order_details = line.strip().split(",")
                        Pizza.order_history.append(order_details)
        except FileNotFoundError:
            pass 

    def save_sales_data(self):
        with open(self.sales_file, 'w') as file:
            for month, sales_count in Pizza.monthly_sales.items():
                pizza_sales = []
                for pizza, count in Pizza.pizza_sales.items():
                    pizza_sales.append(f"{pizza}:{count}")
                file.write(f"{month}|{sales_count}|{','.join(pizza_sales)}\n")

    def save_order_history(self):
        with open(self.order_file, 'a') as file:
            file.write(f"{'USER NAME -->',self.name},{'Mobile Number -->',self.number},{','.join([pizza for pizza, _ in self.menulist])},{'TOTAL PRICE-->',self.total_price}\n")

    def input_user_details(self):
        self.name = input("Enter Your Name: ")
        self.number = input("Enter Your Number: ")
        
        trys = 0
        while trys < 3:
            if len(self.number) == 10 and self.number.isdigit():
                print("Your Number Is Successful ✅")
                break
            else:
                print("⚠️ Please Enter a Valid 10-Digit Number!")
                trys += 1
                self.number = input("Enter Your Number Again: ")

    def PizzaMenu(self):
        self.menulist = []  
        self.total_price = 0  

        menu_dict = {
            "regular": [
                ("MARGHERITA", "₹109"),
                ("ACHARI DO PIZZA", "₹119"),
                ("MOROCCAN SPICE PASTA PIZZA", "₹129"),
                ("DOUBLE CHEESE MARGHERITA", "₹139"),
                ("FRESH VEGGIE", "₹149"),
                ("CHEESE N CORN", "₹159"),
                ("CHEESE N TOMATO", "₹169"),
                ("CREAMY TOMATO PIZZA PASTA", "₹179"),
            ],
            "medium": [
                ("MARGHERITA", "₹209"),
                ("ACHARI DO PIZZA", "₹219"),
                ("MOROCCAN SPICE PASTA PIZZA", "₹229"),
                ("DOUBLE CHEESE MARGHERITA", "₹239"),
                ("FRESH VEGGIE", "₹249"),
                ("CHEESE N CORN", "₹259"),
                ("CHEESE N TOMATO", "₹269"),
                ("CREAMY TOMATO PIZZA PASTA", "₹279"),
            ],
            "large": [
                ("MARGHERITA", "₹309"),
                ("ACHARI DO PIZZA", "₹319"),
                ("MOROCCAN SPICE PASTA PIZZA", "₹329"),
                ("DOUBLE CHEESE MARGHERITA", "₹339"),
                ("FRESH VEGGIE", "₹349"),
                ("CHEESE N CORN", "₹359"),
                ("CHEESE N TOMATO", "₹369"),
                ("CREAMY TOMATO PIZZA PASTA", "₹379"),
            ],
        }

        self.size = input("Please Enter Size (Regular/Medium/Large): ").lower()

        if self.size not in menu_dict:
            print("⚠️ Invalid choice! Please enter a correct size.")
            self.show_sales_graphs()  # Show graphs even if size is incorrect
            return  

        menu = menu_dict[self.size]  

        
        print("\n" + "=" * 50)
        print(f"{'🍕 Pizza Name':<35} {'💰 Price'}")
        print("=" * 50)

        for pizza, price in menu:
            print(f"{pizza:<35} {price}")

        print("=" * 50)

        
        print("\n🛒 Please type the name of the pizza you want to order.")
        print("👉 Type 'done' when you are finished ordering.")

        while True:
            order = input("➡️ Enter Pizza Name: ").strip().upper()
            if order == "DONE":
                break
            
            found = False
            for pizza, price in menu:
                if order == pizza.upper():
                    self.menulist.append((pizza, price))
                    self.total_price += int(price[1:])
                    
                    if pizza in Pizza.pizza_sales:
                        Pizza.pizza_sales[pizza] += 1
                    else:
                        Pizza.pizza_sales[pizza] = 1
                    
                    found = True
                    print(f"\n✅ {pizza} added to your order!")
                    break
            if not found:
                print("❌ Pizza not found in the menu! Please enter a valid pizza name.")

        self.update_monthly_sales()

        print("\n🎉 Your Final Order 🎉")
        print("=" * 50)

        if not self.menulist:
            print("⚠️ No pizzas ordered!")
        else:
            for pizza, price in self.menulist:
                print(f"{pizza:<35} {price}")
            print("=" * 50)
            print(f"{'🛒 TOTAL PRICE':<35} ₹{self.total_price}")
            print("=" * 50)

        print("🍕 Thank you for ordering! Enjoy your pizza! 😊")
        self.payment()  
        self.save_order_history()  
        self.save_sales_data() 
        self.show_sales_graphs()  

    def payment(self):
        print("\n💳 **Choose a Payment Method:**")
        print("1️⃣ UPI")
        print("2️⃣ Card")
        print("3️⃣ Cash on Delivery (COD)")

        while True:
            payment_method = input("➡️ Enter Payment Method (UPI/CARD/COD): ").strip().upper()

            if payment_method == "UPI":
                upi_id = input("💳 Enter Your UPI ID: ")
                self.verify_pin("UPI")  
                print(f"✅ Payment of ₹{self.total_price} successful via UPI ({upi_id})!")
                break
            elif payment_method == "CARD":
                card_number = input("💳 Enter Last 4 Digits of Your Card: ")
                self.verify_pin("CARD")  
                print(f"✅ Payment of ₹{self.total_price} successful via Card (**** **** **** {card_number})!")
                break
            elif payment_method == "COD":
                print(f"✅ You have selected **Cash on Delivery**. Please pay ₹{self.total_price} when you receive your order.")
                break
            else:
                print("❌ Invalid Payment Method! Please choose UPI, CARD, or COD.")

    def verify_pin(self, method):
        attempts = 3
        correct_pin = "1234" if method == "CARD" else "654321"  

        while attempts > 0:
            pin = input(f"🔒 Enter {method} PIN ({'4' if method == 'CARD' else '6'} digits): ")

            if pin == correct_pin:
                print("✅ PIN Verified Successfully!")
                return
            else:
                attempts -= 1
                print(f"❌ Incorrect PIN! {attempts} attempts remaining.")

        print("🚨 Transaction Failed! Too many incorrect attempts.")
        exit()

    def update_monthly_sales(self):
        if self.month in Pizza.monthly_sales:
            Pizza.monthly_sales[self.month] += len(self.menulist)
        else:
            Pizza.monthly_sales[self.month] = len(self.menulist)


    def show_sales_graphs(cls):
        cls.show_monthly_sales()
        cls.show_pizza_sales_distribution()


    def show_monthly_sales(cls):
        if not cls.monthly_sales:
            print("⚠️ No sales data available!")
            return

        months = list(cls.monthly_sales.keys())
        sales = list(cls.monthly_sales.values())

        plt.figure(figsize=(50, 5))
        plt.bar(months, sales, color='orange', alpha=0.7)
        plt.xlabel("Months")
        plt.ylabel("Number of Pizzas Sold")
        plt.title(f"📊 Live Pizza Sales - {datetime.datetime.now().strftime('%Y')}")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()


    def show_pizza_sales_distribution(cls):
        if not cls.pizza_sales:
            print("⚠️ No sales data available!")
            return

        pizza_names = list(cls.pizza_sales.keys())
        sales_count = list(cls.pizza_sales.values())

        plt.figure(figsize=(8, 8))
        plt.pie(sales_count, labels=pizza_names, autopct='%1.1f%%', colors=['red','green','yellow','blue','purple','lightgreen','magenta','lightyellow'])
        plt.title("🍕 Pizza Sales Distribution")
        plt.show()

while True:
    p = Pizza()
    p.input_user_details()
    p.PizzaMenu() 

    another_order = input("Do you want to make another order? (yes/no): ").strip().lower()
    if another_order != "yes":
        break
    
import tkinter as tk
from tkinter import messagebox
import mysql.connector as mc
import pymysql as mq


mysqldb = mc.connect(host="localhost", user="root",
                     password="")
mysqlcursor = mysqldb.cursor()
try:
    db = "create database mobilestoredb"
    mysqlcursor.execute(db)
    print("database created")
except:
    print("Database Error..!")
mysqldb.commit()
# mysqlcursor.execute("CREATE TABLE orders (Order_id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(30), Contact_Number VARCHAR(10), Email_id VARCHAR(30), Address VARCHAR(50))")

# mysqlcursor.execute("CREATE TABLE ordered_mobile (Order_id INT, mobile_Name VARCHAR(150), mobile_Price INT, FOREIGN KEY (Order_id) REFERENCES orders(Order_id))")


class mobile:
    def init(self, name, price):
        self.name = name
        self.price = price


class ECommerce:
    def init(self, root):
        self.root = root
        self.root.title("mobile Store")
        self.root.geometry("500x500")
        self.products = [
            mobile("samsung S20 ultra", 50000),
            mobile("Apple iphone 13", 120000),
            mobile("vivo v30e", 85000),
            mobile("oppo A15", 90000),
            mobile("oppo x12", 74000),
            mobile("samsung Zfold", 153000),
            mobile("samsung M11", 18000),
            mobile("onelpus nord 2", 65000),
            mobile("samsung M12", 20000),
            mobile("lava", 8000),
            mobile("oppo A15", 55000),
            mobile("Apple iphone 12", 165000)
        ]

        self.cart = []
        self.customer_info = {
            "Name": tk.StringVar(),
            "Email": tk.StringVar(),
            "Ph. No.": tk.StringVar(),
            "Address": tk.StringVar()
        }

        self.create_button()

    def create_button(self):
        self.mobile = tk.Listbox(self.root, width=400, height=20)
        for laptop in self.products:
            self.mobile.insert(tk.END, f"{mobile.name} - Rs{mobile.price}")
        self.laptops.pack(padx=10, pady=10)

        atc_button = tk.Button(self.root, text="Add to Cart", command=self.atc)
        atc_button.pack(pady=5)

        vc_button = tk.Button(self.root, text="View My Cart", command=self.vc)
        vc_button.pack(pady=5)

    def atc(self):
        sel_mobile = self.mobile.curselection()
        if sel_mobile:
            mobile = self.products[sel_mobile[0]]
            self.cart.append(mobile)
            messagebox.showinfo(
                "Added to Cart", f"{mobile.name} added to your cart!")

    def vc(self):
        if not self.cart:
            messagebox.showinfo("Empty Cart", "Your cart is empty.")
        else:
            self.cust_details()

    def cust_details(self):
        cust_ent = tk.Toplevel(self.root, width=40)
        cust_ent.title("Customer Deatils")
        cust_ent.geometry("300x200")

        tk.Label(cust_ent, text="Name :").grid(row=0, column=0)
        tk.Entry(cust_ent, textvariable=self.customer_info["Name"]).grid(
            row=0, column=1)

        tk.Label(cust_ent, text="Email :").grid(row=1, column=0)
        tk.Entry(cust_ent, textvariable=self.customer_info["Email"]).grid(
            row=1, column=1)

        tk.Label(cust_ent, text="Ph. No. :").grid(row=2, column=0)
        tk.Entry(cust_ent, textvariable=self.customer_info["Ph. No."]).grid(
            row=2, column=1)

        tk.Label(cust_ent, text="Address :").grid(row=3, column=0)
        tk.Entry(cust_ent, textvariable=self.customer_info["Address"]).grid(
            row=3, column=1)

        confirm_button = tk.Button(
            cust_ent, text="Confirm", command=self.confirm_order)
        confirm_button.grid(row=4, column=0, columnspan=2, pady=10)

    def confirm_order(self):
        order_details = tk.Toplevel(self.root)
        order_details.title("Order Confirmation")
        order_details.geometry("600x400")

        name = self.customer_info["Name"].get()
        email = self.customer_info["Email"].get()
        mobile = self.customer_info["Ph. No."].get()
        address = self.customer_info["Address"].get()

        order = f"Customer Details:\nName: {name}\nEmail: {email}\nPh. No : {mobile}\nAddress: {address}\n"
        tk.Label(order_details, text=order).pack(padx=10, pady=10)

        self.cart_items = tk.Listbox(order_details, width=80, height=3)
        for i in self.cart:
            self.cart_items.insert(tk.END, f"{i.name} - Rs{i.price}")
        self.cart_items.pack(padx=10, pady=10)

        total_price = sum([mobile.price for mobile in self.cart])
        totalprice = f"\n\nTotal Price: Rs{total_price}\n"
        self.tp = tk.Label(order_details, text=totalprice)
        self.tp.pack(padx=10, pady=10)

        pob = tk.Button(
            order_details, text="Place Order", command=self.place_order)
        pob.pack(padx=10, pady=10)

        dib = tk.Button(
            order_details, text="Delete item/s", command=self.del_item)
        dib.pack(padx=10, pady=10)

    def place_order(self):
            name = self.customer_info["Name"].get()
            email = self.customer_info["Email"].get()
            mobile = self.customer_info["Ph. No."].get()
            address = self.customer_info["Address"].get()

            mysqlcursor.execute("INSERT INTO orders (Name, Contact_Number, Email_id,Address) VALUES (%s, %s, %s, %s)", (name, mobile, email, address))

            order_id = mysqlcursor.lastrowid
            for m in self.cart:
                mysqlcursor.execute("INSERT INTO ordered_mobile(Order_id, mobile_Name, mobile_Price) VALUES (%s, %s, %s)", (order_id, m.name, m.price))
                mysqldb.commit()
            mysqldb.close()

            messagebox.showinfo("Order Confirmed", "Thank U! Visit Again!!")
            self.root.destroy()

    def del_item(self):
        sel_mobile = self.cart_items.curselection()
        mobile = self.cart[sel_mobile[0]]
        self.cart.remove(mobile)
        messagebox.showinfo("Removed from Cart",
                            "Selected item removed from your cart.")

        self.updatecart()

    def updatecart(self):
        self.cart_items.delete(0, tk.END)
        for laptop in self.cart:
            self.cart_items.insert(tk.END, f"{mobile.name} - Rs{mobile.price}")

        self.updateprice()

    def updateprice(self):
        total_price = sum([mobile.price for mobile in self.cart])
        totalprice = f"\n\nTotal Price: Rs{total_price}\n"
        self.tp.config(text=totalprice)


if __name__ == "main":
    root = tk.Tk()
    a = ECommerce(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox

class RestaurantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Restaurant Management System")
        self.geometry("650x450")

        # Menu items (name: price)
        self.menu = {
            "Pizza": 800,
            "Burger": 450,
            "Pasta": 600,
            "Salad": 300,
            "Juice": 200
        }

        self.orders = []  # store (item, qty, subtotal)

        self.create_widgets()

    def create_widgets(self):
        # Menu selection
        ttk.Label(self, text="Select Item:").pack(pady=5)
        self.item_var = tk.StringVar()
        self.item_combo = ttk.Combobox(self, textvariable=self.item_var, values=list(self.menu.keys()))
        self.item_combo.pack(pady=5)

        # Quantity
        ttk.Label(self, text="Quantity:").pack(pady=5)
        self.qty_var = tk.IntVar(value=1)
        self.qty_spin = ttk.Spinbox(self, from_=1, to=20, textvariable=self.qty_var, width=5)
        self.qty_spin.pack(pady=5)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add to Order", command=self.add_order).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_order).grid(row=0, column=1, padx=5)

        # Treeview for orders
        self.tree = ttk.Treeview(self, columns=("Item", "Qty", "Subtotal"), show="headings", height=8)
        self.tree.heading("Item", text="Item")
        self.tree.heading("Qty", text="Qty")
        self.tree.heading("Subtotal", text="Subtotal (Ksh)")
        self.tree.pack(fill="both", expand=True, pady=10)

        # Total label
        self.total_var = tk.StringVar(value="Total Amount: Ksh 0")
        ttk.Label(self, textvariable=self.total_var, font=("Arial", 12, "bold")).pack(pady=10)

        # Checkout button
        ttk.Button(self, text="Checkout", command=self.checkout).pack(pady=5)

    def add_order(self):
        item = self.item_var.get()
        qty = self.qty_var.get()
        if item not in self.menu:
            messagebox.showerror("Error", "Please select a valid item.")
            return
        subtotal = self.menu[item] * qty
        self.orders.append((item, qty, subtotal))
        self.tree.insert("", "end", values=(item, qty, subtotal))
        self.update_total()

    def remove_order(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Remove", "Please select an item to remove.")
            return
        for sel in selected:
            values = self.tree.item(sel, "values")
            self.orders = [order for order in self.orders if not (order[0] == values[0] and order[1] == int(values[1]) and order[2] == int(values[2]))]
            self.tree.delete(sel)
        self.update_total()

    def update_total(self):
        total = sum(order[2] for order in self.orders)
        self.total_var.set(f"Total Amount: Ksh {total}")

    def checkout(self):
        if not self.orders:
            messagebox.showwarning("Empty Order", "No items in the order.")
            return
        total = sum(order[2] for order in self.orders)
        messagebox.showinfo("Checkout", f"Final Total: Ksh {total}\nThank you for dining with us!")
        self.orders.clear()
        self.tree.delete(*self.tree.get_children())
        self.update_total()

if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()



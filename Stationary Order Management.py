import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Optional safer way, or keep native PhotoImage if file exists


class StationeryOrderManagement:

    def __init__(self, root):
        self.root = root
        self.root.title("Stationery Order Management App")

        # Store stationery items and their prices
        self.stationery_items = {
            "NOTEBOOK": 3,
            "PENCIL PACK": 2,
            "PEN SET": 4,
            "ERASER": 1,
            "GEOMETRY BOX": 6,
            "COLOUR PENCILS": 5,
        }

        # Exchange rate for currency conversion
        self.exchange_rate = 82

        # Set up the Canvas background safely
        self.setup_background(root)

        # Create a themed frame to hold the widgets
        frame = ttk.Frame(root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Heading label
        ttk.Label(
            frame, text="Stationery Order Management", font=("Arial", 20, "bold")
        ).grid(row=0, columnspan=3, padx=10, pady=10)

        # Store references to labels and Entry widgets
        self.item_labels = {}
        self.item_quantities = {}

        # Create one row for every stationery item
        for index, (item, price) in enumerate(
            self.stationery_items.items(), start=1
        ):
            item_label = ttk.Label(
                frame, text=f"{item} (${price}):", font=("Arial", 12)
            )
            item_label.grid(row=index, column=0, padx=10, pady=5)
            self.item_labels[item] = item_label

            quantity_entry = ttk.Entry(frame, width=5)
            quantity_entry.grid(row=index, column=1, padx=10, pady=5)
            self.item_quantities[item] = quantity_entry

        # Variable for storing the selected currency
        self.currency_var = tk.StringVar(value="USD")
        ttk.Label(frame, text="Currency:", font=("Arial", 12)).grid(
            row=len(self.stationery_items) + 1, column=0, padx=10, pady=5
        )

        # Currency selection dropdown
        currency_dropdown = ttk.Combobox(
            frame,
            textvariable=self.currency_var,
            state="readonly",
            width=18,
            values=("USD", "INR"),
        )
        currency_dropdown.grid(
            row=len(self.stationery_items) + 1, column=1, padx=10, pady=5
        )
        currency_dropdown.current(0)

        # Update prices whenever the currency changes (using trace_add)
        self.currency_var.trace_add("write", self.update_item_prices)

        # Button to place the stationery order
        order_button = ttk.Button(
            frame, text="Place Order", command=self.place_order
        )
        order_button.grid(
            row=len(self.stationery_items) + 2, columnspan=3, padx=10, pady=10
        )

    def setup_background(self, root):
        background_width = 800
        background_height = 600
        canvas = tk.Canvas(root, width=background_width, height=background_height)
        canvas.pack()

        try:
            # Load and safely resize image if Classroom.jpg exists
            original_image = Image.open("Classroom.jpg")
            resized_image = original_image.resize(
                (background_width, background_height), Image.Resampling.LANCZOS
            )
            self.background_image = ImageTk.PhotoImage(resized_image)
            canvas.create_image(
                0, 0, anchor=tk.NW, image=self.background_image
            )
        except Exception:
            # Fallback background color if image is missing
            canvas.configure(bg="#f0f0f0")
            canvas.create_text(
                background_width // 2,
                background_height // 2,
                text="[Classroom.jpg not found - Solid Background]",
                font=("Arial", 14),
                fill="gray",
            )

    def update_item_prices(self, *args):
        currency = self.currency_var.get()
        symbol = "₹" if currency == "INR" else "$"
        rate = self.exchange_rate if currency == "INR" else 1

        for item, label in self.item_labels.items():
            price = self.stationery_items[item] * rate
            label.config(text=f"{item} ({symbol}{price}):")

    def place_order(self):
        total_cost = 0
        order_summary = "Stationery Order Summary:\n\n"
        currency = self.currency_var.get()
        symbol = "₹" if currency == "INR" else "$"
        rate = self.exchange_rate if currency == "INR" else 1

        items_ordered = 0

        for item, entry in self.item_quantities.items():
            val = entry.get().strip()
            if val.isdigit():
                quantity = int(val)
                if quantity > 0:
                    price = self.stationery_items[item] * rate
                    cost = quantity * price
                    total_cost += cost
                    order_summary += (
                        f"{item}: {quantity} x {symbol}{price} = {symbol}{cost}\n"
                    )
                    items_ordered += 1

        if items_ordered > 0:
            order_summary += f"\nTotal Cost: {symbol}{total_cost}"
            messagebox.showinfo("Order Placed", order_summary)
        else:
            messagebox.showerror(
                "Error", "Please order at least one stationery item with a valid number."
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = StationeryOrderManagement(root)
    root.geometry("800x600")
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

# Import matplotlib libraries to embed the charts inside the GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from tracker import ExpenseTracker
from expense import Expense

tracker = ExpenseTracker()

# ================= WINDOW =================
root = tk.Tk()
root.title("Smart Expense Tracker Pro")

# 🎨 Purple palette matching your design perfectly
BG = "#F3E8FF"          # Light purple for the main application background
PRIMARY = "#6D28D9"     # Deep purple for headers and buttons
TEXT_COLOR = "#1F2937"  # Dark gray color for readable text

root.configure(bg=BG)

# Safely maximize the window across different OS platforms without TclError
try:
    root.state('zoomed')
except tk.TclError:
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

# ================= TOP BAR (HEADER) =================
header_frame = tk.Frame(root, bg=BG)
header_frame.pack(fill="x", padx=30, pady=20)

title_label = tk.Label(
    header_frame,
    text="✨ SMART EXPENSE TRACKER PRO",
    font=("Segoe UI", 26, "bold"),
    bg=BG,
    fg=PRIMARY
)
title_label.pack(side="left")

# ================= MAIN CONTAINER =================
main_container = tk.Frame(root, bg=BG)
main_container.pack(fill="both", expand=True, padx=30)

left_panel = tk.Frame(main_container, bg=BG)
left_panel.pack(side="left", fill="both", expand=True, padx=(0, 15))

right_panel = tk.Frame(main_container, bg="#FFFFFF", width=420, bd=0, highlightthickness=1, highlightbackground="#E5E7EB")
right_panel.pack(side="right", fill="both", padx=(15, 0), pady=(0, 20))
right_panel.pack_propagate(False)

# ================= DASHBOARD CARDS (STATS) =================
cards_frame = tk.Frame(left_panel, bg=BG)
cards_frame.pack(fill="x", pady=(0, 15))

def create_card(parent, title, value, color):
    card = tk.Frame(parent, bg="#FFFFFF", bd=0, highlightthickness=1, highlightbackground="#E5E7EB")
    card.pack(side="left", fill="both", expand=True, padx=6, ipady=12)
    
    lbl_title = tk.Label(card, text=title, font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#4B5563")
    lbl_title.pack(pady=(10, 2))
    
    lbl_val = tk.Label(card, text=value, font=("Segoe UI", 20, "bold"), bg="#FFFFFF", fg=color)
    lbl_val.pack(pady=(0, 10))
    return lbl_val

lbl_total = create_card(cards_frame, "Total Expenses", "₹0.00", "#DC2626")
lbl_budget = create_card(cards_frame, "Budget", f"₹{tracker.monthly_budget:.2f}", PRIMARY)
lbl_remain = create_card(cards_frame, "Remaining", "₹0.00", "#059669")

# ================= INPUT FORM CARD =================
form_card = tk.Frame(left_panel, bg="#FFFFFF", highlightthickness=1, highlightbackground="#E5E7EB")
form_card.pack(fill="x", pady=10, ipady=12)

fields_frame = tk.Frame(form_card, bg="#FFFFFF")
fields_frame.pack(padx=20, pady=10, fill="x")

entry_style = {"font": ("Segoe UI", 11), "bd": 1, "relief": "solid", "highlightthickness": 0, "bg": "#FFFFFF", "fg": TEXT_COLOR}

tk.Label(fields_frame, text="Amount", bg="#FFFFFF", fg=TEXT_COLOR, font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w", pady=8)
amount_entry = tk.Entry(fields_frame, width=20, **entry_style)
amount_entry.grid(row=0, column=1, padx=(10, 30), sticky="ew")

tk.Label(fields_frame, text="Category", bg="#FFFFFF", fg=TEXT_COLOR, font=("Segoe UI", 11, "bold")).grid(row=0, column=2, sticky="w", pady=8)
category_box = ttk.Combobox(fields_frame, width=18, font=("Segoe UI", 11), state="readonly", values=["Food", "Transport", "Shopping", "Makeup", "Bills", "Entertainment", "Other"])
category_box.grid(row=0, column=3, sticky="ew")

tk.Label(fields_frame, text="Description", bg="#FFFFFF", fg=TEXT_COLOR, font=("Segoe UI", 11, "bold")).grid(row=1, column=0, sticky="w", pady=8)
description_entry = tk.Entry(fields_frame, width=20, **entry_style)
description_entry.grid(row=1, column=1, padx=(10, 30), sticky="ew")

tk.Label(fields_frame, text="Date", bg="#FFFFFF", fg=TEXT_COLOR, font=("Segoe UI", 11, "bold")).grid(row=1, column=2, sticky="w", pady=8)
date_picker = DateEntry(fields_frame, width=18, font=("Segoe UI", 11), date_pattern="yyyy-mm-dd", background=PRIMARY, foreground="white", borderwidth=1)
date_picker.grid(row=1, column=3, sticky="ew")

fields_frame.columnconfigure((1, 3), weight=1)

# ================= SEARCH BAR =================
search_bar_frame = tk.Frame(left_panel, bg=BG)
search_bar_frame.pack(fill="x", pady=5)

tk.Label(search_bar_frame, text="🔍 Search Category:", bg=BG, fg=TEXT_COLOR, font=("Segoe UI", 11, "bold")).pack(side="left", padx=(5, 10))
search_entry = tk.Entry(search_bar_frame, font=("Segoe UI", 11), bd=1, relief="solid", bg="#FFFFFF", fg=TEXT_COLOR)
search_entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 10))

# ================= TABLE CARD (TREEVIEW WITH FIXED COLOR) =================
table_card = tk.Frame(left_panel, bg=BG)
table_card.pack(fill="both", expand=True, pady=10)

# Switching theme to 'alt' allows full control over colors and forces the purple background
style = ttk.Style()
style.theme_use("alt") 

style.configure(
    "Treeview", 
    rowheight=35, 
    font=("Segoe UI", 10),
    background=BG,           # Main background for row cells
    fieldbackground=BG,      # Converts the empty space at the bottom to light purple
    foreground=TEXT_COLOR,
    borderwidth=0
)

# Styling table column header bars
style.configure(
    "Treeview.Heading", 
    background=PRIMARY, 
    foreground="white", 
    font=("Segoe UI", 11, "bold"), 
    relief="flat"
)
style.map("Treeview.Heading", background=[('active', PRIMARY)])

# Color used when selecting a row with the mouse
style.map("Treeview", background=[("selected", "#DDD6FE")], foreground=[("selected", PRIMARY)])

# Initializing the standard, stable Treeview
tree = ttk.Treeview(table_card, columns=("ID", "Amount", "Category", "Description", "Date"), show="headings")

vsb = ttk.Scrollbar(table_card, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)

tree.heading("ID", text="ID")
tree.heading("Amount", text="Amount (₹)")
tree.heading("Category", text="Category")
tree.heading("Description", text="Description")
tree.heading("Date", text="Date")

tree.column("ID", width=60, anchor="center")
tree.column("Amount", width=110, anchor="center")
tree.column("Category", width=140, anchor="center")
tree.column("Description", width=220, anchor="w")
tree.column("Date", width=130, anchor="center")

tree.pack(side="left", fill="both", expand=True)
vsb.pack(side="right", fill="y")

# Adding alternating grid row colors for a clean and professional appearance
tree.tag_configure('evenrow', background="#EAD7FE")
tree.tag_configure('oddrow', background="#F3E8FF")

# ================= ACTIONS & BUTTONS BAR =================
button_frame = tk.Frame(left_panel, bg=BG)
button_frame.pack(fill="x", pady=(10, 20))

def btn_factory(parent, text, command, bg_color):
    return tk.Button(parent, text=text, command=command, bg=bg_color, fg="white", font=("Segoe UI", 10, "bold"), bd=0, width=13, height=2, cursor="hand2")

btn_factory(button_frame, "➕ Add", lambda: add_expense(), PRIMARY).pack(side="left", padx=4)
btn_factory(button_frame, "✏ Edit", lambda: edit_expense(), "#2563EB").pack(side="left", padx=4)
btn_factory(button_frame, "🗑 Delete", lambda: delete_expense(), "#DC2626").pack(side="left", padx=4)
btn_factory(button_frame, "🔍 Search", lambda: search_expense(), "#4F46E5").pack(side="left", padx=4)
btn_factory(button_frame, "📁 Export", tracker.export_to_excel, "#D97706").pack(side="left", padx=4)

# ================= CORE FUNCTIONS (LOGIC) =================

def update_dashboard():
    total = float(tracker.df["Amount"].sum()) if not tracker.df.empty else 0.0
    lbl_total.config(text=f"₹{total:.2f}")
    lbl_budget.config(text=f"₹{tracker.monthly_budget:.2f}")
    
    remaining = tracker.monthly_budget - total
    lbl_remain.config(text=f"₹{remaining:.2f}", fg="#059669" if remaining >= 0 else "#DC2626")
    
    render_charts()

def refresh_table(dataframe=None):
    for item in tree.get_children():
        tree.delete(item)
    
    target_df = dataframe if dataframe is not None else tracker.df
    
    count = 0
    for idx, row in target_df.iterrows():
        row_tag = 'evenrow' if count % 2 == 0 else 'oddrow'
        tree.insert("", "end", values=(idx, f"{float(row['Amount']):.2f}", row["Category"], row["Description"], row["Date"]), tags=(row_tag,))
        count += 1
    
    update_dashboard()

def select_item(event):
    selected = tree.focus()
    values = tree.item(selected, "values")
    if values:
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, values[1])
        category_box.set(values[2])
        description_entry.delete(0, tk.END)
        description_entry.insert(0, values[3])
        try:
            date_picker.set_date(datetime.strptime(values[4], "%Y-%m-%d"))
        except:
            pass

tree.bind("<<TreeviewSelect>>", select_item)

def add_expense():
    try:
        if not amount_entry.get() or not category_box.get():
            messagebox.showwarning("Warning", "Please fill Amount and Category")
            return
        expense = Expense(float(amount_entry.get()), category_box.get(), description_entry.get(), date_picker.get())
        tracker.add_expense(expense)
        refresh_table()
        clear_form()
    except:
        messagebox.showerror("Error", "Invalid data format")

def edit_expense():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a row to edit")
        return
    try:
        idx = int(tree.item(selected, "values")[0])
        tracker.edit_expense(idx, float(amount_entry.get()), category_box.get(), description_entry.get(), date_picker.get())
        refresh_table()
        clear_form()
        messagebox.showinfo("Success", "Updated Successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_expense():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a row to delete")
        return
    idx = int(tree.item(selected, "values")[0])
    tracker.delete_expense(idx)
    refresh_table()
    clear_form()

def search_expense():
    query = search_entry.get().strip().lower()
    if query == "":
        refresh_table()
    else:
        filtered_df = tracker.df[tracker.df["Category"].str.lower().str.contains(query) | tracker.df["Description"].str.lower().str.contains(query)]
        refresh_table(filtered_df)

def clear_form():
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    category_box.set("")

search_entry.bind("<KeyRelease>", lambda e: search_expense() if search_entry.get().strip() == "" else None)

# ================= EMBEDDED CHARTS =================
def render_charts():
    for widget in right_panel.winfo_children():
        widget.destroy()
        
    tk.Label(right_panel, text="Expense Summary", font=("Segoe UI", 14, "bold"), bg="#FFFFFF", fg=PRIMARY).pack(pady=15)
    
    if tracker.df.empty:
        tk.Label(right_panel, text="No Data Available for Charts", font=("Segoe UI", 11), bg="#FFFFFF", fg="gray").pack(expand=True)
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4, 6.5), facecolor="#FFFFFF")
    fig.tight_layout(pad=4.0)

    # 1. Pie Chart Configuration
    cat_data = tracker.df.groupby("Category")["Amount"].sum()
    colors = ['#8B5CF6', '#EC4899', '#3B82F6', '#F59E0B', '#10B981', '#6366F1', '#A78BFA']
    ax1.pie(cat_data, labels=cat_data.index, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 8, 'color': TEXT_COLOR})
    ax1.axis('equal')
    ax1.set_title("Category Distribution", fontdict={'fontsize': 10, 'weight': 'bold', 'color': PRIMARY})

    # 2. Bar Chart Configuration
    ax2.bar(cat_data.index, cat_data.values, color=PRIMARY, width=0.4)
    ax2.set_title("Category Wise Expenses", fontdict={'fontsize': 10, 'weight': 'bold', 'color': PRIMARY})
    ax2.tick_params(axis='x', labelsize=8, labelrotation=15, colors=TEXT_COLOR)
    ax2.tick_params(axis='y', labelsize=8, colors=TEXT_COLOR)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)

    canvas = FigureCanvasTkAgg(fig, master=right_panel)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
    plt.close(fig)

# ================= FOOTER =================
tk.Label(root, text="Developed by Nada Mohammad", bg=BG, fg="#7C3AED", font=("Segoe UI", 9, "bold")).pack(side="bottom", pady=10)

# ================= START APP =================
refresh_table()
root.mainloop()
import pandas as pd

class ExpenseTracker:
    def __init__(self):
        self.file_name = "expenses.csv"
        self.monthly_budget = 10000
        try:
            # نقرأ الملف ونجعل العمود الأول هو الـ Index إذا لم يكن فارغاً
            self.df = pd.read_csv(self.file_name)
        except:
            self.df = pd.DataFrame(
                columns=[
                    "Amount",
                    "Category",
                    "Description",
                    "Date"
                ]
            )

    def save_data(self):
        self.df.to_csv(
            self.file_name,
            index=True # نضع index=True لكي يحافظ pandas على رقم السطر الثابت (ID) ولا يتغير عند الحذف
        )

    def add_expense(self, expense):
        new_data = pd.DataFrame([expense.to_dict()])
        self.df = pd.concat(
            [self.df, new_data],
            ignore_index=True
        )
        self.save_data()
        print("\nExpense Added Successfully!")

    def view_expenses(self):
        if self.df.empty:
            print("\nNo Expenses Found!")
        else:
            print("\n===== All Expenses =====")
            print(
                self.df.reset_index().to_string(index=False)
            )

    def total_expenses(self):
        total = self.df["Amount"].sum()
        print(f"\nTotal Expenses = ₹{total:.2f}")

    def category_summary(self):
        if self.df.empty:
            print("\nNo Expenses Found!")
        else:
            summary = self.df.groupby(
                "Category"
            )["Amount"].sum()
            print("\n===== Category Summary =====")
            print(summary)

    def delete_expense(self, index):
        if index in self.df.index:
            # نحذف السطر بدون عمل reset_index لكي لا تتغير أرقام السطور الأخرى
            self.df = self.df.drop(index)
            self.save_data()
            print("\nExpense Deleted Successfully!")
        else:
            print("\nInvalid Expense ID!")

    def edit_expense(
        self,
        index,
        amount,
        category,
        description,
        date
    ):
        if index in self.df.index:
            self.df.at[index, "Amount"] = amount
            self.df.at[index, "Category"] = category
            self.df.at[index, "Description"] = description
            self.df.at[index, "Date"] = date
            self.save_data()
            print("\nExpense Updated Successfully!")
        else:
            print("\nInvalid Expense ID!")

    def set_budget(self, budget):
        self.monthly_budget = budget
        print(
            f"\nMonthly Budget set to ₹{budget:.2f}"
        )

    def check_budget(self):
        if self.monthly_budget == 0:
            print("\nNo Budget Set!")
            return
        total = self.df["Amount"].sum()
        print(
            f"\nMonthly Budget : ₹{self.monthly_budget:.2f}"
        )
        print(
            f"Current Expenses : ₹{total:.2f}"
        )
        remaining = self.monthly_budget - total
        if total > self.monthly_budget:
            print("\n⚠️ WARNING: Budget Exceeded!")
        else:
            print(
                f"\nRemaining Budget : ₹{remaining:.2f}"
            )

    def search_category(self, category):
        result = self.df[
            self.df["Category"].str.lower()
            == category.lower()
        ]
        if result.empty:
            print("\nNo matching expenses found!")
            return pd.DataFrame()
        else:
            return result

    def export_to_excel(self):
        if self.df.empty:
            print("\nNo Expenses to Export!")
        else:
            self.df.to_excel(
                "expense_report.xlsx",
                index=False
            )
            print(
                "\nExcel file created successfully!"
            )
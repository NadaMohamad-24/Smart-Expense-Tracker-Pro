class Expense:

    def __init__(self, amount, category, description, date):

        self.amount = amount
        self.category = category
        self.description = description
        self.date = date


    def to_dict(self):

        return {
            "Amount": self.amount,
            "Category": self.category,
            "Description": self.description,
            "Date": self.date
        }


    def __str__(self):

        return f"{self.date} | {self.category} | ₹{self.amount} | {self.description}"
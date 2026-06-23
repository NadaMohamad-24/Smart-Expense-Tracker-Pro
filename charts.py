import matplotlib.pyplot as plt


def pie_chart(df):

    if df.empty:
        print("No expenses to display!")
        return

    data = df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(7, 7))

    plt.pie(
        data,
        labels=data.index,
        autopct="%1.1f%%"
    )

    plt.title("Expense Distribution")

    plt.show()


def bar_chart(df):

    if df.empty:
        print("No expenses to display!")
        return

    data = df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(8, 5))

    plt.bar(
        data.index,
        data.values
    )

    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")

    plt.show()
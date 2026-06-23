from tracker import ExpenseTracker
from expense import Expense
from charts import pie_chart, bar_chart

tracker = ExpenseTracker()

while True:

    print("\n" + "=" * 45)
    print("        SMART EXPENSE TRACKER")
    print("=" * 45)

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Expenses")
    print("4. Category Summary")
    print("5. Delete Expense")
    print("6. Edit Expense")
    print("7. Set Budget")
    print("8. Check Budget")
    print("9. Pie Chart")
    print("10. Bar Chart")
    print("11. Search by Category")
    print("12. Export to Excel")
    print("13. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":

        amount = float(input("Enter Amount: ₹"))
        category = input("Enter Category: ")
        description = input("Enter Description: ")
        date = input("Enter Date (YYYY-MM-DD): ")

        expense = Expense(
            amount,
            category,
            description,
            date
        )

        tracker.add_expense(expense)

    elif choice == "2":

        tracker.view_expenses()

    elif choice == "3":

        tracker.total_expenses()

    elif choice == "4":

        tracker.category_summary()

    elif choice == "5":

        tracker.view_expenses()

        expense_id = int(
            input("\nEnter Expense ID to delete: ")
        )

        tracker.delete_expense(expense_id)

    elif choice == "6":

        tracker.view_expenses()

        expense_id = int(
            input("\nEnter Expense ID to edit: ")
        )

        amount = float(
            input("New Amount: ₹")
        )

        category = input(
            "New Category: "
        )

        description = input(
            "New Description: "
        )

        date = input(
            "New Date (YYYY-MM-DD): "
        )

        tracker.edit_expense(
            expense_id,
            amount,
            category,
            description,
            date
        )

    elif choice == "7":

        budget = float(
            input("Enter Monthly Budget: ₹")
        )

        tracker.set_budget(budget)

    elif choice == "8":

        tracker.check_budget()

    elif choice == "9":

        pie_chart(tracker.df)

    elif choice == "10":

        bar_chart(tracker.df)

    elif choice == "11":

        category = input(
            "Enter Category: "
        )

        tracker.search_category(category)

    elif choice == "12":

        tracker.export_to_excel()

    elif choice == "13":

        print(
            "\nThank you for using Smart Expense Tracker!"
        )

        break

    else:

        print(
            "\nInvalid Choice! Please try again."
        )
import json

income = []
expenses = {}
balance = 0
budget_limit = None

# Menu to choose what to do
def show_menu():
    print("\n-----------------------------------")
    print("        My Budget Tracker          ")
    print("-----------------------------------")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Balance")
    print("4. View Income and Expenses")
    print("5. Set Budget Limit")
    print("6. Save Data")
    print("7. Load Data")
    print("8. Exit")

# Add Multiple Incomes
def add_multiple_incomes():
    amounts = input("Enter the income amounts separated by commas: ").split(',')
    for amount in amounts:
        try:
            income.append(float(amount.strip()))
        except ValueError:
            print(f"Invalid amount '{amount}'. Skipping...")
    update_balance()
    print("Incomes added successfully.")

# Add Multiple Expenses
def add_multiple_expenses():
    while True:
        category = input("Enter the expense category (e.g. Monthly Expenses, Sundry Expenses, Savings): ")
        amounts = input("Enter the expense amounts separated by commas: ").split(',')
        if category not in expenses:
            expenses[category] = []
        for amount in amounts:
            try:
                expenses[category].append(float(amount.strip()))
            except ValueError:
                print(f"Invalid amount '{amount}' in category '{category}'. Skipping...")
        update_balance()
        print("Expenses added successfully.")
        more = input("Add more expenses? (yes/no): ").strip().lower()
        if more != 'yes':
            break
    check_budget_limit()

# Remove Income or Expense
def remove_entry():
    choice = input("Remove (1) Income or (2) Expense? ")
    if choice == "1":
        index = int(input("Enter the index of the income to remove: ")) - 1
        if 0 <= index < len(income):
            removed = income.pop(index)
            update_balance()
            print(f"Removed R{removed} from income.")
        else:
            print("Invalid index.")
    elif choice == "2":
        category = input("Enter the expense category: ")
        if category in expenses:
            print("Expenses in this category:")
            for i, exp in enumerate(expenses[category]):
                print(f"{i + 1}. R{exp:.2f}")
            index = int(input("Enter the index of the expense to remove: ")) - 1
            if 0 <= index < len(expenses[category]):
                removed = expenses[category].pop(index)
                if not expenses[category]:  # Remove category if empty
                    del expenses[category]
                update_balance()
                print(f"Removed R{removed} from {category} expenses.")
            else:
                print("Invalid index.")
        else:
            print("Category not found.")
    else:
        print("Invalid choice.")

# Update Balance
def update_balance():
    global balance
    balance = sum(income) - sum(sum(exp_list) for exp_list in expenses.values())

# View Balance
def view_balance():
    print(f"Your current balance is: R{balance:.2f}")

# View Income and Expenses
def view_transactions():
    print("\nIncome:")
    for i, inc in enumerate(income, 1):
        print(f"{i}. R{inc:.2f}")
    print("\nExpenses:")
    for category, exp_list in expenses.items():
        print(f"{category}:")
        for i, exp in enumerate(exp_list, 1):
            print(f"  {i}. R{exp:.2f}")

# Set Budget Limit
def set_budget_limit():
    global budget_limit
    budget_limit = float(input("Enter your budget limit: R"))
    print(f"Budget limit set to R{budget_limit:.2f}")

def check_budget_limit():
    if budget_limit is not None and sum(sum(exp_list) for exp_list in expenses.values()) > budget_limit:
        print("Warning: You have exceeded your budget limit!")

# Save Data to File
def save_data():
    data = {
        "income": income,
        "expenses": expenses,
        "budget_limit": budget_limit
    }
    with open('budget_data.json', 'w') as f:
        json.dump(data, f)
    print("Data saved successfully!")

# Load Data from File
def load_data():
    global income, expenses, budget_limit, balance
    try:
        with open('budget_data.json', 'r') as f:
            data = json.load(f)
            income = data.get("income", [])
            expenses = data.get("expenses", {})
            budget_limit = data.get("budget_limit")
            update_balance()
            print("Data loaded successfully!")
    except FileNotFoundError:
        print("No saved data found.")

def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-9): ")

        if choice == "1":
            add_multiple_incomes()
        elif choice == "2":
            add_multiple_expenses()
        elif choice == "3":
            remove_entry()
        elif choice == "4":
            view_balance()
        elif choice == "5":
            view_transactions()
        elif choice == "6":
            set_budget_limit()
        elif choice == "7":
            save_data()
        elif choice == "8":
            load_data()
        elif choice == "9":
            print("Exiting Budget Tracker. Goodbye!")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
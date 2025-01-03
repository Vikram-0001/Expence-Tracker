import sqlite3
import matplotlib.pyplot as plt

class ExpenseTracker:
    def __init__(self, db_name="new.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                category TEXT,
                description TEXT
            )
        """)
        self.conn.commit()

    def add_expense(self, amount, category, description):
        self.cursor.execute("""
            INSERT INTO expenses (amount, category, description)
            VALUES (?, ?, ?)
        """, (amount, category, description))
        self.conn.commit()
        print("Expense added successfully.")

    def view_expenses(self):
        self.cursor.execute("SELECT id, amount, category, description FROM expenses")
        expenses = self.cursor.fetchall()
        
        if not expenses:
            print("No expenses recorded.")
            return
        
        print("All Expenses:")
        for expense in expenses:
            print(f"{expense[0]}. Amount: {expense[1]}, Category: {expense[2]}, Description: {expense[3]}")

    def get_total_expense(self):
        self.cursor.execute("SELECT SUM(amount) FROM expenses")
        total = self.cursor.fetchone()[0]
        total = total if total else 0
        print(f"Total Expense: {total}")

    def get_expenses_by_category(self, category):
        self.cursor.execute("""
            SELECT amount, description FROM expenses
            WHERE category = ?
        """, (category,))
        category_expenses = self.cursor.fetchall()

        if not category_expenses:
            print(f"No expenses recorded in category: {category}")
            return

        print(f"Expenses in category '{category}':")
        for i, expense in enumerate(category_expenses, start=1):
            print(f"{i}. Amount: {expense[0]}, Description: {expense[1]}")

    def plot_expenses_by_category(self):
        self.cursor.execute("""
            SELECT category, SUM(amount) FROM expenses
            GROUP BY category
        """)
        data = self.cursor.fetchall()

        if not data:
            print("No expenses recorded.")
            return

        labels, amounts = zip(*data)

        plt.figure(figsize=(10, 5))
        plt.bar(labels, amounts, color='skyblue')
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.title('Expenses by Category')
        plt.show()

    def close(self):
        self.conn.close()

def main():
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Expense")
        print("4. View Expenses by Category")
        print("5. Plot Expenses by Category")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.add_expense(amount, category, description)
        elif choice == '2':
            tracker.view_expenses()
        elif choice == '3':
            tracker.get_total_expense()
        elif choice == '4':
            category = input("Enter category: ")
            tracker.get_expenses_by_category(category)
        elif choice == '5':
            tracker.plot_expenses_by_category()
        elif choice == '6':
            tracker.close()
            print("Exiting the Expense Tracker.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
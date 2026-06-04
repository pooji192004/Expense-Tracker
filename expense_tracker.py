import sqlite3
from datetime import datetime

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        date        TEXT,
        category    TEXT,
        description TEXT,
        amount      REAL
    )
''')
conn.commit()

def add_expense():
    print("\n--- Add New Expense ---")
    date = datetime.today().strftime("%Y-%m-%d")
    print("Categories: Food, Travel, Shopping, Bills, Health, Education, Other")
    category = input("Enter category: ").strip().capitalize()
    description = input("Enter description: ").strip()
    try:
        amount = float(input("Enter amount (Rs): "))
    except ValueError:
        print("Invalid amount!")
        return
    cursor.execute('''
        INSERT INTO expenses (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))
    conn.commit()
    print(f"Expense of Rs {amount:.2f} added successfully!")

def view_expenses():
    print("\n--- All Expenses ---")
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    if not rows:
        print("No expenses found.")
        return
    print(f"\n{'ID':<5} {'Date':<12} {'Category':<12} {'Description':<25} {'Amount':>10}")
    print("-" * 68)
    for row in rows:
        id_, date, category, description, amount = row
        print(f"{id_:<5} {date:<12} {category:<12} {description:<25} Rs{amount:>9.2f}")
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    print("-" * 68)
    print(f"{'TOTAL':>56} Rs{total:>9.2f}")

def category_summary():
    print("\n--- Category-wise Summary ---")
    cursor.execute('''
        SELECT category, COUNT(*) as count, SUM(amount) as total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    ''')
    rows = cursor.fetchall()
    if not rows:
        print("No expenses found.")
        return
    print(f"\n{'Category':<15} {'No. of Entries':<18} {'Total Amount':>12}")
    print("-" * 48)
    for category, count, total in rows:
        print(f"{category:<15} {count:<18} Rs{total:>11.2f}")

def monthly_report():
    print("\n--- Monthly Report ---")
    month = input("Enter month (YYYY-MM), e.g. 2026-06: ").strip()
    cursor.execute('''
        SELECT category, description, amount, date
        FROM expenses
        WHERE date LIKE ?
        ORDER BY date
    ''', (month + "%",))
    rows = cursor.fetchall()
    if not rows:
        print(f"No expenses found for {month}.")
        return
    print(f"\n{'Category':<12} {'Description':<25} {'Amount':>10} {'Date':<12}")
    print("-" * 62)
    total = 0
    for category, description, amount, date in rows:
        print(f"{category:<12} {description:<25} Rs{amount:>9.2f} {date:<12}")
        total += amount
    print("-" * 62)
    print(f"{'TOTAL for ' + month:>49} Rs{total:>9.2f}")

def delete_expense():
    view_expenses()
    print("\n--- Delete Expense ---")
    try:
        expense_id = int(input("Enter the ID of expense to delete: "))
    except ValueError:
        print("Invalid ID!")
        return
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    row = cursor.fetchone()
    if not row:
        print(f"No expense found with ID {expense_id}.")
        return
    confirm = input(f"Delete '{row[3]}' (Rs {row[4]:.2f})? (yes/no): ")
    if confirm.lower() == "yes":
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        print("Expense deleted successfully!")
    else:
        print("Deletion cancelled.")

def main():
    print("\n" + "=" * 40)
    print("   EXPENSE TRACKER - Welcome!")
    print("=" * 40)
    while True:
        print("\nMENU:")
        print("  1. Add Expense")
        print("  2. View All Expenses")
        print("  3. Category Summary")
        print("  4. Monthly Report")
        print("  5. Delete Expense")
        print("  6. Exit")
        choice = input("\nEnter your choice (1-6): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            category_summary()
        elif choice == "4":
            monthly_report()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("\nGoodbye! Keep tracking your expenses!")
            conn.close()
            break
        else:
            print("Invalid choice. Please enter 1 to 6.")

if __name__ == "__main__":
    main()

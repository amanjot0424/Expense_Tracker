import sys
from src.models import BudgetManager, Income, Expense
from src.storage import StorageEngine
from src.utils import get_validated_float, get_non_empty_string

DATA_FILE = "data/tracker_data.json"

def main():
    manager = BudgetManager()
    
    # Initialize and read state from storage backend
    StorageEngine.load_data(manager, DATA_FILE)
    
    print("=" * 45)
    print("Welcome to your Personal Finance Architecture Engine")
    print("=" * 45)
    
    while True:
        print("\n--- Main Controls ---")
        print("1. Add Income Source")
        print("2. Log Expense Transaction")
        print("3. View Chronological Activity Stream")
        print("4. View Complete Financial Metrics Matrix")
        print("5. Save and Terminate Execution")
        print("6. Set Category Budget Limit")
        print("7. Filter Activity Stream by Category")
        print("8. Export Statement to Text File")
        print("9. Purge/Delete Transaction Entry")

        
        choice = input("\nSelect menu option (1-9): ").strip()
        
        if choice == "1":
            amount = get_validated_float("Enter incoming revenue amount ($): ")
            category = get_non_empty_string("Enter revenue category (e.g., Salary, Freelance): ")
            income_obj = Income(amount, category)
            manager.add_transaction(income_obj)
            print(f"Success: {income_obj.get_details()} registered.")
            
        elif choice == "2":
            amount = get_validated_float("Enter layout expense amount ($): ")
            category = get_non_empty_string("Enter expenditure category (e.g., Food, Rent, Bills): ")
            expense_obj = Expense(amount, category)
            manager.add_transaction(expense_obj)
            print(f"Success: {expense_obj.get_details()} registered.")
            
        elif choice == "3":
            print("\n--- Chronological Activity Stream ---")
            if not manager.transactions:
                print("No transactions currently documented in session ledger.")
            else:
                for index, tx in enumerate(manager.transactions):
                    print(f"Index [{index}] -> {tx.get_details()}")
                    
        elif choice == "4":
            summary = manager.get_summary()
            print("\n--- Financial Metrics Matrix ---")
            print(f"Gross Registered Inflow  : +${summary['total_income']:.2f}")
            print(f"Gross Registered Outflow : -${summary['total_expense']:.2f}")
            print("-" * 35)
            print(f"Net Liquid Asset Spread  : ${summary['net_balance']:.2f}")
            
        elif choice == "5":
            print("\nSerializing structural memory registers down to JSON payload storage...")
            StorageEngine.save_data(manager, DATA_FILE)
            print("State persistence complete. Safely terminating runtime environments. Goodbye!")
            sys.exit(0)

        elif choice == "6":
            # 1. Ask the user which category they want to set a limit for
            category = get_non_empty_string("Enter the category name (e.g., Food, Clothing): ")
            
            # 2. Ask for the maximum budget amount using our validated float function
            amount = get_validated_float(f"Enter the maximum budget ceiling for '{category}' ($): ")
            
            # 3. Pass those variables into your BudgetManager method
            manager.set_ceilings(category, amount)

        elif choice == "7":
            category_target = get_non_empty_string("Enter target category name to search: ")
            
            # Call our brand-new filter method
            filtered_results = manager.filter_by_category(category_target)
            
            print(f"\n--- Filtered Logs for Category: '{category_target}' ---")
            if not filtered_results:
                print(f"No transactions found matching '{category_target}'.")
            else:
                for tx in filtered_results:
                    print(tx.get_details())

        elif choice == "8":
            report_path = "data/financial_statement.txt"
            print(f"\nCompiling statement registers and generating text report...")
            
            # Call our brand-new export method
            StorageEngine.export_text_report(manager, report_path)
            
            print(f"Success! Statement exported cleanly to: '{report_path}'")

        elif choice == "9":
            print("\n--- Ledger Deletion Controls ---")
            if not manager.transactions:
                print("The ledger stream is currently empty. Nothing to delete.")
                continue
            
            print("1. Delete a specific entry by Index")
            print("2. WIPE ALL LEDGER DATA (Global Reset)")
            sub_choice = input("Select deletion type (1-2): ").strip()
            
            if sub_choice == "1":
                try:
                    # Ask the user for the index number
                    target_idx = int(input("Enter the exact Index number to delete: ").strip())
                    
                    # Execute single deletion sequence
                    removed_tx = manager.delete_transaction(target_idx)
                    print(f"Successfully purged entry: {removed_tx.get_details()}")
                    StorageEngine.save_data(manager, DATA_FILE)

                except ValueError:
                    print("Invalid format. Please input numerical integer digits only.")
                except IndexError:
                    print("Error: That index position does not exist in memory. Out of bounds.")
            
            elif sub_choice == "2":
                print("\n⚠️ ⚠️ ⚠️  WARNING: This will permanently delete all records in this session!")
                confirm = input("Are you absolutely sure? Type 'Y' to confirm: ").strip().upper()
                
                if confirm == "Y":
                    manager.purge_all_transactions()
                    print("Database reset successful. The ledger is now completely empty.")
                    StorageEngine.save_data(manager, DATA_FILE)
                else:
                    print("Global purge operation cancelled safely.")
            
            else:
                print("Invalid selection. Returning to Main Controls.")
            
        else:
            print("Action invalid. Please match selection arguments to the explicit indexes provided (1-9).")

if __name__ == "__main__":
    main()
import json
import os
from src.models import Income, Expense, BudgetManager
from datetime import datetime

class StorageEngine:
    @staticmethod
    def save_data(manager: BudgetManager, filepath: str):
        """Serializes Transaction objects to JSON file format."""
        # Ensure data directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        serialized_list = [t.to_dict() for t in manager.transactions]
        
        with open(filepath, "w") as file:
            json.dump(serialized_list, file, indent=4)

    @staticmethod
    def load_data(manager: BudgetManager, filepath: str):
        """Deserializes raw JSON back into explicit OOP Python instances."""
        if not os.path.exists(filepath):
            return  # Fail gracefully if file does not exist yet
        
        try:
            with open(filepath, "r") as file:
                raw_data = json.load(file)
                
                for item in raw_data:
                    if item["type"] == "Income":
                        tx = Income(item["amount"], item["category"], item["date"])
                    elif item["type"] == "Expense":
                        tx = Expense(item["amount"], item["category"], item["date"])
                    manager.add_transaction(tx)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"\n[Warning] Data file corrupted or structure modified. Error: {e}")
            print("Starting application execution with an empty manager state.")
    
    @staticmethod
    def export_text_report(manager: BudgetManager, filepath: str):
        """Generates a human-readable clear text financial statement report."""
        summary = manager.get_summary()
        
        # Open a fresh text file using a context manager
        with open(filepath, "w") as file:
            file.write("=" * 45 + "\n")
            file.write("        PERSONAL FINANCIAL STATEMENT REPORT\n")
            file.write(f"        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            file.write("=" * 45 + "\n\n")
            
            file.write("--- SUMMARY METRICS ---\n")
            file.write(f"Total Gross Income  : +${summary['total_income']:.2f}\n")
            file.write(f"Total Gross Expenses: -${summary['total_expense']:.2f}\n")
            file.write("-" * 30 + "\n")
            file.write(f"Net Asset Balance   : ${summary['net_balance']:.2f}\n\n")
            
            file.write("--- CHRONOLOGICAL LEDGER LOGS ---\n")
            if not manager.transactions:
                file.write("No transaction entries logged in this ledger session.\n")
            else:
                for tx in manager.transactions:
                    file.write(f"{tx.get_details()}\n")
            
            file.write("\n" + "=" * 45 + "\n")
            file.write("            End of Financial Transmission\n")
            file.write("=" * 45 + "\n")
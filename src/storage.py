import json
import os
from src.models import Income, Expense, BudgetManager

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
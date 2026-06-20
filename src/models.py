from abc import ABC, abstractmethod
from datetime import datetime

class Transaction(ABC):
    """Abstract Base Class for all financial transactions."""
    def __init__(self, amount: float, category: str, date: str = None):
        self._amount = float(amount)  # Encapsulation: Protected attribute
        self.category = category
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M")

    @property
    def amount(self) -> float:
        return self._amount

    @abstractmethod
    def get_details(self) -> str:
        """Polymorphic method to display transaction strings."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Converts object details to a dictionary serialization format."""
        pass


class Income(Transaction):
    """Subclass representing incoming revenue."""
    def get_details(self) -> str:
        return f"[INCOME] {self.date} | Category: {self.category} | Amount: +${self.amount:.2f}"

    def to_dict(self) -> dict:
        return {
            "type": "Income",
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }


class Expense(Transaction):
    """Subclass representing outgoing costs."""
    def get_details(self) -> str:
        return f"[EXPENSE] {self.date} | Category: {self.category} | Amount: -${self.amount:.2f}"

    def to_dict(self) -> dict:
        return {
            "type": "Expense",
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }


class BudgetManager:
    """Manages memory collections of transactions and executes business logic."""
    def __init__(self):
        self.transactions = []
        self.category_ceilings = {}

    def set_ceilings(self,category: str, amount: float):
        self.category_ceilings[category.lower()] = float(amount)
        print(f"Ceiling updated: {category} limit is now ${amount:.2f}")

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        if isinstance(transaction, Expense):
            current_category = transaction.category.lower()
            if current_category in self.category_ceilings:
                limit = self.category_ceilings[current_category]
                
                # Calculate total expenses for this category
                total_spent = 0.0
                for t in self.transactions:
                    if isinstance(t, Expense) and t.category.lower() == current_category:
                        total_spent += t.amount
                
                # If total spent breaks the limit, trigger the warning!
                if total_spent > limit:
                    print(f"\n⚠️  [BUDGET WARNING] You have exceeded the ceiling for '{transaction.category}'!")
                    print(f"Total Spent: ${total_spent:.2f} | Ceiling Limit: ${limit:.2f}\n")

    def get_total_balance(self) -> float:
        balance = 0.0
        for t in self.transactions:
            if isinstance(t, Income):
                balance += t.amount
            elif isinstance(t, Expense):
                balance -= t.amount
        return balance

    def get_summary(self) -> dict:
        summary = {"total_income": 0.0, "total_expense": 0.0, "net_balance": 0.0}
        for t in self.transactions:
            if isinstance(t, Income):
                summary["total_income"] += t.amount
            elif isinstance(t, Expense):
                summary["total_expense"] += t.amount
        summary["net_balance"] = summary["total_income"] - summary["total_expense"]
        return summary
    
    def filter_by_category(self, category_name: str) -> list:
        """Returns a list of transaction objects matching the target category."""
        # Loop through self.transactions and pick out items where the categories match
        return [t for t in self.transactions if t.category.lower() == category_name.lower()]
    
    def delete_transaction(self, index: int) -> Transaction:
        """Removes and returns a transaction at a given list index position."""
        # .pop() removes an item from a specific index and returns it
        return self.transactions.pop(index)
    
    def purge_all_transactions(self):
        """Completely empties the transaction ledger memory."""
        self.transactions.clear()
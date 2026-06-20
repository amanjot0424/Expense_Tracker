# Personal Finance Tracker Engine

A modular, production-grade Command-Line Interface (CLI) application built to track personal revenues and expenditures. This project serves as a practical showcase of core **Python Development Foundations**, emphasizing Object-Oriented Programming (OOP), file resilience, and modular design.

## 🚀 Core Features
- **Robust OOP Architecture**: Built using Abstract Base Classes (ABC), inheritance, encapsulation, and runtime polymorphism.
- **State Persistence**: Uses an explicit JSON storage layer with context-managed file handling (`with open()`) to save and reload financial data across sessions.
- **Input Validation Safeguards**: Protected against runtime crashes from user input errors using `try/except` exception handling blocks.
- **Financial Analytics**: Computes real-time metrics including gross inflows, gross outflows, and net liquid balances.

## 📂 Project Architecture
```text
personal_finance_tracker/
│
├── data/
│   └── tracker_data.json      # JSON data persistence layer
│
├── src/                       # Application source modules
│   ├── __init__.py            # Package initializer
│   ├── models.py              # OOP Blueprint: Transactions & BudgetManager
│   ├── storage.py             # File Handling: JSON Engine
│   └── utils.py               # Input Validation & Helper utilities
│
├── main.py                    # Application runtime entry point
├── .gitignore                 # Version control exclusions
└── README.md                  # Project documentation
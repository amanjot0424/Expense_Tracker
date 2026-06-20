def get_validated_float(prompt_message: str) -> float:
    """Loops execution until user provides an authentic float representation."""
    while True:
        try:
            user_input = input(prompt_message).strip()
            value = float(user_input)
            if value <= 0:
                print("Value must be a positive number. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input sequence. Please input numerical digits only (e.g., 45.50).")

def get_non_empty_string(prompt_message: str) -> str:
    """Ensures input options don't default into empty configurations."""
    while True:
        user_input = input(prompt_message).strip()
        if not user_input:
            print("Input field cannot be blank.")
            continue
        return user_input
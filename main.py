import random  # Import the random module to randomly select slot symbols during spins

# --------------------------- CONSTANTS ---------------------------

MAX_LINES = 3   # Maximum number of lines a player can bet on
MAX_BET = 100   # Maximum amount that can be bet per line
MIN_BET = 1     # Minimum amount that can be bet per line

ROWS = 3        # Number of rows on the slot machine
COLS = 3        # Number of columns on the slot machine

# Dictionary representing how many times each symbol appears in the slot machine pool
symbol_count = {
    "A": 2,     # 'A' appears 2 times
    "B": 4,     # 'B' appears 4 times
    "C": 6,     # 'C' appears 6 times
    "D": 8      # 'D' appears 8 times
}

# Dictionary representing the payout multiplier for each symbol when a line wins
symbol_value = {
    "A": 5,     # 'A' pays 5x the bet if the line wins
    "B": 4,     # 'B' pays 4x the bet if the line wins
    "C": 3,     # 'C' pays 3x the bet if the line wins
    "D": 2      # 'D' pays 2x the bet if the line wins
}

# --------------------------- FUNCTIONS ---------------------------

def check_winnings(columns, lines, bet, values):
    """
    This function checks which lines have won based on the slot result.
    - columns: list of columns (each is a list of symbols)
    - lines: number of lines the player bet on
    - bet: amount bet per line
    - values: payout multiplier for each symbol
    """
    winnings = 0
    winning_lines = []

    # Iterate through each line the player bet on
    for line in range(lines):
        symbol = columns[0][line]  # Take the symbol from the first column for this line
        for column in columns:
            symbol_to_check = column[line]  # Get the symbol in the same row (line) but different column
            if symbol != symbol_to_check:   # If any symbol differs, the line is not a win
                break
        else:
            # If loop completes without breaking, all symbols matched => line wins
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)  # Add line number (1-based index)

    # Return total winnings and the list of lines that won
    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    """
    Simulates a spin of the slot machine.
    - Creates 'cols' number of columns with 'rows' number of symbols in each.
    - Randomly selects symbols based on their frequency in 'symbols'.
    """
    all_symbols = []  # Pool of all available symbols based on their frequency
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []  # Will hold each column of symbols

    # Generate each column of the slot machine
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]  # Make a copy of all symbols for this column

        # Randomly choose 'rows' symbols for this column (no repetition within column)
        for _ in range(rows):
            value = random.choice(current_symbols)  # Randomly select a symbol
            current_symbols.remove(value)           # Remove it to avoid duplication in the same column
            column.append(value)                    # Add it to the current column

        columns.append(column)  # Add completed column to the slot machine layout

    return columns  # Returns a list of columns (each containing multiple symbols)


def print_slot_machine(columns):
    """
    Prints the slot machine's current spin result in a readable 3x3 grid format.
    Each row across columns is displayed horizontally.
    """
    for row in range(len(columns[0])):  # For each row
        for i, column in enumerate(columns):  # For each column in that row
            if i != len(columns) - 1:
                print(column[row], end=" | ")  # Print symbol followed by separator if not last column
            else:
                print(column[row], end="")     # Last column, no separator
        print()  # Move to the next line after printing one full row


def deposit():
    """
    Prompts the user to deposit an amount of money.
    Keeps asking until a valid positive number is entered.
    """
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():  # Check if input is a valid integer
            amount = int(amount)
            if amount > 0:
                break  # Valid deposit amount
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")

    return amount  # Return deposited amount


def get_number_of_lines():
    """
    Asks the user for how many lines they want to bet on (1 to MAX_LINES).
    Ensures valid input.
    """
    while True:
        lines = input(
            "Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break  # Valid number of lines
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")

    return lines  # Return number of lines chosen by player


def get_bet():
    """
    Asks the user for how much they want to bet on each line.
    Ensures it's within MIN_BET and MAX_BET range.
    """
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break  # Valid bet
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a number.")

    return amount  # Return bet amount per line


def spin(balance):
    """
    Handles a single round (spin) of the slot machine.
    - Gets number of lines and bet per line from the user.
    - Checks if user has enough balance.
    - Spins the slot machine and calculates winnings/losses.
    """
    lines = get_number_of_lines()

    # Keep asking for bet until total bet <= available balance
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(
                f"You do not have enough to bet that amount, your current balance is: ${balance}")
        else:
            break  # Valid bet amount

    # Show the player their total bet
    print(
        f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    # Perform the slot machine spin
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)  # Display the slot machine

    # Check if player won anything
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines)

    # Return the profit/loss amount to adjust player balance
    return winnings - total_bet


def main():
    """
    Main game loop.
    - Prompts the user to deposit money.
    - Repeats rounds until player quits.
    - Updates and displays balance after each spin.
    """
    balance = deposit()  # Get initial deposit

    # Main game loop
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break  # Exit game if user types 'q'

        # Play one spin and update balance based on winnings/losses
        balance += spin(balance)

    # Display final balance after quitting
    print(f"You left with ${balance}")


# Start the slot machine game
main()

# Function to calculate tax under the Old Regime
def calculate_old_regime_tax(income):
    """
    Calculates tax based on a simplified Old Regime structure.
    Assumes a standard deduction of Rs. 50,000.
    """
    taxable_income = max(0, income - 50000) # Apply standard deduction

    tax = 0
    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = (250000 * 0.05) + (taxable_income - 500000) * 0.20
    else:
        tax = (250000 * 0.05) + (500000 * 0.20) + (taxable_income - 1000000) * 0.30
    return tax

# Function to calculate tax under the New Regime
def calculate_new_regime_tax(income):
    """
    Calculates tax based on a simplified New Regime structure.
    No standard deductions are applied in this regime.
    """
    tax = 0
    if income <= 300000:
        tax = 0
    elif income <= 600000:
        tax = (income - 300000) * 0.05
    elif income <= 900000:
        tax = (300000 * 0.05) + (income - 600000) * 0.10
    elif income <= 1200000:
        tax = (300000 * 0.05) + (300000 * 0.10) + (income - 900000) * 0.15
    elif income <= 1500000:
        tax = (300000 * 0.05) + (300000 * 0.10) + (300000 * 0.15) + (income - 1200000) * 0.20
    else:
        tax = (300000 * 0.05) + (300000 * 0.10) + (300000 * 0.15) + (300000 * 0.20) + (income - 1500000) * 0.30
    return tax

def main():
    """
    Main function to run the console-based tax calculator.
    Takes CTC and Bonus as input, calculates tax under both regimes,
    and displays the results.
    """
    print("TAX CALCULATOR")

    try:
        # Get user input for CTC and Bonus
        ctc = float(input(" ENTER YOUR CTC:"))
        bonus = float(input(" ENTER YOUR BONUS:"))
    except ValueError:
        print("Invalid input. Please enter numeric values for CTC and Bonus.")
        return

    # Calculate total income
    total_income = ctc + bonus

    print(f"\n TOTAL INCOME:RS.{int(total_income)}")

    # Calculate tax for Old Regime
    old_regime_tax = calculate_old_regime_tax(total_income)
    print(f"\n OLD REGIME TAX DEDUCTION:RS.{int(old_regime_tax)}")

    # Calculate tax for New Regime
    new_regime_tax = calculate_new_regime_tax(total_income)
    print(f" NEW REGIME TAX DEDUCTION:RS.{int(new_regime_tax)}")

    # Compare and show savings
    if old_regime_tax < new_regime_tax:
        savings = new_regime_tax - old_regime_tax
        print(f"\n YOU SAVE RS.{int(savings)} MORE USING THE OLD REGIME")
    elif new_regime_tax < old_regime_tax:
        savings = old_regime_tax - new_regime_tax
        print(f"\n YOU SAVE RS.{int(savings)} MORE USING THE NEW REGIME")
    else:
        print("\n Tax deduction is the same for both regimes.")

if __name__ == "__main__":
    main()

def greeting():
    print("Hello World")


def calculate_pi_to_5th_digit():
    """
    Calculate pi to the 5th decimal digit using the Machin formula.
    Returns pi rounded to 5 decimal places (3.14159).
    
    Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    """
    def arctan(x, num_terms=100):
        """Calculate arctan using Taylor series expansion"""
        result = 0
        for n in range(num_terms):
            term = ((-1) ** n) * (x ** (2 * n + 1)) / (2 * n + 1)
            result += term
        return result
    
    # Machin's formula for better convergence
    pi = 4 * (4 * arctan(1/5, 100) - arctan(1/239, 100))
    
    # Round to 5 decimal places
    return round(pi, 5)

# buggy_calculator.py
# A simple calculator with intentional style issues for lab use

def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b

def divide(a: float, b: float) -> float:
    """Return the quotient of a and b."""
    if b == 0:
        raise ValueError("division by zero")
    return a / b

def calculate(op: str, x: float, y: float) -> float:
    """Perform a calculation based on the specified operator."""
    if op == "add":
        return add(x, y)
    elif op == "subtract":
        return subtract(x, y)
    elif op == "multiply":
        return multiply(x, y)
    elif op == "divide":
        return divide(x, y)

def main() -> None:
    """Demonstrate each calculator operation."""
    print("add(3, 5)       =", calculate("add", 3, 5))
    print("subtract(10, 4) =", calculate("subtract", 10, 4))
    print("multiply(6, 7)  =", calculate("multiply", 6, 7))
    print("divide(20, 4)   =", calculate("divide", 20, 4))
    try:
        calculate("divide", 10, 0)
    except ValueError as e:
        print("divide(10, 0)   = error:", e)

if __name__ == "__main__":
    main()

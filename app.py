import streamlit as st

st.set_page_config(page_title="Simple Calculator", layout="centered")

st.title("🧮 Simple Calculator")

# Input fields
num1 = st.number_input("Enter first number", format="%.2f", step=1.0)
num2 = st.number_input("Enter second number", format="%.2f", step=1.0)

operation = st.selectbox("Choose operation", ["Add", "Subtract", "Multiply", "Divide"])

# Calculate result
def calculate(n1, n2, op):
    if op == "Add":
        return n1 + n2
    elif op == "Subtract":
        return n1 - n2
    elif op == "Multiply":
        return n1 * n2
    elif op == "Divide":
        if n2 == 0:
            return "Error: Division by zero"
        return n1 / n2

if st.button("Calculate"):
    result = calculate(num1, num2, operation)
    st.success(f"Result: {result}")

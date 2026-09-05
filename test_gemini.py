from src.gemini import ask_gemini


context = """
Total sales: ₹250000

Top selling products:
1. Smartphone - 450 units
2. Laptop - 390 units
3. T-Shirt - 350 units

Low stock:
- Headphones at Store 1: 3 units
- Laptop at Store 2: 5 units
"""


question = "Which products need immediate attention?"

answer = ask_gemini(
    question,
    context
)

print("\n========== GEMINI RESPONSE ==========\n")
print(answer)
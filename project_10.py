import os
from library import functions
from library.classes import Budget

os.system('cls' if os.name == 'nt' else 'clear')
name_of_user = input("Enter your name: ")
os.system('cls' if os.name == 'nt' else 'clear')


print(f"Hey {name_of_user}, this is BudgetBuddy! Your personal Budgeting Assistant.")
monthly_income = functions.get_valid_float("Enter your monthly income: ")
print("Your income is:", monthly_income)
total_expenses = []
grocery = Budget("Grocery")
car = Budget("Car")
 
grocery.add_expenses()
car.add_expenses()

grocery.write_to_file()
car.write_to_file()

total_expenses.append(grocery.get_expenses())
total_expenses.append(car.get_expenses())

balance = functions.calc_balance(monthly_income, sum(total_expenses))
functions.financial_status(balance)

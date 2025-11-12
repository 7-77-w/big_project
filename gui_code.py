import tkinter as tk
from library import functions   


root = tk.Tk()
root.title("BudgetBuddy")
root.geometry("400x400")

label_prompt = tk.Label(root, text="Enter your name:")
entry_name = tk.Entry(root)
button_submit = tk.Button(root, text="Submit")
label_output = tk.Label(root, text="")


label_income_prompt = tk.Label(root, text="Enter your monthly income:")
entry_income = tk.Entry(root)
button_income = tk.Button(root, text="Check Budget")
label_status = tk.Label(root, text="")


label_prompt.pack(pady=10)
entry_name.pack(pady=5)
button_submit.pack(pady=5)
label_output.pack(pady=10)
label_status.pack(pady=10)


def greet_user():
    name = entry_name.get()
    if name.strip() == "":
        label_output.config(text="Please enter your name.")
        return
    label_output.config(text=f"Hey {name}, this is BudgetBuddy! Your personal budgeting assistant.")
  
    label_income_prompt.pack()
    entry_income.pack()
    button_income.pack()

def show_financial_status():
    try:
        income = float(entry_income.get())
    except ValueError:
        label_status.config(text="Please enter a valid number for income.")
        return


    expenses = 1200.00
    balance = functions.calc_balance(income, expenses)
    status = functions.financial_status(balance)
    label_status.config(text=f"After expenses, your balance is ${balance:.2f}.\nStatus: {status}")


button_submit.config(command=greet_user)
button_income.config(command=show_financial_status)

root.mainloop()
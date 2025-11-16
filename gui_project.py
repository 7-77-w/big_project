# gui_budget.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from library import functions
from library.classes_10 import Budget

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy - Personal Budgeting Assistant")
        self.root.geometry("800x600")
        
        # Initialize data storage
        self.name = ""
        self.monthly_income = 0.0
        self.budgets = {}
        self.current_category = None
        
        # Create the main interface
        self.create_welcome_screen()
    
    def clear_frame(self):
        """Clear all widgets from the root window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_welcome_screen(self):
        """Create the welcome screen with name and income input"""
        self.clear_frame()
        
        # Welcome label
        welcome_label = ttk.Label(self.root, text="Welcome, I am BudgetBuddy!", 
                                 font=("Arial", 16, "bold"))
        welcome_label.pack(pady=20)
        
        # Name input
        name_frame = ttk.Frame(self.root)
        name_frame.pack(pady=10, fill="x", padx=50)
        
        ttk.Label(name_frame, text="Enter your name:").pack(anchor="w")
        self.name_entry = ttk.Entry(name_frame, width=30, font=("Arial", 12))
        self.name_entry.pack(fill="x", pady=5)
        self.name_entry.focus()
        
        # Income input
        income_frame = ttk.Frame(self.root)
        income_frame.pack(pady=10, fill="x", padx=50)
        
        ttk.Label(income_frame, text="Enter your monthly income:").pack(anchor="w")
        self.income_entry = ttk.Entry(income_frame, width=30, font=("Arial", 12))
        self.income_entry.pack(fill="x", pady=5)
        
        # Start button
        start_button = ttk.Button(self.root, text="Start Budgeting", 
                                 command=self.start_budgeting)
        start_button.pack(pady=20)
        
        # Bind Enter key to start budgeting
        self.root.bind('<Return>', lambda event: self.start_budgeting())
    
    def start_budgeting(self):
        """Validate and store user info, then proceed to budget categories"""
        self.name = self.name_entry.get().strip()
        income_text = self.income_entry.get().strip()
        
        if not self.name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        
        try:
            self.monthly_income = float(income_text)
            if self.monthly_income <= 0:
                messagebox.showerror("Error", "Please enter a positive income value.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for income.")
            return
        
        self.create_category_selection()
    
    def create_category_selection(self):
        """Create screen to select budget categories"""
        self.clear_frame()
        
        # Header
        header_label = ttk.Label(self.root, 
                                text=f"Hello {self.name}! Let's manage your budget.",
                                font=("Arial", 14, "bold"))
        header_label.pack(pady=20)
        
        income_label = ttk.Label(self.root, 
                                text=f"Monthly Income: ${self.monthly_income:.2f}",
                                font=("Arial", 12))
        income_label.pack(pady=10)
        
        # Category selection
        category_frame = ttk.LabelFrame(self.root, text="Budget Categories", padding=20)
        category_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        ttk.Label(category_frame, 
                 text="Select a category to add expenses:").pack(anchor="w", pady=10)
        
        # Predefined categories - you can add more here
        categories = ["Grocery", "Car", "Housing", "Utilities", "Entertainment", "Transportation"]
        
        for category in categories:
            cat_button = ttk.Button(category_frame, text=category,
                                   command=lambda cat=category: self.add_expenses_for_category(cat))
            cat_button.pack(pady=5, fill="x")
        
        # View summary button
        summary_button = ttk.Button(self.root, text="View Budget Summary", 
                                   command=self.show_summary)
        summary_button.pack(pady=10)
    
    def add_expenses_for_category(self, category):
        """Create interface for adding expenses for a specific category"""
        self.current_category = category
        self.clear_frame()
        
        # Header
        header_label = ttk.Label(self.root, 
                                text=f"Adding expenses for: {category}",
                                font=("Arial", 14, "bold"))
        header_label.pack(pady=20)
        
        # Back button
        back_button = ttk.Button(self.root, text="← Back to Categories",
                                command=self.create_category_selection)
        back_button.pack(anchor="nw", padx=20, pady=10)
        
        # Expense input frame
        input_frame = ttk.LabelFrame(self.root, text="Add New Expense", padding=15)
        input_frame.pack(pady=10, padx=50, fill="x")
        
        # Expense type
        ttk.Label(input_frame, text="Expense Type:").grid(row=0, column=0, sticky="w", pady=5)
        self.expense_type_entry = ttk.Entry(input_frame, width=30)
        self.expense_type_entry.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
        
        # Expense amount
        ttk.Label(input_frame, text="Amount:").grid(row=1, column=0, sticky="w", pady=5)
        self.expense_amount_entry = ttk.Entry(input_frame, width=30)
        self.expense_amount_entry.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        
        # Add expense button
        add_button = ttk.Button(input_frame, text="Add Expense", 
                               command=self.add_expense)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)
        
        # Current expenses display
        self.create_expenses_display()
    
    def add_expense(self):
        """Add a new expense to the current category"""
        expense_type = self.expense_type_entry.get().strip()
        amount_text = self.expense_amount_entry.get().strip()
        
        if not expense_type:
            messagebox.showerror("Error", "Please enter an expense type.")
            return
        
        try:
            amount = float(amount_text)
            if amount <= 0:
                messagebox.showerror("Error", "Please enter a positive amount.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for amount.")
            return
        
        # Initialize budget category if not exists
        if self.current_category not in self.budgets:
            self.budgets[self.current_category] = Budget(self.current_category)
            self.budgets[self.current_category].expenses_dict = {}
        
        # Add expense to budget
        self.budgets[self.current_category].expenses_dict[expense_type] = amount
        
        # Clear entries
        self.expense_type_entry.delete(0, tk.END)
        self.expense_amount_entry.delete(0, tk.END)
        
        # Refresh expenses display
        self.create_expenses_display()
        
        messagebox.showinfo("Success", f"Added {expense_type}: ${amount:.2f} to {self.current_category}")
    
    def create_expenses_display(self):
        """Display current expenses for the category"""
        # Remove existing display if any
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and "Current Expenses" in widget.cget("text"):
                widget.destroy()
        
        if self.current_category in self.budgets and self.budgets[self.current_category].expenses_dict:
            expenses_frame = ttk.LabelFrame(self.root, text="Current Expenses", padding=15)
            expenses_frame.pack(pady=10, padx=50, fill="both", expand=True)
            
            # Create treeview for expenses
            columns = ("Type", "Amount")
            tree = ttk.Treeview(expenses_frame, columns=columns, show="headings", height=8)
            
            # Define headings
            tree.heading("Type", text="Expense Type")
            tree.heading("Amount", text="Amount ($)")
            
            # Define columns
            tree.column("Type", width=200)
            tree.column("Amount", width=100)
            
            # Add expenses to treeview
            total = 0
            for expense_type, amount in self.budgets[self.current_category].expenses_dict.items():
                tree.insert("", "end", values=(expense_type, f"{amount:.2f}"))
                total += amount
            
            tree.pack(fill="both", expand=True)
            
            # Total label
            total_label = ttk.Label(expenses_frame, 
                                   text=f"Total for {self.current_category}: ${total:.2f}",
                                   font=("Arial", 10, "bold"))
            total_label.pack(pady=10)
    def show_summary(self):
        """Display the budget summary with individual expenses"""
        self.clear_frame()
    
        # Header
        header_label = ttk.Label(self.root, 
                                text="Budget Summary",
                                font=("Arial", 16, "bold"))
        header_label.pack(pady=20)
        
        # Back button
        back_button = ttk.Button(self.root, text="← Back to Categories",
                                command=self.create_category_selection)
        back_button.pack(anchor="nw", padx=20, pady=10)
        
        if not self.budgets:
            no_data_label = ttk.Label(self.root, text="No budget data available. Please add some expenses first.",
                                    font=("Arial", 12))
            no_data_label.pack(pady=50)
            return
        
        # Create a scrollable frame for the summary
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Income display
        income_frame = ttk.LabelFrame(scrollable_frame, text="Income", padding=10)
        income_frame.pack(fill="x", pady=5)
        ttk.Label(income_frame, text=f"Monthly Income: ${self.monthly_income:.2f}",
                font=("Arial", 12, "bold")).pack()
        
        # Detailed expenses by category
        total_expenses = 0
        
        for category, budget in self.budgets.items():
            if budget.expenses_dict:  # Only show categories with expenses
                category_frame = ttk.LabelFrame(scrollable_frame, text=f"{category} Expenses", padding=10)
                category_frame.pack(fill="x", pady=10)
                
                # Create treeview for individual expenses in this category
                columns = ("Expense Type", "Amount")
                tree = ttk.Treeview(category_frame, columns=columns, show="headings", height=6)
                
                # Define headings
                tree.heading("Expense Type", text="Expense Type")
                tree.heading("Amount", text="Amount ($)")
                
                # Define columns
                tree.column("Expense Type", width=250)
                tree.column("Amount", width=100)
                
                # Add individual expenses to treeview
                category_total = 0
                for expense_type, amount in budget.expenses_dict.items():
                    tree.insert("", "end", values=(expense_type, f"{amount:.2f}"))
                    category_total += amount
                
                tree.pack(fill="x", pady=5)
                
                # Category total
                total_label = ttk.Label(category_frame, 
                                    text=f"Total for {category}: ${category_total:.2f}",
                                    font=("Arial", 10, "bold"))
                total_label.pack(pady=5)
                
                total_expenses += category_total
        
        # Calculate and display overall summary
        summary_frame = ttk.LabelFrame(scrollable_frame, text="Financial Summary", padding=15)
        summary_frame.pack(fill="x", pady=20)
        
        balance = functions.calc_balance(self.monthly_income, total_expenses)
        
        ttk.Label(summary_frame, text=f"Total Expenses: ${total_expenses:.2f}",
                font=("Arial", 11)).pack(anchor="w", pady=2)
        ttk.Label(summary_frame, text=f"Balance: ${balance:.2f}",
                font=("Arial", 11)).pack(anchor="w", pady=2)
        
        # Financial status
        #if balance > 0:
            #status_message = "Great! You are saving money!"
            #status_color = "green"
        #elif balance == 0:
            #status_message = "You are breaking even."
            #status_color = "orange"
        #else:
            #status_message = "**Warning** You are overspending!"
            #status_color = "red"

        status_label = ttk.Label(summary_frame, text=status_message, 
                                foreground=status_color, font=("Arial", 12, "bold"))
        status_label.pack(anchor="w", pady=10)
        
        # Save to file button
        save_button = ttk.Button(scrollable_frame, text="Save Budget to File", 
                                command=self.save_to_file)
        save_button.pack(pady=10)
    def save_to_file(self):
        """Save all budget data to file"""
        try:
            # Clear the file first
            open("database.txt", "w").close()
            
            # Write each budget category to file
            for budget in self.budgets.values():
                budget.write_to_file()
            
            messagebox.showinfo("Success", "Budget data saved to database.txt")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")    
            

def main():
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
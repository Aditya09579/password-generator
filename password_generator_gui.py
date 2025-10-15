import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
import re

class PasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator - Internship Task")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=12)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_var = tk.StringVar()
        self.security_rules_var = tk.BooleanVar(value=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🔐 Advanced Password Generator", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Password display section
        display_frame = ttk.LabelFrame(main_frame, text="Generated Password", padding="15")
        display_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Password entry with copy button
        password_entry = ttk.Entry(display_frame, textvariable=self.password_var, 
                                  font=("Courier New", 12), width=50, state='readonly')
        password_entry.grid(row=0, column=0, padx=(0, 10))
        
        copy_btn = ttk.Button(display_frame, text="Copy to Clipboard", 
                             command=self.copy_to_clipboard)
        copy_btn.grid(row=0, column=1)
        
        # Length control
        length_frame = ttk.LabelFrame(main_frame, text="Password Length", padding="15")
        length_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        length_scale = ttk.Scale(length_frame, from_=4, to=50, variable=self.length_var, 
                                orient=tk.HORIZONTAL, command=self.update_length_label)
        length_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.length_label = ttk.Label(length_frame, text="12", font=("Arial", 10, "bold"))
        self.length_label.grid(row=0, column=1, padx=(10, 0))
        
        # Character options
        chars_frame = ttk.LabelFrame(main_frame, text="Character Types", padding="15")
        chars_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Checkbutton(chars_frame, text="Uppercase Letters (A-Z)", 
                       variable=self.uppercase_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(chars_frame, text="Lowercase Letters (a-z)", 
                       variable=self.lowercase_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(chars_frame, text="Numbers (0-9)", 
                       variable=self.numbers_var).grid(row=0, column=1, sticky=tk.W)
        ttk.Checkbutton(chars_frame, text="Symbols (!@#$%^&*)", 
                       variable=self.symbols_var).grid(row=1, column=1, sticky=tk.W)
        
        # Security rules
        security_frame = ttk.LabelFrame(main_frame, text="Security Rules", padding="15")
        security_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Checkbutton(security_frame, text="Enforce strong password rules", 
                       variable=self.security_rules_var).grid(row=0, column=0, sticky=tk.W)
        
        rules_text = tk.Text(security_frame, height=4, width=50, font=("Arial", 9))
        rules_text.grid(row=1, column=0, pady=(10, 0))
        rules_text.insert(tk.END, "• At least 8 characters\n• Mix of uppercase and lowercase\n• Include numbers\n• Include symbols\n• No repeated characters")
        rules_text.config(state=tk.DISABLED)
        
        # Customization
        custom_frame = ttk.LabelFrame(main_frame, text="Customization", padding="15")
        custom_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(custom_frame, text="Exclude specific characters:").grid(row=0, column=0, sticky=tk.W)
        exclude_entry = ttk.Entry(custom_frame, textvariable=self.exclude_var, width=30)
        exclude_entry.grid(row=0, column=1, padx=(10, 0))
        
        # Generate button
        generate_btn = ttk.Button(main_frame, text="Generate Secure Password", 
                                 command=self.generate_password, style="Accent.TButton")
        generate_btn.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Password strength
        strength_frame = ttk.LabelFrame(main_frame, text="Password Strength", padding="15")
        strength_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.strength_label = ttk.Label(strength_frame, text="Not generated", font=("Arial", 10))
        self.strength_label.grid(row=0, column=0, sticky=tk.W)
        
        self.strength_bar = ttk.Progressbar(strength_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.strength_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        length_frame.columnconfigure(0, weight=1)
        chars_frame.columnconfigure(0, weight=1)
        chars_frame.columnconfigure(1, weight=1)
        security_frame.columnconfigure(0, weight=1)
        custom_frame.columnconfigure(1, weight=1)
        strength_frame.columnconfigure(0, weight=1)
        
        # Generate initial password
        self.generate_password()
    
    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))
    
    def generate_password(self):
        try:
            length = self.length_var.get()
            use_upper = self.uppercase_var.get()
            use_lower = self.lowercase_var.get()
            use_numbers = self.numbers_var.get()
            use_symbols = self.symbols_var.get()
            exclude_chars = self.exclude_var.get()
            enforce_rules = self.security_rules_var.get()
            
            # Validate at least one character type is selected
            if not any([use_upper, use_lower, use_numbers, use_symbols]):
                messagebox.showerror("Error", "Please select at least one character type!")
                return
            
            # Character sets
            upper_chars = string.ascii_uppercase
            lower_chars = string.ascii_lowercase
            number_chars = string.digits
            symbol_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
            
            # Remove excluded characters
            if exclude_chars:
                upper_chars = ''.join(c for c in upper_chars if c not in exclude_chars)
                lower_chars = ''.join(c for c in lower_chars if c not in exclude_chars)
                number_chars = ''.join(c for c in number_chars if c not in exclude_chars)
                symbol_chars = ''.join(c for c in symbol_chars if c not in exclude_chars)
            
            # Build character pool
            char_pool = ''
            if use_upper: char_pool += upper_chars
            if use_lower: char_pool += lower_chars
            if use_numbers: char_pool += number_chars
            if use_symbols: char_pool += symbol_chars
            
            if not char_pool:
                messagebox.showerror("Error", "No characters available after exclusions!")
                return
            
            # Generate password
            if enforce_rules:
                password = self.generate_secure_password(length, upper_chars, lower_chars, number_chars, symbol_chars, use_upper, use_lower, use_numbers, use_symbols)
            else:
                password = ''.join(random.choice(char_pool) for _ in range(length))
            
            self.password_var.set(password)
            self.analyze_password_strength(password)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def generate_secure_password(self, length, upper_chars, lower_chars, number_chars, symbol_chars, use_upper, use_lower, use_numbers, use_symbols):
        """Generate password that adheres to security rules"""
        password = []
        
        # Ensure at least one character from each selected type
        if use_upper and upper_chars:
            password.append(random.choice(upper_chars))
        if use_lower and lower_chars:
            password.append(random.choice(lower_chars))
        if use_numbers and number_chars:
            password.append(random.choice(number_chars))
        if use_symbols and symbol_chars:
            password.append(random.choice(symbol_chars))
        
        # Fill remaining length with random characters from all pools
        char_pool = ''
        if use_upper: char_pool += upper_chars
        if use_lower: char_pool += lower_chars
        if use_numbers: char_pool += number_chars
        if use_symbols: char_pool += symbol_chars
        
        while len(password) < length:
            password.append(random.choice(char_pool))
        
        # Shuffle the password
        random.shuffle(password)
        
        # Convert to string and check if we need to truncate
        password = ''.join(password)
        
        # Ensure no repeated characters consecutively
        for i in range(1, len(password)):
            if password[i] == password[i-1]:
                # Replace with different character
                new_char = random.choice([c for c in char_pool if c != password[i]])
                password = password[:i] + new_char + password[i+1:]
        
        return password[:length]
    
    def analyze_password_strength(self, password):
        """Analyze password strength and update UI"""
        score = 0
        max_score = 8
        
        # Length scoring
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if len(password) >= 16: score += 1
        
        # Character variety
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(not c.isalnum() for c in password): score += 1
        
        # No consecutive repeats
        has_repeats = any(password[i] == password[i+1] for i in range(len(password)-1))
        if not has_repeats: score += 1
        
        # Calculate percentage and strength text
        strength_percent = (score / max_score) * 100
        
        if strength_percent < 40:
            strength_text = "Weak"
            color = "red"
        elif strength_percent < 70:
            strength_text = "Fair"
            color = "orange"
        elif strength_percent < 90:
            strength_text = "Good"
            color = "blue"
        else:
            strength_text = "Strong"
            color = "green"
        
        self.strength_label.config(text=f"{strength_text} ({score}/{max_score} criteria met)", foreground=color)
        self.strength_bar['value'] = strength_percent
        
        # Update progress bar color based on strength
        if strength_percent < 40:
            self.strength_bar.configure(style="Red.Horizontal.TProgressbar")
        elif strength_percent < 70:
            self.strength_bar.configure(style="Orange.Horizontal.TProgressbar")
        elif strength_percent < 90:
            self.strength_bar.configure(style="Blue.Horizontal.TProgressbar")
        else:
            self.strength_bar.configure(style="Green.Horizontal.TProgressbar")
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Success", "Password copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not copy to clipboard: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

def main():
    root = tk.Tk()
    
    # Configure styles
    style = ttk.Style()
    style.configure("Accent.TButton", font=("Arial", 12, "bold"))
    
    # Create progress bar styles for different colors
    style.configure("Red.Horizontal.TProgressbar", troughcolor='white', background='red')
    style.configure("Orange.Horizontal.TProgressbar", troughcolor='white', background='orange')
    style.configure("Blue.Horizontal.TProgressbar", troughcolor='white', background='blue')
    style.configure("Green.Horizontal.TProgressbar", troughcolor='white', background='green')
    
    app = PasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
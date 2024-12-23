import tkinter as tk

class FunctionInput:
    def __init__(self, master, callback):
        self.master = master
        master.title("Function Input")
        master.geometry("312x100")

        self.function_text = tk.StringVar()
        self.function_text.set("∫")

        self.entry = tk.Entry(master, textvariable=self.function_text, font=("Helvetica", 14))
        self.entry.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        self.upper_limit_entry = tk.Entry(master, font=("Helvetica", 12))
        self.upper_limit_entry.grid(row=0, column=1, padx=(10,0), pady=5, sticky="ew")
        
        self.lower_limit_entry = tk.Entry(master, font=("Helvetica", 12))
        self.lower_limit_entry.grid(row=1, column=1, padx=(10,0), pady=5, sticky="ew")

        self.submit_button = tk.Button(master, text="Submit", command=self.submit_function)
        self.submit_button.grid(row=1, column=2, pady=5)

        self.callback = callback

    def submit_function(self):
        function = self.function_text.get()
        upper_limit = self.upper_limit_entry.get()
        lower_limit = self.lower_limit_entry.get()
        function_with_limits = f"{upper_limit} {lower_limit} {function}"
        self.callback(function_with_limits)
        self.master.destroy()

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("900x424")

        self.total = tk.StringVar()
        self.total.set("∫")

        self.function = ""

        self.entry = tk.Entry(master, textvariable=self.total, font=("Helvetica", 40))
        self.entry.grid(row=0, column=0, columnspan=5, pady=20, padx=10, sticky="ew")

        self.create_buttons()


    def create_buttons(self):
        button_list = [
            ['sin', 'cos', 'tan', '^', '10^'],
            ['cot', '7', '8', '9', '/'],
            ['cosec', '4', '5', '6', '*'],
            ['sec', '1', '2', '3', '-'],
            ['cot', 'x', 'C', '+',''],
            ['√','','x','+','']
        ]

        for i, row in enumerate(button_list):
            for j, button_text in enumerate(row):
                button = tk.Button(
                    self.master, text=button_text, width=3, height=3, font=("Bold", 20),
                    command=lambda text=button_text: self.click(text)
                )
                button.grid(row=i + 1, column=j, padx=5, pady=5, sticky="nsew")
            self.master.rowconfigure(i + 1, weight=1)

        equal_button = tk.Button(self.master, text="=", width=3, height=3, font=("Helvetica", 20),
                                 command=lambda: self.click('='))
        equal_button.grid(row=5, column=4, padx=5, pady=5, sticky="nsew")

        # Adding Log and Erase Buttons
        log_button = tk.Button(self.master, text="log(x,base)", width=3, height=3, font=("Helvetica", 20),
                               command=lambda: self.click('log'))
        log_button.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        backspace_button = tk.Button(self.master, text="Bkspace", width=3, height=3, font=("Helvetica", 20),
                                     command=lambda: self.click('backspace'))
        backspace_button.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        curly_bracket_open_button = tk.Button(self.master, text="(", width=3, height=3, font=("Helvetica", 20),
                                              command=lambda: self.click('('))
        curly_bracket_open_button.grid(row=5, column=2, padx=5, pady=5, sticky="nsew")

        curly_bracket_close_button = tk.Button(self.master, text=")", width=3, height=3, font=("Helvetica", 20),
                                               command=lambda: self.click(')'))
        curly_bracket_close_button.grid(row=5, column=3, padx=5, pady=5, sticky="nsew")

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.columnconfigure(4, weight=1)

    def click(self, button_text):
        current_text = self.entry.get()
        if button_text == 'C':
            self.total.set("")
            self.function = ""
        elif button_text == '=':
            self.function = current_text
            print("Function:", self.function)
        elif button_text == 'backspace':
            self.function = self.function[:-1]
            self.total.set(current_text[:-1])
        elif button_text == 'log':
            self.function += 'log('
            self.total.set(current_text + 'log(')
        elif button_text == '^':
            self.function += '**('
            self.total.set(current_text + '^(')
        elif button_text in ['sin', 'cos', 'tan', 'cosec', 'sec', 'cot']:
            self.function += button_text + '('
            self.total.set(current_text + button_text + '(')
        elif button_text == ')':
            self.function += ')'
            self.total.set(current_text + ')')
        else:
            self.function += button_text
            self.total.set(current_text + button_text)
    

if __name__ == '__main__':
    root = tk.Tk()
    my_calculator = Calculator(root)
    root.mainloop()

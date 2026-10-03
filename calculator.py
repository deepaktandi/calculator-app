import tkinter as tk
import re
class Calculator:
    def __init__(self, display):
        #-----------------calculator state-------------------
        self.first_number = None
        self.operator = None
        self.last_result = None
        self.display = display
        self.history = []
        self.history_window = None
        self.history_list = None

    def button_click(self, value):
        current = self.display.get()

        if current != "" and current[-1] == ")":
            return

        self.display.insert(tk.END ,value)
        self.update_display_font()
        self.display.xview_moveto(1)

    def operator_click(self, op):
    
        try:
            current = self.display.get()

            if current == "" and self.last_result is not None:
                self.display.insert(0, str(self.last_result))
                self.display.get()
                

            if current == "":
                if op == "-":
                    self.display.insert(tk.END , "-")
                return

            if current[-1] in "+-*/^":
                if op == "-":
                    self.display.insert(tk.END , "-")
                return

            if current[-1]== "-":
                return

            self.display.insert(tk.END , op)
            self.update_display_font()
            self.display.xview_moveto(1)
           
        except:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")


       


    def calculate(self):
    
        try:
            expression = self.display.get()


            if expression == "":
                return

            balance = 0

            for char in expression:
                if char == "(":
                    balance += 1

                elif char == ")":
                    balance -= 1

                    if balance < 0:
                        raise ValueError("Invalid Parentheses")
            
            if balance != 0:
                raise ValueError("Unbalanced Parentheses")

            operators = "+*/^"

            for i in range(len(expression) - 1):
                current = expression[i]
                next_char = expression[i+1]

                if current in operators and next_char in "+*/^":
                    raise ValueError("Invalid operator combination")


            if expression[-1] in "+*/^":
                raise ValueError("Expression cannot end with operator")
                
            expression = re.sub(
                r'(?<![\d.)])-(\d+(?:\.\d+)?)\^',
                r'(-\1)^',
                expression
            )
                

            expression = expression.replace("^" , "**")

            result = eval(expression, {"__builtins__" : None} , {})

            result = self.clean_result(result)
            

            if result == 0:
                result = 0

            history_entry = f"{self.display.get()} = {result}"
            self.history.append(history_entry)

            if self.history_list is not None:
                self.history_list.insert(tk.END, history_entry)
                self.history_list.see(tk.END)

            self.display.delete(0 , tk.END)
            self.display.insert(0 , result)

            self.display.xview_moveto(1)
            self.update_display_font()

            self.last_result = result
            self.first_number = result
            self.operator = None
                    
            
        except Exception as e:
            print("ERROR :",e)
            self.display.delete(0,tk.END)
            self.display.insert(0,"Error")
            self.first_number = None
            self.operator = None
            self.last_result = None


    #-----------------Keyboard/Keypad with the UI---------------------------
    def key_pressed(self,event):
        if event.char in "0123456789":
            self.button_click(event.char)

        elif event.char in "+*/":
            self.operator_click(event.char)

        elif event.char == "-":
            if self.display.get() == "":
                self.display.insert(0, "-")

            else:
               self.operator_click("-")
            


        elif event.keysym == "Return":
            self.calculate()

        elif event.keysym == "BackSpace":
            self.backspace()

        elif event.keysym == "Escape":
            self.clear()

        elif event.char == ".":
            self.decimal_click()


        return "break"




            
         


    def clear(self):
    
        self.display.delete(0,tk.END)
        self.update_display_font()

        self.first_number = None
        self.operator = None
        self.last_result = None

    def clear_history(self,history_list):
        self.history.clear()
        history_list.delete(0, tk.END)


    def backspace(self):
        value = self.display.get()

        self.display.delete(0,tk.END)
        self.display.insert(0,value[:-1])
        self.update_display_font()

    
    def decimal_click(self):
        
        current = self.display.get()

        if current =="":
            self.display.insert(tk.END , "0.")
            return
        
        last_number = current.split("+")[-1].split("-")[-1].split("*")[-1].split("/")[-1].split("^")[-1]

        if "." not in last_number:
            self.display.insert(tk.END ,".")

        self.update_display_font()
        self.display.xview_moveto(1)

        

        

    def toggle_negative(self):
        value = self.display.get()


        if value == "":
            return 

        start = len(value)

        while start > 0 and (value[start -1].isdigit() or value[start -1] =="."):
            start -= 1


        number = value[start:]

        if number == "":
            return

        if start > 0 and value[start -1] == "-":

            self.display.delete(start-1 , tk.END)
            self.display.insert(tk.END, number)

        else:
            self.display.insert(start, "-")

            
        self.update_display_font()
        self.display.xview_moveto(1)


    def percentage(self):
        try:
            value = float(self.display.get())
            result = value / 100
            result = self.clean_result(result)
            

            history_entry = f"{value}% = {result}"
            self.history.append(history_entry)

            if self.history_list is not None:
                self.history_list.insert(tk.END, history_entry)
                self.history_list.see(tk.END)

            self.display.delete(0,tk.END)
            self.display.insert(0,result)

            self.update_display_font()
            self.display.xview_moveto(1)

        except:
            
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")

    def square_root(self):
        try:
            value = float(self.display.get())

            if value < 0:
                raise ValueError("Cannot calculate the Square Root of Negative Number")

            result = value ** 0.5
            result = self.clean_result(result)
            

            history_entry = f"√{value} = {result}"
            self.history.append(history_entry)
            
            if self.history_list is not None:
                self.history_list.insert(tk.END, history_entry)
                self.history_list.see(tk.END)
            

            self.display.delete(0, tk.END)
            self.display.insert(0, result)

            self.update_display_font()
            self.display.xview_moveto(1)

        except:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")


    def reciprocal(self):
        try:
            value = float(self.display.get())

            if value == 0:
                raise ValueError("Cannot divide by zero")

            result = 1 / value
            result = self.clean_result(result)
            

            history_entry = f"1/{value} = {result}"
            self.history.append(history_entry)
                        
            if self.history_list is not None:
                self.history_list.insert(tk.END, history_entry)
                self.history_list.see(tk.END)
            

            self.display.delete(0, tk.END)
            self.display.insert(0, result)

            self.update_display_font()
            self.display.xview_moveto(1)

        except:
            self.display.delete(0, tk.END)
            self.display.insert(0,"Error")


    def parentheses(self, brackets):
        current = self.display.get()

        if brackets == "(":
            if current != "" and (current[-1].isdigit() or current[-1] == ")"):
                self.display.insert(tk.END , "*")

            

        elif brackets == ")":
            if current == "":
                    return

            if current[-1] in "+-*/^(":
                    return

            if current.count("(") <= current.count(")"):
                return
        

        self.display.insert(tk.END, brackets)
       

        self.update_display_font()
        self.display.xview_moveto(1)

    def clean_result(self,result):
        if abs(result - round(result)) < 1e-9:
            return round(result)

        return round(result,10)

   
    def update_display_font(self):
     length = len(self.display.get())

     if length <= 10:
        size = 24
   
     else:
        size = max(16 , 24 - (length - 10 )*2)

     self.display.config(font=("Arial", size))


import tkinter as tk
from tkinter import ttk
import os
import sys



def create_window():
    window = tk.Tk()

    window.title("Calculator")
    if getattr(sys ,"frozen" , False):
        icon_path = os.path.join(sys._MEIPASS ,"Calculator_Icon.ico")
    else:
        icon_path = "Calculator_Icon.ico"
    window.iconbitmap(icon_path)
    
    window.geometry("650x500")
    window.configure(bg="#121212")

    window.rowconfigure(0, weight=0)
    window.rowconfigure(1, weight=1)

    for i in range(7):
        window.columnconfigure(i, weight=1)

    return window

#------------------------button_Frame-----------------------------
def create_button_frame(window):
    button_frame = tk.Frame(window , bg="#121212")
    for i in range(7):
        button_frame.columnconfigure(i, weight=1)
    for i in range(5):
        button_frame.rowconfigure(i, weight=1)


    button_frame.grid(
        row = 1,
        column = 0,
        columnspan = 7,
        sticky = "nsew"
        )
    return button_frame

#-----------------------------------Display-----------------------------------------------

def create_display(window):
    display = tk.Entry(window,font=("Arial",24),justify="right",bg="#1E1E1E" ,fg= "#F5F5F5", insertbackground="#F5F5F5", relief= "flat")
    display.grid(row=0 , column=0 , columnspan=7, padx=12, pady=(12,4), sticky="nsew")
    return display


#--------------------------buttons---------------------------------------------------------

def create_buttons(button_frame, text,row,column,command, bg = "#2D2D2D", activebackground="#555555", rowspan =1):
    button = tk.Button(
        button_frame,
        text = text,
        font=("Arial",18),
        width=5,
        height=2,
        bg= bg,
        fg= "white",
        activebackground= activebackground,
        activeforeground= "white",
        relief="flat",
        bd=0,
        command=command
    )

    button.grid(
        row = row,
        column = column,
        rowspan = rowspan,
        padx = 7,
        pady= 7,
        sticky= "nsew"

    )

    return button


def create_calculator_buttons(window, button_frame, calculator):

    #-------------------History Function------------------------

    def show_history():
        if calculator.history_window is not None:
            return


        history_window = tk.Toplevel(window)

        if getattr(sys, "frozen", False):
            history_icon_path = os.path.join(sys._MEIPASS, "Calculator_Icon.ico")
        else:
            history_icon_path = "Calculator_Icon.ico"
        history_window.iconbitmap(history_icon_path)
            
        history_window.configure(bg="#121212")

        calculator.history_window = history_window

        def close_history():
            calculator.history_window = None
            calculator.history_list = None
            history_window.destroy()

        history_window.protocol("WM_DELETE_WINDOW",close_history)


        history_window.title("Calculator History")
        history_window.geometry("350x400")

        history_window.rowconfigure(0, weight =1)
        history_window.rowconfigure(1, weight=0)
        history_window.columnconfigure(0, weight=1)

        history_frame = tk.Frame(history_window, bg="#121212")

        history_frame.grid(
            row = 0,
            column=0,
            sticky= "nsew"
        )

        style = ttk.Style()
        style.configure(
            "History.Vertical.TScrollbar",
            background = "#3A3A3A",
            troughcolor = "#121212",
            arrowcolor = "#F5F5F5",
            bordercolor = "#121212",
            lightcolor = "#121212",
            darkcolor = "#121212"

        )

        history_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", style = "History.Vertical.TScrollbar")

        calculator.history_list = tk.Listbox(
            history_frame,
            yscrollcommand= history_scrollbar.set,
            font= ("Arial", 14),
            bg="#1E1E1E",
            fg="#F5F5F5",
            selectbackground="#3F4A5A",
            selectforeground="#FFFFFF",
            relief="flat",
            bd =0
        )

        calculator.history_list.pack(
            side = "left",
            fill = "both",
            expand = True
        )

        history_scrollbar.pack(
            side="right",
            fill="y"

        )
        history_scrollbar.config(
            command= calculator.history_list.yview
        )
        for entry in calculator.history:
            calculator.history_list.insert(tk.END, entry)

        history_button_frame = tk.Frame(history_window , bg="#121212")

        history_button_frame.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        clear_history_button = tk.Button(
            history_button_frame,
            text = "Clear History",
            font=("Arial",11),
            bg="#C0392B",
            fg="#FFFFFF",
            activebackground="#A93226",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,

            command= lambda: calculator.clear_history(calculator.history_list)
        )

        clear_history_button.pack(
            fill="x",
            padx= 8,
            pady= 8
        )
        



#----------------------------------buttons------------------------------------------



    numbers = ["7","8","9","4","5","6","1","2","3","0"]

    for i , number in enumerate(numbers):
        row = 1 + i //3
        column = i % 3

        button = tk.Button(
            button_frame,
            text = number,
            command = lambda n = number: calculator.button_click(n), 
            font=("Arial", 18),
            width=5, 
            height=2,
            bg= "#2D2D2D",
            fg= "white",
            activebackground= "#555555",
            activeforeground= "white",
            relief="flat",
            bd=0

        )

        button.grid(row = row, column = column, padx =7, pady=7, sticky="nsew")


    create_buttons(button_frame, "+", 1, 3, lambda: calculator.operator_click("+"), bg = "#FF9500")
    create_buttons(button_frame, "-", 2, 3, lambda: calculator.operator_click("-"), bg = "#FF9500")
    create_buttons(button_frame, "*", 3, 3, lambda: calculator.operator_click("*"), bg = "#FF9500")
    create_buttons(button_frame, "/", 4, 3, lambda: calculator.operator_click("/"), bg = "#FF9500")


    equal_button = tk.Button(
        button_frame,
        text = "=",
        font=("Arial",18),
        width=5,
        height=2,
        bg= "#34C759",
        fg= "white",
        activebackground= "#5DD97A",
        activeforeground= "white",
        relief="flat",
        bd=0,
        command= calculator.calculate
    )

    equal_button.grid(row =4, column=2, padx =7, pady=7, sticky="nsew")






    clear_button = tk.Button(
        button_frame,
        text = "clear",
        font=("Arial",18),
        width=5,
        height=2,
        bg= "#FF3B30",
        fg= "white",
        activebackground= "#FF6259",
        activeforeground= "white",
        relief="flat",
        bd=0,
        
        command= calculator.clear

    )

    clear_button.grid(row =4 , column=1, padx =7, pady=7, sticky="nsew")

    backspace_buttons = tk.Button(
        button_frame,
        text="⌫",
        font=("Arial",18),
        width= 5 ,
        height=2,
        bg= "#4A4A4A",
        fg= "#FFFFFF",
        activebackground= "#5A5A5A",
        activeforeground= "#FFFFFF",
        relief="flat",
        bd=0,
        
        command= calculator.backspace)

    backspace_buttons.grid(row=4, column=4, padx =7, pady=7, sticky="nsew")


    decimal_button = tk.Button(
        button_frame,
        text=".",
        font=("Arial",18),
        width=5,
        height=2,
        bg= "#4A4A4A",
        fg= "white",
        activebackground= "#5A5A5A",
        activeforeground= "white",
        relief="flat",
        bd=0,
        
        command= calculator.decimal_click
    )

    decimal_button.grid(row = 3, column=4, padx =7, pady=7, sticky="nsew")


    create_buttons(button_frame, "+/-" , 2, 4, calculator.toggle_negative, bg="#4A4A4A", activebackground="#5A5A5A")

    create_buttons(button_frame, "xʸ" , 2 , 5 , lambda : calculator.operator_click("^") , bg= "#FF9500")

    create_buttons(button_frame, "√" , 3, 5, calculator.square_root, bg="#4A4A4A", activebackground="#5A5A5A")

    create_buttons(button_frame, "1/x", 4, 5, calculator.reciprocal, bg="#4A4A4A", activebackground="#5A5A5A")

    create_buttons(button_frame, "(", 1, 6, lambda :calculator.parentheses("("), bg="#3F4A5A", activebackground="#526176",rowspan=2)

    create_buttons(button_frame, ")", 3, 6, lambda :calculator.parentheses(")"), bg="#3F4A5A", activebackground="#526176",rowspan=2)


    history_button = tk.Button(
        button_frame,
        text="History",
        font=("Arial",18),
        width= 5 ,
        height=2,
        bg= "#3F4A5A",
        fg= "#FFFFFF",
        activebackground= "#526176",
        activeforeground= "#FFFFFF",
        relief="flat",
        bd=0,
        
        command= show_history)


    history_button.grid(row=1, column=4, padx =7, pady=7, sticky="nsew")

    create_buttons(button_frame, "%", 1, 5, calculator.percentage, bg= "#4A4A4A", activebackground="#5A5A5A" )

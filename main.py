from calculator import Calculator
from ui import (
    create_window, 
    create_button_frame, 
    create_display,  
    create_calculator_buttons
)


      

#----------------------------------window------------------------------------------

window = create_window()



#------------------------button_Frame-----------------------------
button_frame = create_button_frame(window)

#----------------Display--------------------
display = create_display(window)

#---------Connecting the Display with Calculator---------------------------
calculator = Calculator(display)

create_calculator_buttons(window, button_frame, calculator)


#-------------------keyboard Binding----------------------------------------

window.bind("<Key>", calculator.key_pressed)




window.mainloop()
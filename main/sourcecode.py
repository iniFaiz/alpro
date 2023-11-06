import tkinter as tk
import customtkinter as ctk
import time


#aplikasinya
app = ctk.CTk()
app.title("organize")
app.geometry("900x600")

#frame samping
sidebar = ctk.CTkFrame(master=app, width=200, corner_radius=0, fg_color="#FAFAF5", border_width=10, border_color="#A9CCE3",)
sidebar.pack(side='left', fill='y',)

main_content = ctk.CTkFrame(master=app, fg_color="#A9CCE3", corner_radius=0)
main_content.pack(side='right', fill='both', expand=True)

#tombol
def menu_button_click(button_name):
    print(f"{button_name} clicked!")
    
buttons_names = ["Pomodoro", "To-do list", "Stopwatch", "Analisis"]
for name in buttons_names:
    button = ctk.CTkButton(master=sidebar, text=name,
                            command=lambda n=name: menu_button_click(n), corner_radius=8, fg_color="#75A5D0", hover_color="#5084B9", height=50)
    button.pack(pady=20, padx=20, fill='x')
    


app.mainloop()

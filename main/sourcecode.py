import tkinter as tk
import customtkinter as ctk
import time
import csv
from win10toast import ToastNotifier
from tkinter import *
 
app = ctk.CTk()
app.title("organize")
app.geometry("900x600")
app.resizable(width=0, height=0)


# frame samping
sidebar = ctk.CTkFrame(master=app,
                       width=200,
                       corner_radius=0, 
                       fg_color="#FAFAF5", 
                       border_width=10, 
                       border_color="#A9CCE3",)
sidebar.pack(side='left', fill='y',)
# sidebar.pack_propagate(False)
# sidebar.configure()
 
#main content
main_content = ctk.CTkFrame(master=app, 
                            fg_color="#A9CCE3", 
                            corner_radius=0)
main_content.pack(side='right', fill='both', expand=True)

# function
def todolist():
    todolist = ctk.CTkFrame(master = main_content)
    label = ctk.CTkLabel(master = todolist,
                        fg_color = '#c9d1d9',
                        font = ('Arial Bold', 40),
                        width = 640,
                        height = 400
                        )
    label.pack(fill = 'both')
    todolist.pack()
    
def delete_pages():
    for frame in main_content.winfo_children():
        frame.destroy()

def hide_indicate():
    pomodoro_btn.configure(fg_color = '#75A5D0')
    todo_btn.configure(fg_color = '#75A5D0')
    stopwatch_btn.configure(fg_color = "#75A5D0")
    analisis_btn.configure(fg_color = "#75A5D0")

def indicate(lb, page):
    hide_indicate()
    lb.configure(fg_color = '#5084B9')
    delete_pages()
    page()

# tombol pomodoro
pomodoro_btn = ctk.CTkButton(sidebar, 
                             text='Pomodoro', 
                             corner_radius=8, 
                             fg_color="#75A5D0", 
                             hover_color="#5084B9", 
                             height=50,
                             command= lambda: indicate(pomodoro_btn, pomodoro_page))
pomodoro_btn.pack(pady=20, padx=20, fill='x')
 
# tombol todo list
todo_btn = ctk.CTkButton(sidebar, 
                         text='To-Do List', 
                         corner_radius=8, 
                         fg_color="#75A5D0", 
                         hover_color="#5084B9", 
                         height=50,
                         command= lambda: indicate(todo_btn, todolist))
todo_btn.pack(pady=20, padx=20, fill='x')
 
# tombol stopwatch
stopwatch_btn = ctk.CTkButton(sidebar, 
                              text='Stopwatch', 
                              corner_radius=8, 
                              fg_color="#75A5D0", 
                              hover_color="#5084B9", 
                              height=50)
stopwatch_btn.pack(pady=20, padx=20, fill='x')
 
# tombol analisis
analisis_btn = ctk.CTkButton(sidebar, 
                             text='Analisis', 
                             corner_radius=8, 
                             fg_color="#75A5D0", 
                             hover_color="#5084B9", 
                             height=50)
analisis_btn.pack(pady=20, padx=20, fill='x')

#page pomodoro
def pomodoro_page():
    
    pomodoro_timer_label = ctk.CTkLabel(main_content, 
                                    text="25:00", 
                                    font=("Helvetica", 180))
    pomodoro_timer_label.pack(pady=100)
 

    pomodoro_running = False
    pomodoro_time = 1500 #dalam detik = 25 menit
    # Tombol up untuk memulai pomodoro
    up_button = ctk.CTkButton(main_content, 
                          text="▲", 
                          width=80, 
                          height=80, 
                          corner_radius=20, 
                          command=start_pomodoro)
    up_button.pack(side='left', padx=110)
 
    # Tombol down untuk menghentikan pomodoro
    reset_button = ctk.CTkButton(main_content, 
                            text="■", 
                            width=80, 
                            height=80, 
                            corner_radius=20, 
                            command=stop_pomodoro)
    reset_button.pack(side='right', padx=110)
 
    # Tombol pause (||)
    pause_button = ctk.CTkButton(main_content, 
                             text="||", 
                             width=80, 
                             height=80, 
                             corner_radius=20, 
                             command=pause_pomodoro)
    pause_button.pack(side='right', padx=20)

# Fungsi untuk memulai pomodoro
def start_pomodoro():
    global pomodoro_running, pomodoro_time
    if not pomodoro_running:
        pomodoro_running = True
        update_pomodoro_timer()
 
# Fungsi untuk melakukan pause pada pomodoro
def pause_pomodoro():
    global pomodoro_running
    pomodoro_running = False
 
# Fungsi untuk menghentikan pomodoro
def stop_pomodoro():
    global pomodoro_running, pomodoro_time
    pomodoro_running = False
    pomodoro_time = 1500
    pomodoro_timer_label.configure(text="25:00")
 
 
# Fungsi untuk mengupdate timer pomodoro
def update_pomodoro_timer():
    global pomodoro_running, pomodoro_time
    if pomodoro_running and pomodoro_time > 0:
        minutes, seconds = divmod(pomodoro_time, 60)
        timer_text = "{:02d}:{:02d}".format(minutes, seconds)
        pomodoro_timer_label.configure(text=timer_text)
        pomodoro_time -= 1
        app.after(1000, update_pomodoro_timer)
    elif pomodoro_running and pomodoro_time == 0:
        pomodoro_running = False
        pomodoro_timer_label.configure(text="25:00")
        toaster.show_toast("Pomodoro", "Waktu pomodoro sudah habis. Istirahat sejenak!", duration=300)
 
# Fungsi untuk menampilkan notifikasi
toaster = ToastNotifier()
 












# Label untuk To-Do-List
# todo_label = ctk.CTkLabel(main_content, 
#                           text="To-Do List", 
#                           font=("Helvetica", 24))
# todo_label.pack(pady=20)
 
# # Entry untuk memasukkan tugas baru
# todo_entry = ctk.CTkEntry(main_content, 
#                           font=("Helvetica", 14))
# todo_entry.pack(pady=10)
 
# # Listbox untuk menampilkan daftar tugas
# todo_listbox = tk.Listbox(main_content, 
#                               font=("Helvetica", 14), 
#                               selectmode=tk.SINGLE, 
#                               height=10, width=40)
# todo_listbox.pack(pady=10)
 
# # Fungsi untuk menambahkan tugas baru
# def add_task():
#     task = todo_entry.get()
#     if task:
#         todo_listbox.insert(tk.END, task)
#         todo_entry.delete(0, tk.END)
 
# # Fungsi untuk menghapus tugas yang dipilih
# def delete_task():
#     selected_task_index = todo_listbox.curselection()
#     if selected_task_index:
#         todo_listbox.delete(selected_task_index)
 
# # Tombol untuk menambahkan tugas baru
# add_task_button = ctk.CTkButton(main_content, 
#                                 text="Add Task", 
#                                 command=add_task)
# add_task_button.pack(pady=10)
 
# # Tombol untuk menghapus tugas yang dipilih
# delete_task_button = ctk.CTkButton(main_content, 
#                                    text="Delete Task", 
#                                    command=delete_task)
# delete_task_button.pack(pady=10)
 
app.mainloop()

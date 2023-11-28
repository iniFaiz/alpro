import tkinter as tk
import tkcalendar
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
    
# variable global untuk todo list
todo_entry = None
todo_listbox = None

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
                              height=50,
                              command= lambda: indicate(stopwatch_btn, stopwatch_page))
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
                          text="▶", 
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
 

def stopwatch_page():
    global stopwatch_running
    global stopwatch_counter
    global time_label
    stopwatch_running = False
    stopwatch_counter = 0  # Menghitung dalam milidetik
    # Membuat label untuk menampilkan waktu
    time_label = ctk.CTkLabel(main_content, pady= 150, text="00:00:00.00", font=("Helvetica", 100,))
    time_label.pack(pady=20)

    # Membuat tombol untuk kontrol stopwatch
    start_button = ctk.CTkButton(main_content, width=80, height=80, corner_radius=20, text="▶", command=start_stopwatch)
    start_button.pack(side= 'left', padx=10, )

    stop_button = ctk.CTkButton(main_content, width=80, height=80, corner_radius=20, text="■", command=stop_stopwatch)
    stop_button.pack(side= 'left', padx=210,)

    reset_button = ctk.CTkButton(main_content, width=80, height=80, corner_radius=20, text="Reset", command=reset_stopwatch)
    reset_button.pack(side= 'right', padx=10,) 

# Fungsi untuk memperbarui waktu pada label
def update_time():
    if stopwatch_running:
        global stopwatch_counter
        stopwatch_counter += 16  # Menambah 10 milidetik
        milliseconds = stopwatch_counter % 1000
        seconds = (stopwatch_counter // 1000) % 60
        minutes = (stopwatch_counter // (1000 * 60)) % 60
        hours = (stopwatch_counter // (1000 * 60 * 60)) % 24

        time_display = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{int(milliseconds/10):02d}"
        time_label.configure(text=time_display)
        app.after(10, update_time)  # Update setiap 10 milidetik

# Fungsi untuk memulai/melanjutkan stopwatch
def start_stopwatch():
    global stopwatch_running
    if not stopwatch_running:
        stopwatch_running = True
        update_time()

# Fungsi untuk menghentikan stopwatch
def stop_stopwatch():
    global stopwatch_running
    stopwatch_running = False

# Fungsi untuk mereset stopwatch
def reset_stopwatch():
    global stopwatch_counter, stopwatch_running
    stopwatch_running = False
    stopwatch_counter = 0
    time_label.configure(text="00:00:00.00")
    
# function for To-Do List
def todolist():
    global todo_entry, todo_listbox, deadline_entry
    todolist_frame = ctk.CTkFrame(master=main_content,
                                  fg_color= "#A9CCE3")
    todolist_frame.pack(expand=True, fill='both')

    todo_label = ctk.CTkLabel(master=todolist_frame,
                              text="To-Do List",
                              font=('Arial Bold', 20))
    todo_label.pack(pady=20)

    
    entry_frame = ctk.CTkFrame(todolist_frame)
    entry_frame.pack(pady=10)

    deadline_frame = ctk.CTkFrame(todolist_frame)
    deadline_frame.pack(pady=10)

    # Tambah Label di sebelah kiri Entry
    label_placeholder = ctk.CTkLabel(entry_frame,
                                     text="Masukkan To-Do List")
    label_placeholder.pack(side="left", padx=5)

    # Set teks default untuk Entry
    todo_entry = ctk.CTkEntry(entry_frame,
                              font=("Helvetica", 14),
                              width=180)
    todo_entry.pack(side="left", padx=5)
    
    # Tambah Entry untuk Deadline
    deadline_label = ctk.CTkLabel(deadline_frame,
                                  text="Deadline:")
    deadline_label.pack(side="left", pady=5)

    deadline_entry = tkcalendar.DateEntry(deadline_frame,
                                          width=52,
                                          fg_colour='#5084B9')
    deadline_entry.pack(side="left", pady=5)


    todo_listbox = tk.Listbox(todolist_frame,
                              font=("Helvetica", 14),
                              selectmode=tk.SINGLE,
                              height=18, width=75)
    todo_listbox.pack(pady=10)

    add_task_button = ctk.CTkButton(todolist_frame,
                                    text="Add Task",
                                    command=add_task)
    add_task_button.pack(side='left', padx=20)

    delete_task_button = ctk.CTkButton(todolist_frame,
                                       text="Delete Task",
                                       command=delete_task)
    delete_task_button.pack(side='right', padx=20)
    
    return todolist_frame

# function for To-Do List
def add_task():
    global todo_entry, todo_listbox
    task = todo_entry.get()
    if task:
        todo_listbox.insert(tk.END, task)
        todo_entry.delete(0, tk.END)


# function for To-Do List
def delete_task():
    global todo_listbox
    selected_task_index = todo_listbox.curselection()
    if selected_task_index:
        todo_listbox.delete(selected_task_index)
        
# function for To-Do List
def add_task():
    global todo_entry, todo_listbox, deadline_entry
    task = todo_entry.get()
    deadline = deadline_entry.get_date()  # Get the selected date from DateEntry

    if task:
        task_with_deadline = f"{task} - Deadline: {deadline.strftime('%Y-%m-%d')}"
        todo_listbox.insert(tk.END, task_with_deadline)
        todo_entry.delete(0, tk.END)
        deadline_entry.set_date(None) 



 
app.mainloop()

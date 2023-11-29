import tkinter as tk
import tkcalendar
import customtkinter as ctk
import time
import csv
import datetime
from win10toast import ToastNotifier
from tkinter import *
from threading import Thread



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
 
#main content
main_content = ctk.CTkFrame(master=app, 
                            fg_color="#A9CCE3", 
                            corner_radius=0)
main_content.pack(side='right', fill='both', expand=True)
main_label = ctk.CTkLabel(master=main_content, text="Organize\nManajemen waktu bersama kami",
                         font=('Arial Bold', 34), text_color='#0d1117')
main_label.place(x=100,y=250)

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
                             height=50,
                             command= lambda: indicate(analisis_btn, analisis_page))
analisis_btn.pack(pady=20, padx=20, fill='x')

# POMODORO

def pomodoro_page():
    global notifier
    global timer_seconds
    global rest_time
    global timer_running
    global timer_label
    global start_button
    global add_button
    global subtract_button
    global stop_button
    global resume_button
    global reset_button
    #notifier
    notifier = ToastNotifier()

    #values
    timer_seconds = 30 * 60  # 30 minutes
    rest_time = False
    timer_running = False

    # Timer label
    timer_label = ctk.CTkLabel(main_content,
                               pady=150,
                               text="30:00",
                               font=("Arial", 100))
    timer_label.pack(pady=20)

    # Buttons
    start_button = ctk.CTkButton(main_content,
                                 width=80, height=80,
                                 corner_radius=20,
                                 text="▶",
                                 command=start_timer)
    
    add_button = ctk.CTkButton(main_content, 
                               width=80, 
                               height=80, 
                               corner_radius=20,
                               text="+", 
                               command=add_time)
    
    subtract_button = ctk.CTkButton(main_content, 
                                    width=80, 
                                    height=80, 
                                    corner_radius=20,
                                    text="-", 
                                    command=subtract_time)
    
    stop_button = ctk.CTkButton(main_content, 
                                text="Stop", 
                                command=stop_timer)
    
    resume_button = ctk.CTkButton(main_content, 
                                  text="Resume", 
                                  command=resume_timer)
    
    reset_button = ctk.CTkButton(main_content, 
                                 text="Reset", 
                                 command=reset_timer)

    start_button.pack(side='left', padx=10, pady=10)
    add_button.pack(side='left', padx=210, pady=10)
    subtract_button.pack(side='right', padx=10, pady=10)

def update_timer():
    global timer_running, timer_seconds, rest_time
    while timer_running:
        time.sleep(1)
        timer_seconds -= 1

        if timer_seconds <= 0:
            if rest_time:
                timer_running = False
                notifier.show_toast("Pomodoro Timer", "Waktu istirahat selesai!", duration=5)
            else:
                notifier.show_toast("Pomodoro Timer", "Waktu bekerja selesai, mulai istirahat!", duration=5)
                timer_seconds = 5 * 60  # Istirahat 5 menit
                rest_time = True
        else:
            if not rest_time and timer_seconds == (30 * 60):
                notifier.show_toast("Pomodoro Timer", "30 menit telah lewat, mulai istirahat!", duration=5)
                timer_seconds = 5 * 60  # Istirahat 5 menit
                rest_time = True
        if not timer_running:
            break
        minutes, seconds = divmod(timer_seconds, 60)
        timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")

def start_timer():
    global timer_running
    timer_running = True
    thread = Thread(target=update_timer)
    thread.start()
    start_button.pack_forget()
    add_button.pack_forget()
    subtract_button.pack_forget()
    stop_button.pack(pady=10)
    reset_button.pack(pady=10)
    resume_button.pack_forget()

def stop_timer():
    global timer_running
    timer_running = False
    stop_button.pack_forget()
    resume_button.pack(pady=10)

def resume_timer():
    global timer_running
    timer_running = True
    thread = Thread(target=update_timer)
    thread.start()
    resume_button.pack_forget()
    stop_button.pack(pady=10)

def reset_timer():
    global timer_seconds, rest_time, timer_running
    timer_running = False
    timer_seconds = 30 * 60
    rest_time = False
    update_timer_label()
    stop_button.pack_forget()
    reset_button.pack_forget()
    resume_button.pack_forget()
    start_button.pack(side='left', padx=10, pady=10)
    add_button.pack(side='left', padx=210, pady=10)
    subtract_button.pack(side='right', padx=10, pady=10)

def add_time():
    global timer_seconds
    if not rest_time:
        timer_seconds += 30 * 60
        update_timer_label()

def subtract_time():
    global timer_seconds
    if not rest_time and timer_seconds > 30 * 60:
        timer_seconds -= 30 * 60
        update_timer_label()

def update_timer_label():
    minutes, seconds = divmod(timer_seconds, 60)
    timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")

# TO DO LIST

todo_listbox=None
todo_entries = []
 
def todolist():
    global todo_entry, todo_listbox, deadline_entry
    todolist_frame = ctk. CTkFrame(master = main_content,
                                   fg_color="#A9CCE3")
    todolist_frame.pack(expand=True, fill='both')
    
    todo_label = ctk.CTkLabel(master=todolist_frame,
                              text="To-Do List",
                              font = ('Arial Bold', 20))
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

    load_datatodo()

# function for To-Do List
def add_task():
    global todo_entry, todo_listbox
    task = todo_entry.get()
    if task:
        todo_listbox.insert(tk.END, task)
        todo_entry.delete(0, tk.END)


# function for To-Do List
def add_task():
    global todo_entry, todo_listbox, deadline_entry, todo_entries
    task = todo_entry.get()
    deadline = deadline_entry.get_date()

    if task:
        task_with_deadline = f"{task} - Deadline: {deadline.strftime('%Y-%m-%d')}"
        todo_entries.append(task_with_deadline)
        todo_listbox.insert(tk.END, task_with_deadline)
        todo_entry.delete(0, tk.END)
        deadline_entry.set_date(None)
        add_data()

def delete_task():
    global todo_listbox, todo_entries
    selected_task_index = todo_listbox.curselection()
    if selected_task_index:
        todo_listbox.delete(selected_task_index)
        todo_entries.pop(selected_task_index[0])
        add_data()

def add_data():
    with open('todolist.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for entry in todo_entries:
            writer.writerow([entry])

def load_datatodo():
    try:
        with open('todolist.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                todo_entries.append(row[0])
                todo_listbox.insert(tk.END, row[0])
    except FileNotFoundError:
        pass
   
# STOPWATCH        

def stopwatch_page():
    global stopwatch_running
    global stopwatch_counter
    global time_label
    stopwatch_running = False
    stopwatch_counter = 0  # Menghitung dalam milidetik
    # Membuat label untuk menampilkan waktu
    time_label = ctk.CTkLabel(main_content, 
                              pady= 150, 
                              text="00:00:00.00", 
                              font=("Helvetica", 100,))
    time_label.pack(pady=20)

    # Membuat tombol untuk kontrol stopwatch
    start_button = ctk.CTkButton(main_content, 
                                 width=80, 
                                 height=80, 
                                 corner_radius=20, 
                                 text="▶", 
                                 command=start_stopwatch)
    start_button.pack(side= 'left', padx=10, )

    stop_button = ctk.CTkButton(main_content, 
                                width=80, 
                                height=80, 
                                corner_radius=20, 
                                text="■", 
                                command=stop_stopwatch)
    stop_button.pack(side= 'left', padx=210,)

    reset_button = ctk.CTkButton(main_content, 
                                 width=80, 
                                 height=80, 
                                 corner_radius=20, 
                                 text="Reset", 
                                 command=reset_stopwatch)
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
    
# ANALISIS     

def analisis_page():
    global analisis_frame
    analisis_frame = ctk.CTkFrame(master=main_content)

app.mainloop()

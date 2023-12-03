import tkinter as tk
import customtkinter as ctk
import time
import csv
from datetime import datetime
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
# sidebar.pack_propagate(False)
# sidebar.configure()
 
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
                         command= lambda: indicate(todo_btn, todo_page))
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
    timer_seconds = 1 * 60  # 30 minutes
    rest_time = False
    timer_running = False

    # Timer label
    timer_label = ctk.CTkLabel(main_content, pady=150, text="30:00", font=("Arial", 100))
    timer_label.pack(pady=20)

    # Buttons
    start_button = ctk.CTkButton(main_content, width=80, height=80, corner_radius=20,text="▶", command=start_timer)
    add_button = ctk.CTkButton(main_content, width=80, height=80, corner_radius=20,text="+", command=add_time)
    subtract_button = ctk.CTkButton(main_content, width=80, height=80, corner_radius=20,text="-", command=subtract_time)
    stop_button = ctk.CTkButton(main_content, text="Stop", command=stop_timer)
    resume_button = ctk.CTkButton(main_content, text="Resume", command=resume_timer)
    reset_button = ctk.CTkButton(main_content, text="Reset", command=reset_timer)

    start_button.pack(side='left', padx=10, pady=10)
    add_button.pack(side='left', padx=210, pady=10)
    subtract_button.pack(side='right', padx=10, pady=10)


def start_timer():
    global timer_running, start_time
    timer_running = True
    start_time = datetime.now()
    thread = Thread(target=update_timer)
    thread.start()
    start_button.pack_forget()
    add_button.pack_forget()
    subtract_button.pack_forget()
    stop_button.pack(pady=10)
    reset_button.pack(pady=10)
    resume_button.pack_forget()

def stop_timer():
    global timer_running, end_time, duration, save_pomodoro_session
    timer_running = False
    end_time = datetime.now()  # Catat waktu selesai
    duration = end_time - start_time
    save_pomodoro_session(duration, start_time)
    stop_button.pack_forget()
    resume_button.pack(pady=10)

def save_pomodoro_session(duration, start_time):
    with open('pomodoro_sessions.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([start_time.strftime("%Y-%m-%d %H:%M:%S"), str(duration)])

def resume_timer():
    global timer_running
    timer_running = True
    thread = Thread(target=update_timer)
    thread.start()
    resume_button.pack_forget()
    stop_button.pack(pady=10)

def reset_timer():
    global timer_seconds, rest_time, timer_running, update_timer_label
    if timer_running:
        end_time = datetime.now()  # Catat waktu saat reset
        duration = end_time - start_time  # Hitung durasi
        save_pomodoro_session(duration, start_time)  # Simpan sesi ke CSV
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

def reset_to_initial_state():
    global timer_seconds, rest_time, timer_running
    timer_running = False
    timer_seconds = 30 * 60  # Reset waktu ke 30 menit
    rest_time = False
    update_timer_label()
    # Kembali ke tampilan awal
    stop_button.pack_forget()
    reset_button.pack_forget()
    resume_button.pack_forget()
    start_button.pack(side='left', padx=10, pady=10)
    add_button.pack(side='left', padx=210, pady=10)
    subtract_button.pack(side='right', padx=10, pady=10)

def update_timer():
    global timer_running, timer_seconds, rest_time
    while timer_running:
        time.sleep(1)
        timer_seconds -= 1

        if timer_seconds <= 0:
            end_time = datetime.now()  # Catat waktu saat timer berakhir
            duration = end_time - start_time  # Hitung durasi
            if rest_time:
                timer_running = False
                notifier.show_toast("Pomodoro Timer", "Waktu istirahat selesai!", duration=5)
                save_pomodoro_session(duration, start_time)
                reset_to_initial_state()
            else:
                notifier.show_toast("Pomodoro Timer", "Waktu bekerja selesai, mulai istirahat!", duration=5)
                timer_seconds = 1 * 60  # Istirahat 5 menit
                rest_time = True
        else:
            if not rest_time and timer_seconds == (30 * 60):
                notifier.show_toast("Pomodoro Timer", "30 menit telah lewat, mulai istirahat!", duration=5)
                timer_seconds = 1 * 60  # Istirahat 5 menit
                rest_time = True
        if not timer_running:
            break
        minutes, seconds = divmod(timer_seconds, 60)
        timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")

 
def todo_page():
    global task_listbox
    # Membuat frame untuk To-Do List
    todo_frame = ctk.CTkFrame(main_content)
    todo_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Tombol untuk membuka pop-up penambahan task
    add_task_btn = ctk.CTkButton(todo_frame, text="+", command=open_add_task_popup)
    add_task_btn.pack(side="top", pady=10)

    # Listbox untuk menampilkan daftar task
    task_listbox = tk.Listbox(todo_frame)
    task_listbox.pack(pady=20, fill="both", expand=True)

    # Tombol untuk menghapus task yang dipilih
    delete_task_btn = ctk.CTkButton(todo_frame, text="Delete Task", command=delete_task)
    delete_task_btn.pack(side="bottom", pady=10)
    
    load_datatodo()

# database todolist
def add_data():
    item = task_entry.get().strip()
    if item:
        task_listbox.insert(tk.END, item)
        data_todo()

# save data
def data_todo():
    with open('todolist.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in range(task_listbox.size()):
            writer.writerow([task_listbox.get(i)])
    

# Fungsi untuk menambahkan task
def add_task():
    task = task_entry.get()
    if task:
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)

# Fungsi untuk menghapus task yang dipilih
def delete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        # Menghapus task dari Listbox
        task_listbox.delete(selected_task_index)

        # Membaca semua task dari CSV dan menyimpan kecuali yang dihapus
        remaining_tasks = []
        with open('todolist.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index != selected_task_index[0]:
                    remaining_tasks.append(row)

        # Menulis ulang file CSV dengan task yang tersisa
        with open('todolist.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for task in remaining_tasks:
                writer.writerow(task)

#load database todo
def load_datatodo():
    try:
        with open('todolist.csv', 'r', newline= '') as file:
            reader = csv.reader(file)
            for row in reader:
                task_listbox.insert(tk.END, row[0])
    except FileNotFoundError:
        pass

# Membuat pop-up untuk menambahkan task
def open_add_task_popup():
    popup = ctk.CTkToplevel(app)
    popup.title("Add Task")
    
    global task_entry
    task_entry = ctk.CTkEntry(popup, width=200)
    task_entry.pack(pady=10)
    
    add_task_button = ctk.CTkButton(popup, text="Add Task", command=add_data)
    add_task_button.pack()

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
        stopwatch_counter += int(13.5)
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

def analisis_page():
    global analisis_frame, data_listbox
    analisis_frame = ctk.CTkFrame(master=main_content)
    analisis_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Membuat Listbox untuk menampilkan data
    data_listbox = tk.Listbox(analisis_frame)
    data_listbox.pack(pady=20, fill="both", expand=True)

    # Membaca dan menampilkan data dari CSV
    try:
        with open('pomodoro_sessions.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                data_listbox.insert(tk.END, row)
    except FileNotFoundError:
        # Tindakan jika file tidak ditemukan
        data_listbox.insert(tk.END, "Data tidak ditemukan")

    # Tombol reset
    reset_button = ctk.CTkButton(analisis_frame, text="Reset Data", command=reset_database)
    reset_button.pack(pady=10)

def reset_database():
    # Mengosongkan file CSV
    open('pomodoro_sessions.csv', 'w').close()

    # Mengosongkan data di Listbox
    data_listbox.delete(0, tk.END)

    # Menampilkan pop-up konfirmasi
    popup = ctk.CTkToplevel(app)
    popup.title("Konfirmasi")
    confirmation_label = ctk.CTkLabel(popup, text="Keseluruhan data analisis sudah di reset")
    confirmation_label.pack(pady=20)
    close_button = ctk.CTkButton(popup, text="Tutup", command=popup.destroy)
    close_button.pack(pady=10)





app.mainloop()

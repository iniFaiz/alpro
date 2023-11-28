import tkinter as tk
import tkcalendar
import customtkinter as ctk
import time
from win10toast import ToastNotifier

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

# main content
main_content = ctk.CTkFrame(master=app,
                            fg_color="#A9CCE3",
                            corner_radius=0)
main_content.pack(side='right', fill='both', expand=True)

# variable global untuk pomodoro
pomodoro_running = False
pomodoro_time = 1500  # dalam detik = 25 menit
pomodoro_timer_label = None

# variable global untuk todo list
todo_entry = None
todo_listbox = None

# variable global untuk stopwatch
stopwatch_running = False
stopwatch_seconds = 0
stopwatch_label = None
result_label = None
time_listbox = None

# variable global untuk notifikasi
toaster = ToastNotifier()


# function
def delete_pages(exclude_frame = None):
    for frame in main_content.winfo_children():
        if frame != exclude_frame:
            frame.destroy()


def hide_indicate():
    pomodoro_btn.configure(fg_color='#75A5D0')
    todo_btn.configure(fg_color='#75A5D0')
    stopwatch_btn.configure(fg_color="#75A5D0")
    analisis_btn.configure(fg_color="#75A5D0")


def indicate(lb, page):
    hide_indicate()
    lb.configure(fg_color='#5084B9')
    delete_pages()
    page()


# tombol pomodoro
pomodoro_btn = ctk.CTkButton(sidebar,
                             text='Pomodoro',
                             corner_radius=8,
                             fg_color="#75A5D0",
                             hover_color="#5084B9",
                             height=50,
                             command=lambda: indicate(pomodoro_btn, pomodoro_page))
pomodoro_btn.pack(pady=20, padx=20, fill='x')

# tombol todo list
todo_btn = ctk.CTkButton(sidebar,
                         text='To-Do List',
                         corner_radius=8,
                         fg_color="#75A5D0",
                         hover_color="#5084B9",
                         height=50,
                         command=lambda: indicate(todo_btn, lambda: todolist()))
todo_btn.pack(pady=20, padx=20, fill='x')

# tombol stopwatch
stopwatch_btn = ctk.CTkButton(sidebar,
                              text='Stopwatch',
                              corner_radius=8,
                              fg_color="#75A5D0",
                              hover_color="#5084B9",
                              height=50,
                              command=lambda: indicate(stopwatch_btn, stopwatch_page))
stopwatch_btn.pack(pady=20, padx=20, fill='x')

# tombol analisis
analisis_btn = ctk.CTkButton(sidebar,
                             text='Analisis',
                             corner_radius=8,
                             fg_color="#75A5D0",
                             hover_color="#5084B9",
                             height=50)
analisis_btn.pack(pady=20, padx=20, fill='x')


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


# function for Stopwatch
def stopwatch_page():
    global stopwatch_running, stopwatch_seconds, stopwatch_label, result_label, time_listbox
    stopwatch_frame = ctk.CTkFrame(master=main_content,
                                   fg_color= "#A9CCE3")
    stopwatch_frame.pack(expand=True, fill='both')

    stopwatch_label = ctk.CTkLabel(stopwatch_frame,
                                   text="00:00",
                                   font=("Helvetica", 180))
    stopwatch_label.pack(pady=10) 

    # Tambahkan Listbox untuk menampilkan waktu yang di-reset
    time_listbox = tk.Listbox(stopwatch_frame,
                              font=("Helvetica", 14),
                              selectmode=tk.SINGLE,
                              height=5, width=60)
    time_listbox.pack(pady=10, padx=60)  # Tampilkan Listbox

    delete_time_button = ctk.CTkButton(stopwatch_frame,
                                        text="Delete",
                                        command= delete_time)
    delete_time_button.pack(pady=20)

    result_label = ctk.CTkLabel(stopwatch_frame,
                                text="",
                                font=("Helevetica", 16))
    result_label.pack(pady=5)  
    
    start_stopwatch_button = ctk.CTkButton(stopwatch_frame,
                                           text="Start",
                                           command=start_stopwatch)
    start_stopwatch_button.pack(side='left', padx=100)

    reset_stopwatch_button = ctk.CTkButton(stopwatch_frame,
                                           text="Reset",
                                           command=reset_stopwatch)
    reset_stopwatch_button.pack(side='right', padx=100)
     
# function for Pomodoro
def pomodoro_page():
    global pomodoro_running, pomodoro_time, pomodoro_timer_label
    pomodoro_frame = ctk.CTkFrame(master=main_content,
                                  fg_color= "#A9CCE3")
    pomodoro_frame.pack(expand=True, fill='both')

    pomodoro_timer_label = ctk.CTkLabel(pomodoro_frame,
                                        text="25:00",
                                        font=("Helvetica", 180))
    pomodoro_timer_label.pack(pady=100)

    up_button = ctk.CTkButton(pomodoro_frame,
                              text="▲",
                              width=80,
                              height=80,
                              corner_radius=20,
                              command=start_pomodoro)
    up_button.pack(side='left', padx=110)

    reset_button = ctk.CTkButton(pomodoro_frame,
                                 text="■",
                                 width=80,
                                 height=80,
                                 corner_radius=20,
                                 command=stop_pomodoro)
    reset_button.pack(side='right', padx=110)

    pause_button = ctk.CTkButton(pomodoro_frame,
                                 text="||",
                                 width=80,
                                 height=80,
                                 corner_radius=20,
                                 command=pause_pomodoro)
    pause_button.pack(side='right', padx=20)


# function for Stopwatch
def start_stopwatch():
    global stopwatch_running, stopwatch_seconds
    if not stopwatch_running:
        stopwatch_running = True
        update_stopwatch()

def reset_stopwatch():
    global stopwatch_running, stopwatch_seconds
    stopwatch_running = False
    minutes, seconds = divmod(stopwatch_seconds, 60)
    timer_text = "{:02d}:{:02d}".format(minutes, seconds)
    result_label.configure(text=f"Stopwatch Result: {timer_text}")  # Tampilkan hasil stopwatch di label
    time_listbox.insert(tk.END, timer_text)  # Tambahkan waktu ke Listbox
    stopwatch_seconds = 0
    stopwatch_label.configure(text="00:00")

def update_stopwatch():
    global stopwatch_running, stopwatch_seconds
    if stopwatch_running:
        minutes, seconds = divmod(stopwatch_seconds, 60)
        timer_text = "{:02d}:{:02d}".format(minutes, seconds)
        stopwatch_label.configure(text=timer_text)
        stopwatch_seconds += 1
        app.after(1000, update_stopwatch)
        
def delete_time():
    global time_listbox
    selected_time_index = time_listbox.curselection()
    if selected_time_index:
        time_listbox.delete(selected_time_index)


# function for Pomodoro
def start_pomodoro():
    global pomodoro_running, pomodoro_time
    if not pomodoro_running:
        pomodoro_running = True
        update_pomodoro_timer()


def pause_pomodoro():
    global pomodoro_running
    pomodoro_running = False


def stop_pomodoro():
    global pomodoro_running, pomodoro_time
    pomodoro_running = False
    pomodoro_time = 1500
    pomodoro_timer_label.configure(text="25:00")


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

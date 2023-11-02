import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

# Tema warna
colors = {
    "night": {
        "bg": "#1C1C1C",
        "fg": "#F0F0F0",
        "btn": "#5084B9",
        "border": "#1E1E1E",
    },
    "day": {
        "bg": "#A9CCE3",
        "fg": "#1C1C1C",
        "btn": "#5084B9",
        "border": "#5084B9",
    },
}

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("COBAKKK")
        self.root.configure(bg=colors["day"]["bg"])
 
        # Menu Bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
 
        # Menu Tema
        self.theme_menu = tk.Menu(self.menubar, tearoff=0)
        self.theme_menu.add_command(label="Hari", command=lambda: self.set_theme("day"))
        self.theme_menu.add_command(label="Malam", command=lambda: self.set_theme("night"))
        self.menubar.add_cascade(label="Tema", menu=self.theme_menu)

        # Buat ttk.PanedWindow
        self.paned_window = tk.PanedWindow(self.root, orient="horizontal")
        self.paned_window.pack(fill="both", expand=True, padx=8, pady=8)

        # Buat frame untuk menu tombol
        self.menu_frame = tk.Frame(self.paned_window, bg=colors["day"]["bg"])
        self.paned_window.add(self.menu_frame)

        # Buat frame untuk konten fitur
        self.content_frame = tk.Frame(self.paned_window, bg=colors["day"]["bg"])
        self.paned_window.add(self.content_frame)

        # Buat tombol-tombol menu
        self.podomoro_btn = ttk.Button(self.menu_frame, text="Podomoro", command=self.show_podomoro)
        self.podomoro_btn.pack(pady=10, fill="x")

        self.todo_btn = ttk.Button(self.menu_frame, text="To-Do List", command=self.show_todo)
        self.todo_btn.pack(pady=10, fill="x")

        self.stopwatch_btn = ttk.Button(self.menu_frame, text="Stopwatch", command=self.show_stopwatch)
        self.stopwatch_btn.pack(pady=10, fill="x")

        self.timer_btn = ttk.Button(self.menu_frame, text="Timer", command=self.show_timer)
        self.timer_btn.pack(pady=10, fill="x")

        # Inisialisasi frame pertama yang ditampilkan (Pomodoro)
        self.podomoro_frame = tk.Frame(self.content_frame, bg=colors["day"]["bg"])
        self.podomoro_frame.pack(padx=15, pady=15)

        self.timer_frame = tk.Frame(self.content_frame, bg=colors["day"]["bg"])
        self.timer_frame.pack(padx=15, pady=15)

        self.stopwatch_frame = tk.Frame(self.content_frame, bg=colors["day"]["bg"])
        self.stopwatch_frame.pack(padx=15, pady=15)

        self.todo_frame = tk.Frame(self.content_frame, bg=colors["day"]["bg"])
        self.todo_frame.pack(padx=15, pady=15)

        # Pomodoro Frame
        self.podomoro_timer_label = tk.Label(self.podomoro_frame, text="00:00", bg=colors["day"]["bg"], fg=colors["day"]["fg"], font=("Helvetica", 40))
        self.podomoro_timer_label.pack(pady=10)

        
        self.podomoro_label = tk.Label(self.podomoro_frame, text="Podomoro", bg=colors["day"]["bg"], fg=colors["day"]["fg"])
        self.podomoro_label.pack(pady=8)

        self.podomoro_entry = tk.Entry(self.podomoro_frame)
        self.podomoro_entry.pack(pady=5)

        self.podomoro_start_btn = tk.Button(self.podomoro_frame, text="Mulai", command=self.start_pomodoro)
        self.podomoro_start_btn.pack(pady=5)

        self.podomoro_time = 0
        self.podomoro_running = False

        # Timer Frame
        self.timer_label = tk.Label(self.timer_frame, text="Timer", bg=colors["day"]["bg"], fg=colors["day"]["fg"])
        self.timer_label.pack(pady=8)

        self.timer_entry = tk.Entry(self.timer_frame)
        self.timer_entry.pack(pady=5)

        self.timer_start_btn = tk.Button(self.timer_frame, text="Mulai", command=self.start_timer)
        self.timer_start_btn.pack(pady=5)

        self.timer_time = 0

        # Stopwatch Frame
        self.stopwatch_label = tk.Label(self.stopwatch_frame, text="Stopwatch", bg=colors["day"]["bg"], fg=colors["day"]["fg"])
        self.stopwatch_label.pack(pady=8)

        self.stopwatch_start_btn = tk.Button(self.stopwatch_frame, text="Mulai", command=self.start_stopwatch)
        self.stopwatch_start_btn.pack(pady=5)

        self.stopwatch_stop_btn = tk.Button(self.stopwatch_frame, text="Hentikan", command=self.stop_stopwatch)
        self.stopwatch_stop_btn.pack(pady=5)

        self.stopwatch_reset_btn = tk.Button(self.stopwatch_frame, text="Reset", command=self.reset_stopwatch)
        self.stopwatch_reset_btn.pack(pady=5)

        self.stopwatch_start_time = 0
        self.stopwatch_running = False

        # To-Do List Frame
        self.todo_listbox = tk.Listbox(self.todo_frame, bg=colors["day"]["bg"], fg=colors["day"]["fg"])
        self.todo_listbox.pack(pady=5)

        self.todo_entry = tk.Entry(self.todo_frame)
        self.todo_entry.pack(pady=5)

        self.todo_add_btn = tk.Button(self.todo_frame, text="Tambah", command=self.add_todo)
        self.todo_add_btn.pack(pady=5)

        self.todo_remove_btn = tk.Button(self.todo_frame, text="Hapus", command=self.remove_todo)
        self.todo_remove_btn.pack(pady=5)

        self.show_podomoro()

    # Metode show_podomoro, show_todo, show_stopwatch, show_timer, hide_all_content, dan lainnya seperti yang Anda miliki

    def show_podomoro(self):
        self.hide_all_content()
        self.podomoro_frame.pack()

    def show_todo(self):
        self.hide_all_content()
        self.todo_frame.pack()

    def show_stopwatch(self):
        self.hide_all_content()
        self.stopwatch_frame.pack()

    def show_timer(self):
        self.hide_all_content()
        self.timer_frame.pack()

    def hide_all_content(self):
        frames = [self.podomoro_frame, self.todo_frame, self.stopwatch_frame, self.timer_frame]
        for frame in frames:
            if frame:
                frame.pack_forget()

    
    def set_theme(self, theme):
        if theme == "day":
            self.root.configure(bg=colors["day"]["bg"])
            self.podomoro_label.configure(bg=colors["day"]["bg"], fg=colors["day"]["fg"])
            self.timer_label.configure(bg=colors["day"]["bg"], fg=colors["day"]["fg"])
            self.stopwatch_label.configure(bg=colors["day"]["bg"], fg=colors["day"]["fg"])
            self.todo_listbox.configure(bg=colors["day"]["bg"], fg=colors["day"]["fg"])
        elif theme == "night":
            self.root.configure(bg=colors["night"]["bg"])
            self.podomoro_label.configure(bg=colors["night"]["bg"], fg=colors["night"]["fg"])
            self.timer_label.configure(bg=colors["night"]["bg"], fg=colors["night"]["fg"])
            self.stopwatch_label.configure(bg=colors["night"]["bg"], fg=colors["night"]["fg"])
            self.todo_listbox.configure(bg=colors["night"]["bg"], fg=colors["night"]["fg"])

    def start_pomodoro(self):
        try:
            self.podomoro_time = int(self.podomoro_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Entri waktu tidak valid. Silakan masukkan angka.")
            return

        self.podomoro_entry.delete(0, "end")
        self.countdown(self.podomoro_time * 60, self.podomoro_alarm)
        self.update_podomoro_timer()

    def update_podomoro_timer(self):
        minutes, seconds = divmod(self.podomoro_time, 60)
        timer_text = "{:02d}:{:02d}".format(minutes, seconds)
        self.podomoro_timer_label.config(text=timer_text)
        self.podomoro_time -= 1

        if self.podomoro_time >= 0:
            self.root.after(1000, self.update_podomoro_timer)
            
    def podomoro_alarm(self):
        messagebox.showinfo("Pomodoro", "Waktunya istirahat. Bersantailah sebentar.")


    def start_timer(self):
        try:
            self.timer_time = int(self.timer_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Entri waktu tidak valid. Silakan masukkan angka.")
            return

        self.timer_entry.delete(0, "end")
        self.countdown(self.timer_time, self.timer_alarm)

    def timer_alarm(self):
        messagebox.showinfo("Timer", "Waktunya selesai!")

    def start_stopwatch(self):
        self.stopwatch_start_time = time.time()
        self.stopwatch_running = True
        self.update_stopwatch()

    def stop_stopwatch(self):
        self.stopwatch_running = False

    def reset_stopwatch(self):
        self.stopwatch_label.configure(text="00:00:00")

    def update_stopwatch(self):
        if self.stopwatch_running:
            elapsed_time = time.time() - self.stopwatch_start_time
            elapsed_mins, elapsed_secs = divmod(elapsed_time, 60)
            elapsed_hours, elapsed_mins = divmod(elapsed_mins, 60)

            stopwatch_time = ("{:02d}:{:02d}:{:02d}".format(int(elapsed_hours), int(elapsed_mins), int(elapsed_secs)))
            self.stopwatch_label.configure(text=stopwatch_time)

            self.root.after(1000, self.update_stopwatch)

    def add_todo(self):
        todo_item = self.todo_entry.get()
        if todo_item:
            self.todo_listbox.insert("end", todo_item)
            self.todo_entry.delete(0, "end")

    def remove_todo(self):
        selected_item = self.todo_listbox.curselection()
        if selected_item:
            self.todo_listbox.delete(selected_item)

    def countdown(self, remaining_time, alarm_function):
        if remaining_time >= 0:
            hours, minutes = divmod(remaining_time, 60)
            timer_time = ("{:02d}:{:02d}".format(int(hours), int(minutes)))
            self.timer_label.configure(text=timer_time)

            if remaining_time == 0:
                alarm_function()
            else:
                self.root.after(1000, self.countdown, remaining_time - 1, alarm_function)

    def hide_all_content(self):
        for frame in (self.podomoro_frame, self.todo_frame, self.stopwatch_frame, self.timer_frame):
            frame.pack_forget()

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = TimerApp(root)
    app.start()


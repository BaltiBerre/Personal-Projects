import tkinter as tk
from tkinter import filedialog, messagebox
import dp
from datetime import datetime


class EmailAnalysisGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
        self.mbox_file_paths = []
        self.cancel_requested = False

    def cancel_analysis(self):
        self.cancel_requested = True
        self.analyze_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')

    def is_cancel_requested(self):
        return self.cancel_requested


    def create_widgets(self):
        self.choose_mbox_btn = tk.Button(self, text="Choose mbox file(s)", command=self.choose_mbox_files)
        self.choose_mbox_btn.grid(row=0, column=0)

        self.mbox_file_label = tk.Label(self, text="")
        self.mbox_file_label.grid(row=0, column=1)

        self.start_date_label = tk.Label(self, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.grid(row=1, column=0)

        self.start_date_entry = tk.Entry(self)
        self.start_date_entry.grid(row=1, column=1)

        self.end_date_label = tk.Label(self, text="End Date (YYYY-MM-DD):")
        self.end_date_label.grid(row=2, column=0)

        self.end_date_entry = tk.Entry(self)
        self.end_date_entry.grid(row=2, column=1)

        self.keyword_label = tk.Label(self, text="Keyword filter:")
        self.keyword_label.grid(row=3, column=0)

        self.keyword_entry = tk.Entry(self)
        self.keyword_entry.grid(row=3, column=1)

        self.analyze_btn = tk.Button(self, text="Analyze", command=self.analyze)
        self.analyze_btn.grid(row=4, column=0, columnspan=2)

        self.cancel_btn = tk.Button(self, text="Cancel", command=self.cancel_analysis, state='disabled')
        self.cancel_btn.grid(row=5, column=0, columnspan=2)

        self.quit_btn = tk.Button(self, text="Quit", command=self.master.quit)
        self.quit_btn.grid(row=6, column=0, columnspan=2)

    def choose_mbox_files(self):
        self.mbox_file_paths = filedialog.askopenfilenames(filetypes=[("mbox files", "*.mbox")])
        self.mbox_file_label.config(text="; ".join(self.mbox_file_paths))

    def is_valid_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def analyze(self):
        if not self.mbox_file_paths:
            messagebox.showerror("Error", "Please choose at least one mbox file before analyzing.")
            return

        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        keyword = self.keyword_entry.get()

        if start_date and not self.is_valid_date(start_date):
            messagebox.showerror("Error", "Invalid start date format. Please use YYYY-MM-DD.")
            return

        if end_date and not self.is_valid_date(end_date):
            messagebox.showerror("Error", "Invalid end date format. Please use YYYY-MM-DD.")
            return

        start_date_dt = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date_dt = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

        self.analyze_btn.config(state='disabled')
        self.cancel_btn.config(state='normal')

        dp.analyze_email(mbox_files=self.mbox_file_paths, start_date=start_date_dt, end_date=end_date_dt, keyword=keyword, cancel_callback=self.is_cancel_requested)

        self.analyze_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')

    def cancel_analysis(self):
        dp.cancel_analysis()
        self.analyze_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')


def run_gui():
    root = tk.Tk()
    root.title("Email Analysis GUI")
    app = EmailAnalysisGUI(master=root)
    app.mainloop()


if __name__ == "__main__":
    run_gui()


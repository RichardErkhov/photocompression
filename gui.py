#simplt gui for archiver
import tkinter as tk
import threading
import time
import main as archiver
from tkinter import messagebox


def interface():
    root = tk.Tk()
    root.title("Archiver")
    root.geometry("300x500")
    root.resizable(False, False)
    root.configure(background='#f0f0f0')
    Title = tk.Label(root, text="Archiver", font=("Helvetica", 16), bg='#f0f0f0')
    Title.pack(pady=10)
    input_folder = tk.StringVar()
    input_folder.set("Input Folder")
    input_folder_label = tk.Label(root, textvariable=input_folder, bg='#f0f0f0')
    input_folder_label.pack(pady=10)
    input_folder_entry = tk.Entry(root, width=30)
    input_folder_entry.pack(pady=10)
    output_folder = tk.StringVar()
    output_folder.set("Output Folder")
    output_folder_label = tk.Label(root, textvariable=output_folder, bg='#f0f0f0')
    output_folder_label.pack(pady=10)
    output_folder_entry = tk.Entry(root, width=30)
    output_folder_entry.pack(pady=10)
    password = tk.StringVar()
    password.set("Password")
    password_label = tk.Label(root, textvariable=password, bg='#f0f0f0')
    password_label.pack(pady=10)
    password_entry = tk.Entry(root, width=30)
    password_entry.pack(pady=10)
    archive_name = tk.StringVar()
    archive_name.set("Archive Name")
    archive_name_label = tk.Label(root, textvariable=archive_name, bg='#f0f0f0')
    archive_name_label.pack(pady=10)
    archive_name_entry = tk.Entry(root, width=30)
    archive_name_entry.pack(pady=10)
    kmeans_check = tk.IntVar()
    kmeans_check.set(0)
    kmeans_check_button = tk.Checkbutton(root, text="K-Means", variable=kmeans_check, bg='#f0f0f0')
    kmeans_check_button.pack(pady=10)
    make_archive_button = tk.Button(root, text="Make Archive", command=lambda: archiver.make_archive(archive_name_entry.get(), input_folder_entry.get(), password_entry.get(), output_folder_entry.get(), kmeans_check.get()), bg='#f0f0f0')
    make_archive_button.pack(pady=10)
    open_archive_button = tk.Button(root, text="Open Archive", command=lambda: archiver.open_archive(archive_name_entry.get(), output_folder_entry.get(), password_entry.get()))
    open_archive_button.pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    interface()

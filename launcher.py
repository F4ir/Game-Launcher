# GameLauncher was proudly coded by F4ir

import os
import subprocess
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, font
import win32com.client  # Requires `pywin32` package for working with shortcuts

# Directory containing the game executables and shortcuts
GAMES_DIR = os.path.join(os.getcwd(), 'gamefiles')

# Function to launch the selected game or URL
def launch_game():
    selected_game = listbox.get(tk.ACTIVE)
    if selected_game:
        game_path = os.path.join(GAMES_DIR, selected_game)
        if os.path.isfile(game_path):
            if selected_game.endswith('.lnk'):
                try:
                    shell = win32com.client.Dispatch('WScript.Shell')
                    shortcut = shell.CreateShortCut(game_path)
                    game_path = shortcut.TargetPath
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to resolve shortcut: {e}")
                    return
            elif selected_game.endswith('.url'):
                try:
                    with open(game_path, 'r') as url_file:
                        for line in url_file:
                            if line.startswith("URL="):
                                game_path = line.strip().split("=", 1)[1]
                                break
                    subprocess.Popen(['start', '', game_path], shell=True)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to read URL file: {e}")
                    return
            
            try:
                subprocess.Popen(game_path, shell=True)
            except FileNotFoundError:
                messagebox.showerror("Error", "Game executable or URL not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch game: {e}")
        else:
            messagebox.showwarning("Warning", "Selected game file does not exist.")
    else:
        messagebox.showwarning("Warning", "Please select a game to launch.")

# Function to load game executables and shortcuts into the listbox
def load_games():
    if os.path.exists(GAMES_DIR):
        for filename in os.listdir(GAMES_DIR):
            if filename.endswith('.exe') or filename.endswith('.lnk') or filename.endswith('.url'):
                listbox.insert(tk.END, filename)
    else:
        messagebox.showerror("Error", "Game files directory does not exist.")

# GUI setup
root = tk.Tk()
root.title("Game Launcher")
root.geometry("480x500")  # Adjusted window size
root.configure(bg='#2e2e2e')

# Center the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (480 // 2)
y = (screen_height // 2) - (500 // 2)
root.geometry(f"480x500+{x}+{y}")

# Set custom icon
icon_path = os.path.join(os.getcwd(), 'Other', 'LauncherImage.ico')
root.iconbitmap(icon_path)

# Custom font
custom_font = font.Font(family="Helvetica", size=12)

# Title label
title_label = tk.Label(root, text="Select Your Added Game to Launch", bg='#2e2e2e', fg='white', font=("Helvetica", 16))
title_label.pack(pady=(10, 0))

# Frame for the listbox
frame = tk.Frame(root, bg='#3e3e3e', padx=20, pady=20, bd=2, relief=tk.RAISED)
frame.pack(pady=10, padx=10)

# Scrollbar for the listbox
scrollbar = Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Listbox for game selection with improved styling
listbox = Listbox(frame, width=50, height=10, yscrollcommand=scrollbar.set, 
                  bg='#2e2e2e', fg='white', selectbackground='#5e5e5e', 
                  selectforeground='black', font=custom_font, bd=0, relief=tk.FLAT)
listbox.pack(padx=10, pady=10)
scrollbar.config(command=listbox.yview)

# Launch button with styling
button_launch = tk.Button(root, text="Launch Game", command=launch_game, 
                          bg='#4e4e4e', fg='white', font=custom_font, 
                          relief=tk.RAISED, bd=2, padx=10, pady=5)
button_launch.pack(pady=10)

# Hover effect for button
def on_enter(event):
    event.widget['bg'] = '#5e5e5e'

def on_leave(event):
    event.widget['bg'] = '#4e4e4e'

button_launch.bind("<Enter>", on_enter)
button_launch.bind("<Leave>", on_leave)

# Add a footer label
footer_label = tk.Label(root, text="Game Launcher by F4ir", bg='#2e2e2e', fg='white', font=("Helvetica", 10))
footer_label.pack(side=tk.BOTTOM, pady=10)

# Load games when the program starts
load_games()

root.mainloop()

# GameLauncher was proudly coded by F4ir

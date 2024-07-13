# GameLauncher was proudly coded by F4ir

import os
import subprocess
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, font
import json
import webbrowser
import win32com.client  # Requires `pywin32` package for working with shortcuts

# Directory containing the game executables and shortcuts
GAMES_DIR = os.path.join(os.getcwd(), 'gamefiles')
OTHER_DIR = os.path.join(os.getcwd(), 'Other')
RECENTLY_PLAYED_FILE = os.path.join(OTHER_DIR, 'recentlyplayed.json')

# Load recently played games from JSON files
if os.path.exists(RECENTLY_PLAYED_FILE):
    with open(RECENTLY_PLAYED_FILE, 'r') as file:
        recently_played = json.load(file)
else:
    recently_played = []

# Function to save recently played games to JSON file
def save_recently_played():
    with open(RECENTLY_PLAYED_FILE, 'w') as file:
        json.dump(recently_played, file)

# Function to launch the selected game or URL
def launch_game():
    selected_game_index = listbox.curselection()
    if selected_game_index:
        selected_game = listbox.get(selected_game_index).strip()
        if selected_game not in ["Recently Played:", "All Games:"]:
            game_path = os.path.join(GAMES_DIR, selected_game + get_file_extension(selected_game))
            if os.path.isfile(game_path):
                if selected_game in recently_played:
                    recently_played.remove(selected_game)

                # Insert the selected game at the start
                recently_played.insert(0, selected_game)

                # Limit to 3 recently played games
                if len(recently_played) > 3:
                    recently_played.pop()  # Remove the oldest game

                save_recently_played()
                load_games()

                if game_path.endswith('.lnk'):
                    try:
                        shell = win32com.client.Dispatch('WScript.Shell')
                        shortcut = shell.CreateShortCut(game_path)
                        game_path = shortcut.TargetPath
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to resolve shortcut: {e}")
                        return
                elif game_path.endswith('.url'):
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
    listbox.delete(0, tk.END)

    # Load recently played games
    if recently_played:
        listbox.insert(tk.END, "--------------------------Recently Played--------------------------")
        for game in recently_played:
            listbox.insert(tk.END, game)

    # Load all games
    if os.path.exists(GAMES_DIR):
        listbox.insert(tk.END, "------------------------------All Games------------------------------")
        for filename in os.listdir(GAMES_DIR):
            if filename.endswith('.exe') or filename.endswith('.lnk') or filename.endswith('.url'):
                game_name = os.path.splitext(filename)[0]
                if game_name not in recently_played:
                    listbox.insert(tk.END, game_name)
    else:
        messagebox.showerror("Error", "Game files directory does not exist.")

def get_file_extension(game_name):
    """Get the file extension based on the game name."""
    for filename in os.listdir(GAMES_DIR):
        if os.path.splitext(filename)[0] == game_name:
            return os.path.splitext(filename)[1]
    return ""

# Function to search games
def search_games():
    search_query = search_entry.get().lower()
    listbox.delete(0, tk.END)

    # Load recently played games
    if recently_played:
        for game in recently_played:
            if search_query in game.lower():
                listbox.insert(tk.END, game)

    # Load all games
    if os.path.exists(GAMES_DIR):
        for filename in os.listdir(GAMES_DIR):
            if filename.endswith('.exe') or filename.endswith('.lnk') or filename.endswith('.url'):
                game_name = os.path.splitext(filename)[0]
                if search_query in game_name.lower() and game_name not in recently_played:
                    listbox.insert(tk.END, game_name)

# Function to handle the Enter key press
def on_enter_key(event):
    search_games()

# Function to open GitHub link
def open_github():
    webbrowser.open("https://github.com/F4ir")

# Function to refresh games
def refresh_games():
    load_games()

# GUI setup
root = tk.Tk()
root.title("Game Launcher")
root.geometry("480x500")
root.configure(bg='#2e2e2e')

# Set custom icon for both window and taskbar
icon_path = os.path.join(os.getcwd(), 'Other', 'LauncherImage.ico')
root.iconbitmap(icon_path)

# Center the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (480 // 2)
y = (screen_height // 2) - (500 // 2)
root.geometry(f"480x500+{x}+{y}")

# Custom font
custom_font = font.Font(family="Helvetica", size=12)

# Title label
title_label = tk.Label(root, text="Select Your Added Game to Launch", bg='#2e2e2e', fg='white', font=("Helvetica", 16))
title_label.pack(pady=(10, 0))

# Add a frame for the search bar and button
search_frame = tk.Frame(root, bg='#2e2e2e')
search_frame.pack(pady=(10, 0))

# Add a search bar
search_entry = tk.Entry(search_frame, font=custom_font, bg='#3e3e3e', fg='white', bd=1, relief=tk.SOLID, width=25)  # Adjusted width
search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
search_entry.bind("<Return>", on_enter_key)

# Add a search button
search_button = tk.Button(search_frame, text="Search", command=search_games, bg='#4e4e4e', fg='white', font=custom_font, relief=tk.RAISED, bd=2, width=10)  # Adjusted width
search_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Load the Refresh image and resize it
refresh_image_path = os.path.join(OTHER_DIR, 'Refresh.png')
refresh_image = tk.PhotoImage(file=refresh_image_path)
refresh_image = refresh_image.subsample(20)  # Adjusted subsample value for a slightly larger size

# Add refresh button next to the search bar
refresh_button = tk.Button(search_frame, image=refresh_image, command=refresh_games, bd=0, bg='#2e2e2e', activebackground='#2e2e2e')
refresh_button.pack(side=tk.LEFT, padx=(5, 0))

# Frame for the listbox
frame = tk.Frame(root, bg='#3e3e3e', padx=20, pady=20, bd=2, relief=tk.RAISED)
frame.pack(pady=10, padx=10)

# Scrollbar for the listbox
scrollbar = Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Listbox for game selection with improved styling
listbox = Listbox(frame, width=50, height=12, yscrollcommand=scrollbar.set, 
                  bg='#2e2e2e', fg='white', selectbackground='#A9A9A9', 
                  selectforeground='black', font=custom_font, bd=0, relief=tk.FLAT)
listbox.pack(padx=10, pady=10)
scrollbar.config(command=listbox.yview)

# Launch button with styling
button_launch = tk.Button(root, text="Launch Game", command=launch_game, 
                          bg='#4e4e4e', fg='white', font=custom_font, 
                          relief=tk.RAISED, bd=2, padx=10, pady=5)
button_launch.pack(pady=(20, 10))

# Hover effect for button
def on_enter(event):
    event.widget['bg'] = '#5e5e5e'

def on_leave(event):
    event.widget['bg'] = '#4e4e4e'

button_launch.bind("<Enter>", on_enter)
button_launch.bind("<Leave>", on_leave)

# Add a footer label
footer_label = tk.Label(root, text="Game Launcher by F4ir", bg='#2e2e2e', fg='white', font=("Helvetica", 10))
footer_label.pack(side=tk.TOP, pady=10)

# Load the GitHub image and resize it
github_image_path = os.path.join(OTHER_DIR, 'Github.png')
github_image = tk.PhotoImage(file=github_image_path)
github_image = github_image.subsample(20)  # Resize image to a smaller size

# Add GitHub image button in the bottom left corner
github_button = tk.Button(root, image=github_image, command=open_github, bd=0, bg='#2e2e2e', activebackground='#2e2e2e')
github_button.place(x=10, y=460)

# Load games when the program starts
load_games()

root.mainloop()

# GameLauncher was proudly coded by F4ir

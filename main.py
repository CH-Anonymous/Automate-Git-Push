import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from utils import (
    push_to_github,
    create_github_repo,
    delete_github_repo,
    list_github_repos,
    update_repo_remote,
    save_token,
    load_token,
    reset_token
)

# ==== THEME COLORS ====
BG_COLOR = "#e6f0ff"        # Background
BTN_COLOR = "#007bff"       # Blue Buttons
BTN_TEXT_COLOR = "#ffffff"  # White text
TEXT_COLOR = "#001f3f"      # Dark navy
ENTRY_BG = "#d0f0c0"        # Eye-catching mint green

# ==== ROOT WINDOW ====
root = tk.Tk()
root.title("AutoGitPush Pro")
root.geometry("650x500")
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.configure("TNotebook", background=BG_COLOR)
style.configure("TNotebook.Tab", padding=[10, 5])
style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"))

username_var = tk.StringVar()
token_var = tk.StringVar()

notebook = ttk.Notebook(root)

# ==== GUI INIT ====
def init_gui():
    notebook.pack(expand=True, fill='both', padx=10, pady=10)
    setup_push_tab()
    setup_delete_tab()
    setup_update_tab()
    setup_settings_tab()
    root.update()

# ==== FIRST TIME LOGIN ====
def first_time_prompt():
    popup = tk.Toplevel()
    popup.title("GitHub Login Required")
    popup.geometry("400x200")
    popup.grab_set()
    popup.configure(bg=BG_COLOR)

    tk.Label(popup, text="GitHub Username:", bg=BG_COLOR).pack(pady=5)
    temp_username = tk.StringVar()
    tk.Entry(popup, textvariable=temp_username, width=40, bg=ENTRY_BG).pack()

    tk.Label(popup, text="GitHub Token:", bg=BG_COLOR).pack(pady=5)
    temp_token = tk.StringVar()
    tk.Entry(popup, textvariable=temp_token, show='*', width=40, bg=ENTRY_BG).pack()

    def save_and_start():
        if not temp_username.get() or not temp_token.get():
            messagebox.showerror("Missing", "Enter both username and token")
            return
        username_var.set(temp_username.get())
        token_var.set(temp_token.get())
        save_token(temp_username.get(), temp_token.get())
        popup.destroy()
        init_gui()

    tk.Button(popup, text="Login", command=save_and_start, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=15)

def load_saved_credentials():
    u, t = load_token()
    if u and t:
        username_var.set(u)
        token_var.set(t)
        init_gui()
    else:
        first_time_prompt()

# ==== PUSH TAB ====
def setup_push_tab():
    push_tab = ttk.Frame(notebook)
    notebook.add(push_tab, text='Push Code')

    repo_name_push = tk.StringVar()
    repo_desc_push = tk.StringVar()
    folder_push = tk.StringVar()

    def browse_push():
        folder_push.set(filedialog.askdirectory())

    def do_push():
        if not repo_name_push.get() or not folder_push.get():
            messagebox.showwarning("Missing", "Please fill all fields.")
            return

        created, msg = create_github_repo(
            repo_name_push.get(),
            username_var.get(),
            token_var.get(),
            repo_desc_push.get()
        )
        messagebox.showinfo("Repo Check", msg)

        success, info = push_to_github(folder_push.get(), username_var.get(), repo_name_push.get(), token_var.get())
        if success:
            messagebox.showinfo("Success", info)
        else:
            messagebox.showerror("Failed", info)

    ttk.Label(push_tab, text="Repository Name:").pack(pady=5)
    tk.Entry(push_tab, textvariable=repo_name_push, width=50, bg=ENTRY_BG, fg=TEXT_COLOR).pack()

    ttk.Label(push_tab, text="Repository Description (optional):").pack(pady=5)
    tk.Entry(push_tab, textvariable=repo_desc_push, width=50, bg=ENTRY_BG, fg=TEXT_COLOR).pack()

    ttk.Label(push_tab, text="Folder to Push:").pack(pady=5)
    tk.Entry(push_tab, textvariable=folder_push, width=50, bg=ENTRY_BG, fg=TEXT_COLOR).pack()
    tk.Button(push_tab, text="Browse", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=browse_push).pack(pady=5)
    tk.Button(push_tab, text="Push to GitHub", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=do_push).pack(pady=10)

# ==== DELETE TAB ====
def setup_delete_tab():
    delete_tab = ttk.Frame(notebook)
    notebook.add(delete_tab, text='Delete Repo')

    repo_listbox = tk.Listbox(delete_tab, height=10, width=50, bg=ENTRY_BG, fg=TEXT_COLOR)
    repo_listbox.pack()

    def refresh_repo_list():
        repo_listbox.delete(0, tk.END)
        for name in list_github_repos(token_var.get()):
            repo_listbox.insert(tk.END, name)

    def do_delete():
        selected = repo_listbox.get(tk.ACTIVE)
        if not selected:
            messagebox.showwarning("Select", "Select a repo to delete.")
            return
        if delete_github_repo(selected, token_var.get()):
            messagebox.showinfo("Deleted", f"{selected} deleted.")
            refresh_repo_list()
        else:
            messagebox.showerror("Error", "Failed to delete repo.")

    tk.Button(delete_tab, text="Refresh List", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=refresh_repo_list).pack(pady=5)
    tk.Button(delete_tab, text="Delete Selected", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=do_delete).pack(pady=10)

# ==== UPDATE TAB ====
def setup_update_tab():
    update_tab = ttk.Frame(notebook)
    notebook.add(update_tab, text='Update Repo')

    repo_listbox_update = tk.Listbox(update_tab, height=10, width=50, bg=ENTRY_BG, fg=TEXT_COLOR)
    repo_listbox_update.pack()

    repo_name_update = tk.StringVar()
    folder_update = tk.StringVar()

    def browse_update():
        folder_update.set(filedialog.askdirectory())

    def refresh_update_repo_list():
        repo_listbox_update.delete(0, tk.END)
        for name in list_github_repos(token_var.get()):
            repo_listbox_update.insert(tk.END, name)

    def do_update_remote():
        selected = repo_listbox_update.get(tk.ACTIVE)
        if not selected or not folder_update.get():
            messagebox.showerror("Missing", "Please select repo and folder.")
            return
        repo_name_update.set(selected)
        success, msg = update_repo_remote(folder_update.get(), username_var.get(), selected, token_var.get())
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def do_update_push():
        selected = repo_listbox_update.get(tk.ACTIVE)
        if not selected or not folder_update.get():
            messagebox.showerror("Missing", "Please select repo and folder.")
            return
        repo_name_update.set(selected)
        success, msg = push_to_github(folder_update.get(), username_var.get(), selected, token_var.get())
        if success:
            messagebox.showinfo("Pushed", msg)
        else:
            messagebox.showerror("Failed", msg)

    tk.Button(update_tab, text="Refresh Repo List", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=refresh_update_repo_list).pack(pady=5)

    ttk.Label(update_tab, text="Folder to Push:").pack(pady=5)
    tk.Entry(update_tab, textvariable=folder_update, width=50, bg=ENTRY_BG, fg=TEXT_COLOR).pack()
    tk.Button(update_tab, text="Browse", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=browse_update).pack(pady=5)

    tk.Button(update_tab, text="Update Remote", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=do_update_remote).pack(pady=5)
    tk.Button(update_tab, text="Push All Changes", bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=do_update_push).pack(pady=5)

# ==== SETTINGS TAB ====
def setup_settings_tab():
    settings_tab = ttk.Frame(notebook)
    notebook.add(settings_tab, text='Settings')

    ttk.Label(settings_tab, text="GitHub Username").pack()
    username_entry = tk.Entry(settings_tab, textvariable=username_var, width=50, bg=ENTRY_BG, fg=TEXT_COLOR)
    username_entry.pack()
    username_entry.config(state='disabled')

    ttk.Label(settings_tab, text="GitHub Token").pack()
    token_entry = tk.Entry(settings_tab, textvariable=token_var, show='*', width=50, bg=ENTRY_BG, fg=TEXT_COLOR)
    token_entry.pack()
    token_entry.config(state='disabled')

    tk.Button(settings_tab, text="Reset Token", bg="#cc4c4c", fg=BTN_TEXT_COLOR,
              command=lambda: reset_token() or messagebox.showinfo("Reset", "Token removed. Restart app.")).pack(pady=10)

# ==== RUN APP ====
load_saved_credentials()
root.mainloop()
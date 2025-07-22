# 🚀 AutoGitPush Pro
![GitHub release (latest by date)](https://img.shields.io/github/v/release/CH-Anonymous/anti-keylogger-scanner)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Made with Python](https://img.shields.io/badge/made%20with-Python-3776AB?logo=python&logoColor=white)

**AutoGitPush Pro** is a desktop application built with Python and Tkinter that allows you to **automatically push your local project folders to GitHub**. It simplifies Git operations and repository management through a clean, modern GUI.

---

## 🎯 Features

- 🔐 **One-time GitHub token authentication** (securely stored)
- 📂 **Push any local folder** to GitHub with a click
- 🔁 **Update existing repositories** easily
- 🗑️ **Delete GitHub repositories** from the app
- 📃 **View all your GitHub repositories**
- 📦 Auto `.gitignore` support (optional)
- 🎨 **Modern GUI** with attractive colors and user-friendly layout
- 💾 Saves GitHub credentials securely for reuse

---

## 💻 Technologies Used

- Python 🐍
- Tkinter 🎨
- GitPython 🧠
- PyGithub 🌐

---

## 🔧 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
````

Your `requirements.txt` should include:

```
tk
gitpython
PyGithub
```

---

## 🚀 How to Use

### 1. Run the App

```bash
python main.py
```

### 2. Set Up Your GitHub Token

* Enter your GitHub **username** and **token**
* Click **Save Token**
* This token will be reused automatically next time

### 3. Use the Tabs:

#### 🔹 Push Code Tab

* Choose a folder
* Enter a repo name
* Push to GitHub

#### 🔹 Update Repo Tab

* Select an existing repo from the list
* Browse a folder
* Push updates to that repo

#### 🔹 Delete Repo Tab

* Select a repo
* Click **Delete**

#### 🔹 Settings Tab

* Save/Reset token

---

## 📂 Project Structure

```
AutoGitPush-Pro/
├── main.py                  # Main GUI file
├── utils.py                 # GitHub + Git functions
├── README.md                # This file
├── .gitignore               # Ignore sensitive/log files
└── requirements.txt         # Pip requirements

```

---

## 🔒 Security

* Your token is stored **locally in a JSON file**
* You can reset it any time from the **Settings** tab
* No tokens are exposed or transmitted elsewhere

---

## 📄 License

This project is open-source under the MIT License.
Feel free to fork, modify, and use it in your own projects.

---

## 🙌 Author

**Chirag Khatri**
*“Automate your Git game with a click!”*

[GitHub](https://github.com/CH-Anonymous)
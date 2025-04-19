# 🧠 Python AI Toolkit (Local, Offline-Capable)
 
 > ⚠️ Ollama currently supports macOS, Windows (via WSL2), and Linux. Mobile platforms are not supported.
 
 
 This project is a suite of AI-powered educational tools that run locally using **Ollama** and the **phi-2** model. It includes:
 
 - ✅ AI Study Timer (with motivational quotes)
 - ✅ Flashcard Generator
 - ✅ Grammar Checker
 - ✅ Quiz Maker
 - ✅ AI Concept Explainer
 
 All tools are accessed from a single launcher (`main.py`) and run through a user-friendly GUI built with Tkinter. No internet or API keys required.
 
 ---
 
 ## 🚀 How to Run This Project
 
 ### 1. ✅ Install Python
 
 Download and install Python 3.9 or higher:  
 🔗 https://www.python.org/downloads
 
 After installing, verify Python is available:
 
 ```bash
 python --version
 ```
 
 If that doesn’t work, try:
 
 ```bash
 python3 --version
 ```
 
 ---
 
 ### 2. 🧠 Install Ollama and the phi-2 Model
 
 Download Ollama from:  
 🔗 https://ollama.com
 
 Install it like any normal app, then **launch Ollama** — it must be running in the background.
 
 Open a terminal (Command Prompt, Terminal, or PyCharm's terminal) and run:
 
 ```bash
 ollama pull phi
 ```
 
 This will download and start the local AI model. **Keep this terminal open** while using the app.
 
 ---
 
 ### 3. 📦 Install Python Dependencies
 
 In your project folder, open a terminal and run:
 
 ```bash
 pip install -r requirements.txt
 ```
 
 If that fails, try:
 
 ```bash
 python3 -m pip install -r requirements.txt
 ```
 > 🐧 Linux Users: If you get an error about tkinter, run:
 > ```bash
 > sudo apt install python3-tk
 > ```
 
 # MAC USERS
 To open terminal in the folder:
 ## Option 1: Use Finder
 Open Finder and navigate to the folder.
 
 Right-click (or Control + Click) inside the folder.
 
 Select "New Terminal at Folder".
 
 ## Option 2: Use Terminal Manually
 Open Terminal (search "Terminal" in Spotlight).
 
 Use cd to navigate to your folder
 
 ```bash
 cd ~/Desktop/YourFolderName
 ```
 
 # WINDOW USERS
 To open terminal in the folder:
 ## Option 1: Use File Explorer
 Open File Explorer and navigate to your project folder.
 
 Click the address bar, type cmd, and hit Enter.
 → This opens Command Prompt in that folder.
 
 Or, if you have Windows Terminal installed:
 
 Right-click in the folder while holding Shift, and choose “Open PowerShell window here” or “Open in Terminal”.
 
 ## Option 2: Use Command Prompt Manually
 Open Command Prompt (search "cmd").
 
 Use cd to go to your project folder:
 
 ```cd
 C:\Users\YourName\Desktop\YourFolderName
 ```
 
 ---
 
 ### 4. ▶️ Launch the Toolkit
 
 To start the application:
 
 ```bash
 python main.py
 ```
 
 Or on some systems:
 
 ```bash
 python3 main.py
 ```
 
 ---
 
 ## 📁 Project Contents
 
 | File Name              | Description                                     |
 |------------------------|-------------------------------------------------|
 | `main.py`              | Launcher script that opens all AI tools         |
 | `ai_timer.py`          | AI Study Timer with motivational quotes         |
 | `flashcards.py`        | Flashcard generator based on input text         |
 | `concept_explainer.py` | Concept breakdown with analogies + steps        |
 | `requirements.txt`     | All Third-Party Python packages required to run |
 | `README.md`            | Project overview and setup instructions         |
 
 ---
 
 ## 🧠 AI Model Info
 
 This project uses:
 
 - **Model**: `phi-2`
 - **Runs via**: Ollama
 - **Offline**: ✅ Yes
 - **Free**: ✅ Yes
 - **Fast**: ✅ Runs fully local, no internet needed
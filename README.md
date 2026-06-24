# 🚀 Week 1 Project: The Mystery of Disappearing Data!

Welcome to my Week 1 project for my coding challenge! 

## 📖 The Story Behind This Project

When I first started building a simple notes app, I kept running into a huge problem. Every time I closed the program or refreshed the page, all my notes completely disappeared! I knew how to write the code to make the app work, but I didn't understand where my data was actually going.

I finally figured it out by learning about **data persistence** and Python file handling. I built a simple backend that takes my notes and saves them directly into a text file on my hard drive. Now, instead of keeping the notes in temporary memory (RAM), my app reads them from the saved file. Even if I close the app a hundred times, my notes are still there!

This taught me something huge: Code isn't just magic on a screen. It's actually a set of instructions moving data around inside the computer—from short-term memory (which gets wiped) to long-term storage (which stays safe). Understanding how that works completely changed how I look at software.

## 💻 Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** Vanilla HTML, CSS, JavaScript
- **Core Concept:** Data Persistence (File handling)

## 🚀 How to Run the App

1. **Install Requirements:**
   Make sure you have Python installed, then install the backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Start the Backend Server:**
   Run the FastAPI server from the root directory:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

3. **Open the Frontend:**
   Simply open `frontend/index.html` in your favorite web browser! You don't need a frontend server for this, it runs perfectly as a static file.

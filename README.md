# 🕰️ Time Traveller Game

**Guess the year associated with key facts pulled live from Wikipedia!**

## 🎮 Game Description

Think you know history? Put your knowledge to the test in **Time Traveller**!

You're given a famous event — your challenge is to guess the year it happened. Get instant feedback after each guess: were you too early, too late, or spot on?

💡 Learn new facts, improve your memory, and compete for the highest score.  
Perfect for history buffs, trivia fans, or anyone who loves a challenge!

---

## 📜 Game Rules

- Choose the number of rounds (1 to 3)
- Each player selects a category:
  - Sports  
  - History  
  - Famous People  
  - Music Releases  
  - Movies  
  - Random  
- The player receives a question and must guess the year
- Input must be a full year (e.g., `1945`), or negative for BC (e.g., `-753`)
- The system provides a Wikipedia article with the correct answer

---

## 🧠 Scoring System

| Accuracy       | Points |
|----------------|--------|
| Exact year     | 100    |
| Within 10 yrs  | 50     |
| Within 50 yrs  | 20     |
| Otherwise      | 0      |

---

## 🛠️ Features

- Live data pulled from **Wikipedia API**
- Expandable question categories in `categories.py`
- Colorful terminal UI with `colorama`
- Test script to verify Wikipedia connection
- Supports multiple players and rounds

---

## Made with ❤️ by:
- Christin - https://github.com/chrissy-tech
- Constantin - 
- Sandra  - 
- Greg - https://github.com/gregorydearing 

---

## 📦 Installation

```bash
git clone https://github.com/franciscoxhernandez/time-traveller-game.git
cd time-traveller-game
pip install -r requirements.txt
python game/main.py


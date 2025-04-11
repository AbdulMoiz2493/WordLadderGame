# Word Ladder Game 🧩

A console-based Python implementation of the classic **Word Ladder** game. Transform a start word into an end word by changing one letter at a time, ensuring each intermediate word is valid!

## 📌 Introduction

The **Word Ladder Adventure Game** challenges players to convert one word into another through a series of valid intermediary words. The game supports various difficulty levels and includes AI-powered hints, leveraging three search algorithms to identify the best transformation paths.

## 📌 Features

- User-defined word length and dictionary.
- Automatically generates word ladders.
- Validates word transformations.
- Simple and interactive CLI-based game.
- AI-powered tip system using BFS, UCS, and A*.
- Multiple game modes and difficulty levels.

## 🧠 How It Works

Given a start and end word of equal length, the game finds the shortest transformation sequence where each word differs by one letter from the last.

Example:
```
hit → hot → dot → dog → cog
```

### Graph Representation:
- Words = nodes
- One-letter difference = edges
- A preloaded dictionary ensures all intermediate words are valid

## 🎓 Game Modes & Difficulty Levels

### 🏋️ Beginner Mode
- Short word ladders.
- Simple transformations like "cat" → "big"

### 💡 Advanced Mode
- Longer transformations like "stone" → "money"
- Requires strategic thinking and planning

### ⚡ Challenge Mode
- Introduces obstacles:
  - Banned words
  - Restricted letters
  - Limited number of moves
- Offers a dynamic and more challenging gameplay experience

## 🤖 AI Search Algorithms Implemented

### ● Breadth-First Search (BFS)
- Explores all possibilities at current depth first
- Finds the shortest path (in number of moves)
- Effective on unweighted graphs

### ● Uniform Cost Search (UCS)
- Uses priority queue to explore lowest-cost nodes
- Accounts for transformation costs (e.g., punishing rare words)
- Finds the optimal path, though slower than BFS

### ● A* Search Algorithm
- Uses f(n) = g(n) + h(n)
  - g(n): steps from start
  - h(n): estimated steps to goal (e.g., Hamming distance)
- Efficient and accurate; combines benefits of BFS and UCS

## ⚡ Challenges Faced

### ✔ Dictionary and Word Validation
- Difficult to ensure all transitions are valid
- Solved by preloading and verifying against a dictionary

### ✔ Performance Optimization
- Searching large dictionaries is resource-intensive
- Used priority queues to optimize UCS and A* algorithms

### ✔ Game Interface & User Experience
- Built an interactive CLI experience
- Balanced manual vs AI-assisted gameplay
- Potential to expand with visual transformation graphs

## 💠 Requirements

- Python 3.6 or above
- No external libraries required

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/AbdulMoiz2493/WordLadderGame.git
   cd WordLadderGame
   ```

2. Run the game:
   ```bash
   python Word-Ladder-Game.py
   ```

## 📄 File Structure

- `.py`: Main Python script with all game logic.

## 📧 Contact

For any queries or suggestions:

- 📧 Email: [abdulmoiz8895@gmail.com](mailto:abdulmoiz8895@gmail.com)
- 💙 GitHub: [AbdulMoiz2493](https://github.com/AbdulMoiz2493)

---

Made with ❤️ by Abdul Moiz


# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** A number guessing game where the player tries to guess a secret number within a limited number of attempts. The difficulty setting controls the range and how many guesses you get.

- [x] **Bugs found:**
  - Hints were swapped — "Too High" said "Go HIGHER!" and "Too Low" said "Go LOWER!"
  - Secret was cast to a string on even attempts, breaking numeric comparison
  - Attempt counter started at 1 instead of 0, so the first guess was counted as attempt 2
  - Info text always showed "1 to 100" regardless of difficulty
  - New Game button didn't reset status or history, so the game stayed locked after winning or losing
  - Difficulty ranges were wrong — Hard (1–50) was easier than Normal (1–100)
  - Attempt limits were wrong — Normal (8) allowed more guesses than Easy (6)
  - New game always generated a secret from 1–100, ignoring the selected difficulty

- [x] **Fixes applied:**
  - Corrected the hint messages in check_guess
  - Removed the string conversion of the secret — always compare as integers
  - Initialized attempts to 0
  - Updated the info text to use the actual low and high values
  - Added status = "playing" and history = [] resets to the New Game handler
  - Set correct ranges: Easy (1–10), Normal (1–50), Hard (1–100)
  - Set correct attempt limits: Easy (10), Normal (7), Hard (5)
  - Moved all logic into logic_utils.py and wrote pytest tests for every fix

## 📸 Demo Walkthrough

1. User guesses 25 → "Too Low — Go HIGHER!"
2. User guesses 40 → "Too High — Go LOWER!"
3. User guesses 32 → "Correct!" Score updates and confetti plays
4. Game ends and displays the final score
5. User clicks New Game → session resets, fresh secret picked within the difficulty range

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

collected 38 items                                                               

tests\test_game_logic.py ......................................            [100%]

============================== 38 passed in 0.11s ===============================

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

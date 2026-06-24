# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
- What did the game look like the first time you ran it?
  It looked like a guessing number game and gived you hint if needed.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
    - The difficulty range for hard is backwards
    - The guess responsie is opposite, high when low and vice-versa

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Select "Hard" | Range harder than Normal (e.g. 1–200) | Range is 1–50, easier than Normal's 1–100 | No error; wrong range in sidebar |
| Type "abc", click Submit | Invalid input should not use an attempt | Attempt counter still increments | error - That is not a number |
| Correct guess on attempt 2 | Player wins | Secret cast to string; win never detected | No error; game continues as if wrong |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  * Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  * Claude suggested the check_guess solution of reversed hint and it was correct. I used the solution suggested and tested it on the game and it was correct.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  * No suggestions were incorrect or misleading

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  * I went on the website and tested that it worked correctly
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
  * I created a pytest testcase with claude for check_guess and tested all
    the cases and edge cases. It showed all the flaws and things that worked.
- Did AI help you design or understand any tests? How?
  * Yes. it helped me to design and create the test cases, which I verified
    and finalized.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

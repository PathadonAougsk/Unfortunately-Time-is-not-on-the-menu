<h1 align="center">Unfortunately-Time-is-not-on-the-menu</h1>

![Alt Text](Assets/Homepage.png)
## Project Description
- Project by: Pathadon Aougsk
- Game Genre: Point-and-Click Strategy, survival horror

---

## Installation

To Clone this project:
```sh
git clone https://github.com/PathadonAougsk/Unfortunately-Time-is-not-on-the-menu.git
```

To create and run Python Environment for this project:

**Windows:**
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Mac:**
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Running Guide

After activating the Python Environment of this project, you can proceed to run the game by:

**Windows:**
```bat
python main.py
```

**Mac:**
```sh
python3 main.py
```

---

## Tutorial / Usage

**Goal:** Reach 100 points by completing the minigame.

**Minigame:**
- Click **Accept** when the screen says to accept an order
- Do **not** click when the screen says to reject

**Controls:**
| Action | How |
|---|---|
| Change to PC Room | Swipe Left (hover left edge) |
| Go Back to Office | Swipe Right (hover right edge) |
| Wear a Mask | Press **Space** |
| Close the Door | Click the door button |
| Toggle PC | Click the PC button |

**Threats to watch for:**
- Hear a **cat sound** → close the door
- Hear a **footstep** → wear a mask
- See something in the **center of the PC screen** → close the PC

---

## Game Features

- 3 animatronics — MrTemp, MrBall, and MrHappy, each with a unique attack style and a different counter
- Minigame — submit or reject orders to earn score, speeds up as score increases
- Two-room layout — switch between the office and backroom to manage different threats
- Dynamic difficulty — animatronics get more aggressive as your score goes up
- Statistics system — tracks every action and encounter and saves them to an Excel file
- Data visualization — a separate stats window with 5 graphs and tables showing your gameplay data
- Volume control — adjust each animatronic's sound from the main menu

---

## Known Bugs

Sometimes MrBall will kill the player even if the door is closed.
This happens because the AI updates before the player input is processed, so clicking the door on the last frame still counts as open when the attack check runs.

---

## External Sources

### Sound Effects

Sound Effect by [DRAGON-STUDIO](https://pixabay.com/users/dragon-studio-38165424/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=401729) from [Pixabay](https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=401729)

Sound Effect by [DRAGON-STUDIO](https://pixabay.com/users/dragon-studio-38165424/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=397987) from [Pixabay](https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=397987)

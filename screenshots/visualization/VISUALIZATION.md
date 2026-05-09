# Data Visualization

## Overview

![Statistics Window Overview](reaction_time_vs_score.png)

A separate Tkinter window that opens from the main menu. You can filter by animatronic at the top and navigate between 5 visualizations using PREV / NEXT or arrow keys. All data is pulled from `Data.xlsx` which gets written at the end of each session.

---

## Component 1 — Reaction Time vs Score (Line Plot)

![Reaction Time vs Score](reaction_time_vs_score.png)

Shows how fast the player reacted to an attack at different score levels. Green is survived, red is died. Players who die react fast but press the wrong thing, survivors are more consistent and get better as score goes up.

---

## Component 2 — Session Time vs Number of Inputs (Scatter Plot)

![Session Time vs Inputs](session_time_vs_inputs.png)

Each dot is one session — green survived, red died. Deaths tend to have way more inputs in less time (panic mashing). Surviving sessions have fewer, more spread out inputs meaning the player is being more deliberate.

---

## Component 3 — Action Frequency (Bar Plot)

![Action Frequency](action_frequency.png)

Total times the player used each defensive action across all sessions. Mask leads at 102, then PC at 89, Door at 73. Mask being the highest makes sense since MrTemp is the most active threat and the mask is his counter.

---

## Component 4 — Success Rate per Animatronic (Table)

![Success Rate Table](success_rate_table.png)

MrTemp is easiest to survive at 92% — players learn his pattern fast. MrBall sits at 55%. MrHappy is at 0% since players keep forgetting to check the backroom or leave the PC on while he's already approaching.

---

## Component 5 — Input Burst by Time Interval (Box Plot)

![Input Burst by Interval](input_burst_by_interval.png)

Groups inputs by the gap between button presses. The 0–1s group has the highest counts — fast pressing almost always means panic. As the gap gets bigger the counts drop, meaning slower players press far less overall.

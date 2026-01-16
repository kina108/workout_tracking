# Workout Tracking 

A lightweight workout logging app built with Streamlit for recording training sessions and reviewing past workouts.

**Live app:** https://workout-log.streamlit.app

---

## Overview

This project focuses on keeping workout tracking simple and flexible.  
Instead of a full-featured fitness platform, it provides a minimal interface for logging workouts and revisiting past sessions.

The app is designed to be easy to extend and suitable for personal use.

---

## Features

- Log workouts (exercise, sets, reps, weight, notes)
- View and manage past sessions
- Track training consistency over time
- Local data storage using SQLite

---

## Tech stack

- Streamlit
- Python
- SQLite

---

## Running locally

```bash
git clone https://github.com/kina108/workout_tracking.git
cd workout_tracking

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\Activate.ps1  # Windows

pip install -r requirements.txt
streamlit run app.py


# Performance Analyzer for Sports Science for STEM Education
## Website overview
This website is a Performance Analyzer for Sports Science for STEM Education to help users compare their physical performance metrics against a historical dataset. The website uses a Flask web app to:

Collect user data (Toe Taps, Lane Agility, Shuttle Run, Push Ups, Vertical Jump)

Calculate percentile ranks by comparing user input to historical data

Visualize performance using a spider plot (radar chart)

The goal is to provide users with a visual representation of how students perform relative to a given population.
## Features
User Input Form: Allows users to enter their performance metrics.

Percentile Calculation: Computes how a user's performance ranks compared to historical data.

Spider Plot: Generates a radar chart showing user performance scaled by percentile rank.

Responsive Design: Accessible through a simple web interface.
## Troubleshooting
### Historical data errors:

Error: "Error: Historical data file not found."

Fix: Ensure historical_data.csv is present in the project directory.

Tip: Double-check the file path and confirm it matches the one in combineeventapp.py.
### Missing categories:
Error: "Error: Missing columns in dataset."
Fix: Ensure historical_data.csv contains all the required columns:

-Toe Taps

-Lane Agility

-Shuttle Run

-Push Ups

-Vertical Jump
### Matplotlib errors:
Error: "ValueError: x and y must have the same first dimension."

Fix: This occurs if the categories and data points don't match. Ensure the same number of labels and values are passed to the spider plot function.
### Session errors:
Error: "KeyError: 'Toe Taps'"

Fix: This may happen if form names don't match the keys in the Flask session. Ensure form field names in input.html are the same as the keys in combineeventapp.py.
### Flask not running:

Error: "ModuleNotFoundError: No module named 'flask'"

Fix: Make sure Flask is installed:


## Project Structure
project_directory/
│
├── combineeventapp.py        # Main Flask application
├── historical_data.csv       # Historical dataset for performance comparison
│
├── templates/                # HTML templates for Flask
│   ├── home.html
│   ├── input.html
│   ├── result.html
│
├── static/                   # Static files (CSS, JS, images)
│   ├── css/
│   │   └── styles.css
│   ├── spider_plot.png       # Generated spider plot
│
└── README.md



from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Define performance categories and their min/max values
categories = {
    'Toe Taps': (10, 50),       # Higher is better
    'Lane Agility': (5, 20),     # Lower is better
    'Shuttle Run': (10, 30),     # Lower is better
    'Push Ups': (8, 20),         # Higher is better
    'Vertical Jump': (8, 30)     # Higher is better
}

historical_data_path = "historical_data (1).csv"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        # Store user input in session
        for category in categories.keys():
            session[category] = float(request.form.get(category, 0))
        return redirect(url_for('result'))
    return render_template('input.html')
@app.route('/result')
def result():
    # Retrieve user input from session
    user_data = {category: session.get(category, 0) for category in categories.keys()}

    # Load historical data
    if not os.path.exists(historical_data_path):
        return "Error: Historical data file not found."

    historical_data = pd.read_csv(historical_data_path)

    # Ensure all categories exist in the historical data
    missing_columns = [col for col in categories.keys() if col not in historical_data.columns]
    if missing_columns:
        return f"Error: Missing columns in dataset: {missing_columns}"

    # Compute user's percentile ranks
    user_percentiles = []
    for cat, (min_val, max_val) in categories.items():
        if cat in ['Lane Agility', 'Shuttle Run']:  # Lower is better
            percentile = (historical_data[cat] > user_data[cat]).mean() * 100
        else:  # Higher is better
            percentile = (historical_data[cat] < user_data[cat]).mean() * 100
        user_percentiles.append(percentile)

    # Normalize percentiles to [0, 1] for proper scaling
    normalized_values = [p / 100 for p in user_percentiles]

    # Zip the data before passing it to the template
    zipped_data = list(zip(user_data.keys(), user_percentiles))

    # Generate the spider plot
    generate_spider_plot(list(categories.keys()), normalized_values)

    return render_template('result.html', user_data=zipped_data)


def generate_spider_plot(categories, normalized_values):
    num_vars = len(categories)

    # Calculate angles for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles.append(angles[0])

    # Ensure the plot closes by looping back to the first value
    normalized_values.append(normalized_values[0])

    # Create radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Plot user performance (percentile-based scaling)
    ax.plot(angles, normalized_values, linewidth=2, linestyle='solid', label="User Percentile Rank", color='red')
    ax.fill(angles, normalized_values, alpha=0.3, color='orange')

    # Set labels for each axis
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # Add percentage labels on the radial axis
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"])
    ax.set_ylim(0, 1)

    # Add title and legend
    plt.title("User Performance Comparison (Percentile-Based)")
    ax.legend(loc='upper right')

    # Save the spider plot
    plt.savefig('static/spider_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)


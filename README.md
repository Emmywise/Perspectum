# Leaderboard Application

This is a Flask web application for displaying a leaderboard. It supports pagination and a live search feature, allowing users to search for leaderboard entries by name or score. The application also dynamically updates the search results as the user types and allows navigation through pages of results.

## Features

- **Live Search**: Search by name or score as you type.
- **Pagination**: Navigate through leaderboard entries 20 items at a time.
- **Responsive Design**: Compatible with both desktop and mobile browsers.

## Installation

To get this application running on your local machine, follow these steps:

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Setting Up a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
pip install -r requirements.txt
python app.py
The application should now be running on http://localhost:5000/

# To run the test:
python -m unittest test_app.py
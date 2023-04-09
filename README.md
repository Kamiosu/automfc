# MyFigureCollection Automation Project

This repository contains a Python script that automates the process of adding entries to a user's MyFigureCollection.net account using Selenium WebDriver.

## Features

- Automates the sign-in process to MyFigureCollection.net
- Reads data from a CSV file and processes it
- Navigates to the "Add Entry" page and fills out the form based on the processed data
- Supports saving and loading login cookies to minimize the need for signing in repeatedly

## Prerequisites

Before running the script, ensure that you have the following installed on your system:

- Python 3.x
- Selenium WebDriver
- Google Chrome WebDriver
- pandas

## Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory in the terminal.
3. Install the required Python packages:

\```bash
pip install -r requirements.txt
\```

4. Download the [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it in your system's `PATH`.

## Usage

1. Open the `config.py` file and update the following variables with your own MyFigureCollection.net account information:

\```python
USERNAME = 'your_username'
PASSWORD = 'your_password'
\```

2. Create a CSV file named `data.csv` in the project directory, containing the information you want to add to your collection. The CSV file should have the following columns:

- Item Type (e.g., 'goods', 'figures', etc.)
- Display Type (e.g., 'on shelves', 'on walls', etc.)
- Adult Content (e.g., 'safe', 'nsfw', or 'nsfw+')
- Image Filename (if applicable)

3. Run the `main.py` script:

\```bash
python main.py
\```

4. The script will automatically sign in to your account, navigate to the "Add Entry" page, and fill out the form based on the processed data from the CSV file.

5. The script saves login cookies to a file named `cookies.pkl`. Once you have successfully logged in and saved the cookies, you can use them for future sessions by loading them before running the script.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. We appreciate any help in improving the project!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

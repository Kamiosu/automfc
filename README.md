<div align="center">
<img src="images/mfcauto.png" width="50%">
<h1> <a href="https://myfigurecollection.net" target="_blank"><span>MyFigureCollection</span></a> Automation Project </h1>

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)](https://github.com/your_username/your_repository_name/pulls)
[![GitHub last commit](https://img.shields.io/github/last-commit/Kamiosu/automfc)](https://github.com/Kamiosu/automfc/commits/main)


This repository contains a Python script that automates the process of adding entries to a user's MyFigureCollection.net account using Selenium WebDriver.
</div>

## Features

- Automates the sign-in process to MyFigureCollection.net
- Reads data from a JSON file and processes it
- Navigates to the "Add Entry" page and fills out the form based on the processed data
- Supports saving and loading login cookies to minimize the need for signing in repeatedly

## Prerequisites

Before running the script, ensure that you have the following installed on your system read more about installing requirments below:

- Python 3.x
- Selenium WebDriver
- Google Chrome WebDriver
- pandas
- BeautifulSoup
- lxml

## Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory in the terminal.
3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

4. Download the [Chrome WebDriver](https://sites.google.com/chromium.org/driver/downloads?authuser=0) and place it in your system's `PATH`.

## Usage

1. Open the `config.py` file and update the following variables with your own MyFigureCollection.net account information:

```python
USERNAME = 'your_username'
PASSWORD = 'your_password'
```

2. A .JSON file has is already provided that specifies what you need to add. However you can also create your own, .JSON file named `data.JSON` in the project directory, containing the information you want to add to your collection. The JSON file should have the following columns: 
When you run the `script.py` the scraper will automatically create a json for each entry.

- Item Type (e.g., 'goods', 'figures', etc.)
- Display Type (e.g., 'on shelves', 'on walls', etc.)
- Adult Content (e.g., 'safe', 'nsfw', or 'nsfw+')
- Image Filename (if applicable)

| id |  root | category | content_level | image_name | origin | characters | companies | artists | classification |
|:--:|:-----:|:--------:|:-------------:|:----------:|:------:|:----------:|:---------:|:-------:|:--------------:|
|  0 |       |          |               |            |        |            |           |         |                |        
|  1 |       |          |               |            |        |            |           |         |                |
|  2 |       |          |               |            |        |            |           |         |                | 

3. Run the `savecookies.py` script:

```bash
python savecookies.py
```

4. The script will automatically sign in to your account and saves login cookies to a file named `cookies.pkl`. Once you have successfully logged in and saved the cookies, you can use them for future sessions by loading them before running that script anymore.

5. Enter all links when corresponding artists in scraperGOT.py

6. Run script.py, should open a new chrome window and add each entry link given

7. Sit back and relax!
## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. We appreciate any help in improving the project!

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

# IMDb Movies Scraper

This Python script scrapes the top-rated movies from IMDb and stores the data in a MySQL database.

## Prerequisites

Before running the script, make sure you have the following:

- Python
- [MySQL Server](https://dev.mysql.com/downloads/mysql/)


## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/U-Shashank/Movie-Scraper.git
   cd Movie-Scraper
   ```
2. Create a MySQL database and update  the config.json file with your database credentials.

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```
4. Start your mysql server and run the main.py

5. If you want to see the content of the sql table after execution uncomment line number 66-71 before running main.py


## Configuration

You can configure the script by updating the config.json file. Specify your database credentials, including user, password, host, and database.
# DiscordAutoForumBot
DiscordAutoForumBot is a Python script that automates posting images to a Discord forum channel. It uploads images from specified folders, creates posts with custom titles, and tracks progress to avoid re-uploading content. Built with Selenium, it handles login, post creation, and error retries for efficient automation.

---

## Features

- Automates Discord post creation with images.
- Uploads images from folders with custom titles.
- Tracks completed posts to avoid duplicates.
- Handles retries with exponential backoff for reliability.
- Simulates real-user interaction using **Selenium WebDriver**.
- Configurable to work with your existing Chrome login session.

---

## Requirements

- Python 3.x
- Chrome browser and **chromedriver** (compatible with your Chrome version)
- **Selenium** Python library

### Install Dependencies

To install the required Python libraries, run:

```bash
pip install selenium
```

Download ChromeDriver
Download the correct version of ChromeDriver for your installed version of Chrome from [here](https://sites.google.com/chromium.org/driver/).
Place chromedriver.exe in a folder on your machine (e.g., C:\path\to\chromedriver.exe).

Configuration
You need to set up the following configurations in the script:

FORUM_CHANNEL_URL: URL of the Discord forum channel where the posts will be created.
FOLDER_PATH: Path to the folder containing subfolders of images (e.g., C:\path\to\gun_images).
USER_DATA_DIR: Path to your existing Chrome user data (e.g., C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data).
CHROME_DRIVER_PATH: Path to the chromedriver.exe.

Usage
Run the Script
Open a terminal and navigate to the folder where the script is located.

Execute the script:

````bash
python discord_uploader.py
````

The script will:
Log into Discord using your existing Chrome profile.

Loop through folders in the FOLDER_PATH, creating posts with image uploads.
Track completed posts and avoid duplicating uploads.

Progress Tracking
The script tracks previously completed posts using a file named upload_progress.txt. 
If the script is stopped and restarted, it will resume from the last successfully uploaded post.

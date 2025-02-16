# DiscordAutoForumBot 🤖📸

This code contains AI GENERATED CONTENT

Automate image posting to Discord forum channels with browser automation. Perfect for bulk uploads while maintaining "human-like" interaction patterns.

[![Python Version](https://img.shields.io/badge/python-3.x-blue?logo=python)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.x-green?logo=selenium)](https://pypi.org/project/selenium/)

## Features ✨

- 🚀 **Automated Post Creation** - Bulk upload images from organized folders
- 📁 **Smart Folder Processing** - Processes subfolders with custom titles
- 🔄 **Progress Tracking** - Resumes from last successful upload
- ⏳ **Human-like Delays** - Random intervals between actions (Make the delay higher for appearing human like)
- 🔒 **Session Persistence** - Uses existing Chrome profile
- 🛡 **Error Recovery** - Exponential backoff retry system
- 📸 **Image Upload Handling** - Supports multiple formats (PNG, JPG, JPEG, GIF)

## Prerequisites 📋

- Python 3.10+
- Google Chrome (latest version)
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) (matching Chrome version)

## Installation & Setup 🛠️

1. **Install dependencies**
   ```bash
   pip install selenium
   ```

2. **Download ChromeDriver**  
   - Get matching version from [ChromeDriver site](https://sites.google.com/chromium.org/driver/)
   - Place `chromedriver.exe` in your preferred location

3. **Configuration**  
   Edit these variables in `discord_uploader.py`:
   ```python
   # Discord channel URL
   FORUM_CHANNEL_URL = "YOUR_FORUM_CHANNEL_URL"
   
   # Path configurations
   FOLDER_PATH = r"PATH_TO_YOUR_IMAGE_FOLDERS"  # e.g. r"C:\gun_images"
   USER_DATA_DIR = r"CHROME_USER_PROFILE_PATH"  # e.g. r"C:\Users\You\AppData\Local\Google\Chrome\User Data"
   CHROME_DRIVER_PATH = r"PATH_TO_CHROMEDRIVER"  # e.g. r"C:\chromedriver.exe"
   ```

## Usage ▶️

1. Organize your images in this structure:
   ```
   📂 FOLDER_PATH/
   ├── 📂 Class/
   │    ├── 📂 Name_1/
   │    │   ├── image1.jpg
   │    │   └── image2.png
   │    └── 📂 Name_2/
   │         └── imageA.jpeg
   └ ── 📂 Class_2/
 
   ```

2. Start the bot:
   ```bash
   python discord_uploader.py
   ```

3. Let the bot work! 🎉  
   It will:
   - Login using your existing Chrome session
   - Process folders sequentially
   - Create posts with image attachments
   - Save progress for resuming

## Progress Tracking 📈

The bot maintains an `upload_progress.txt` file:
- ✅ Records completed uploads
- 🔄 Auto-resumes from last position
- ❌ Manual edits allowed for error recovery

## Technical Notes ⚙️

- **Humanized Interactions:**  
  Built with randomized delays (0.9-3s between actions)
  
- **Error Handling:**  
  3 retry attempts with exponential backoff
  
- **Browser Compatibility:**  
  Requires Chrome profile with active Discord login ( Just Log in in your Chrome browser )

- **Performance:**  
  Processes ~270-354 posts/hour (varies by image count 59 in 10mins with 1-4 images)

## Troubleshooting 🚨

| Issue                  | Solution                          |
|------------------------|-----------------------------------|
| ChromeDriver mismatch  | Update Chrome & ChromeDriver     |
| Login required         | Manually login in Chrome first   |
| Element not found      | Check Discord UI updates         |
| Upload failures        | Verify image paths & permissions |


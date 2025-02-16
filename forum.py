import os
import time
import logging
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging - fixing encoding issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_uploader.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
FORUM_CHANNEL_URL = "INSERT_DISCORD_CHANNEL_URL"
FOLDER_PATH = r"C:\Users\Desktop\Masurai_gun_build"
USER_DATA_DIR = r"C:\Users\AppData\Local\Google\Chrome\User Data"
CHROME_DRIVER_PATH = r"C:\Users\Desktop\autoforum_post\chromedriver.exe"

# Track progress
PROGRESS_FILE = "upload_progress.txt"

def initialize_driver():
    """Starts the Chrome WebDriver with user session data."""
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={USER_DATA_DIR}")  # Uses your existing login
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    
    service = Service(CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

def wait_for_element(driver, locator_type, locator, timeout=10):
    """Waits for an element to be present using different locator strategies."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((locator_type, locator)))

def wait_and_click(driver, locator_type, locator, timeout=10):
    """Waits for an element to be clickable and clicks it using different locator strategies."""
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((locator_type, locator)))
    element.click()
    return element

def create_forum_post(driver, gun_name, image_paths, max_retries=3):
    """Creates a Discord forum post with the gun's name and uploads images."""
    retries = 0
    while retries < max_retries:
        try:
            logger.info(f"Creating post for: {gun_name}")

            # Click "New Post" button with improved waiting
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//div[contains(text(), 'New Post') or contains(text(), 'Neuer Beitrag')]]")
                )).click()
                logger.info(f"Clicked new Post")
            except:
                driver.execute_script("document.querySelector('button[aria-label*=\"Post\"]').click();")

            # Wait for modal to appear using presence of title field
            title_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'title_d9be46')]"))

)

            # Enter post title
            logger.info(f"Entering Title")
            title_field.click()
            title_field.send_keys(Keys.CONTROL + "a")
            title_field.send_keys(Keys.DELETE)
            for char in gun_name:
                title_field.send_keys(char)
                time.sleep(0.05)

            # Enter post message (a simple ".")
            try:
                logger.info(f"Enter message . ")
                message_field = wait_for_element(driver, By.XPATH, "//div[contains(@class,'slateTextArea')]", timeout=0.5)
                message_field.click()
                message_field.send_keys(".")
            except:
                try:
                    message_field = wait_for_element(driver, By.CSS_SELECTOR, "[role='textbox']", timeout=0.5)
                    message_field.click()
                    message_field.send_keys(".")
                except Exception as e:
                    logger.error(f"Error setting message: {e}")
                    raise
            
            # Click "Post" button
            try:
                logger.info(f"Clicking Post")
                post_button = wait_and_click(driver, By.XPATH, "//button[text()='Post']", timeout=1)
            except:
                try:
                    # Try to find button by partial text
                    buttons = driver.find_elements(By.TAG_NAME, "button")
                    for button in buttons:
                        if "Post" in button.text and "Upload" not in button.text:
                            button.click()
                            break
                except Exception as e:
                    logger.error(f"Error clicking post button: {e}")
                    # Try pressing Enter as last resort
                    message_field.send_keys(Keys.CONTROL + Keys.ENTER)
            
            # Wait for post to be created
            time.sleep(1.2)
             
            
            # Upload images
            if image_paths:
                try:
                    logger.info("Processing Image Upload")
                    # Find file input element
                    file_input = wait_for_element(driver, By.CSS_SELECTOR, "input[type='file']", timeout=10)
                    
                    # Upload images one by one with a small delay between each
                    for image_path in image_paths:
                        file_input.send_keys(image_path)
                        time.sleep(0.5)  # Small delay between uploads
                    
                    # Wait for uploads to finish - look for progress bars to disappear
                    try:
                        WebDriverWait(driver, 60).until(
                            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.uploadProgressBar"))
                        )
                    except:
                        # If we can't find the progress bar, just wait a reasonable time
                        wait_time = len(image_paths) * 3  # 3 seconds per image
                        logger.info(f"Waiting {wait_time} seconds for uploads to complete...")
                        time.sleep(wait_time)
                    
                    # Press Enter to send the message with images
                    text_area = driver.find_element(By.CSS_SELECTOR, "[role='textbox']")
                    text_area.send_keys(Keys.ENTER)
                
                except Exception as e:
                    logger.error(f"Error uploading images: {e}")
            
            # Handle potential "add media to original post" popup
            
            try:
                logger.info("Looking for :'Add to Post'")
                add_to_post_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[div[contains(text(), 'Add to Post')]]"))
                )
                add_to_post_button.click()
                logger.info("Clicked 'Add to Post' button.")
            except TimeoutException:
                logger.info("'Add to Post' button not found, continuing.")
                # Popup didn't appear, continue
                pass
            time.sleep(3)
            # Close the post view using the X button in top right
            
            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Close']"))
                )
                close_button.click()
                logger.info("Clicked 'Close' button.")
            except TimeoutException:
                logger.warning("'Close' button not found, continuing.")
            
            # Success!
            logger.info(f"Post successfully created for {gun_name} ✓")
            return True

        except TimeoutException:
            retries += 1
            wait_time = 5 + (retries * 2)  # Exponential backoff
            logger.warning(f"Timeout error while processing {gun_name}. "
                          f"Retry {retries}/{max_retries} in {wait_time} seconds...")
            time.sleep(wait_time)

        except NoSuchElementException as e:
            logger.error(f"Failed to locate an element for {gun_name}: {e}")
            retries += 1
            if retries >= max_retries:
                logger.error(f"Max retries exceeded for {gun_name}. Skipping...")
                return False
            time.sleep(5)

        except Exception as e:
            logger.error(f"Unexpected error with {gun_name}: {e}")
            retries += 1
            if retries >= max_retries:
                return False
            time.sleep(5)
    
    logger.error(f"Max retries exceeded for {gun_name}. Skipping...")
    return False

def get_completed_posts():
    """Reads previously completed posts from progress file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return set(line.strip() for line in f.readlines())
    return set()

def mark_as_completed(gun_folder):
    """Marks a gun folder as successfully processed."""
    with open(PROGRESS_FILE, 'a') as f:
        f.write(f"{gun_folder}\n")

def main():
    """Main function to process all weapon folders."""
    completed_posts = get_completed_posts()
    logger.info(f"Found {len(completed_posts)} previously completed posts")
    
    driver = initialize_driver()
    try:
        driver.get(FORUM_CHANNEL_URL)
        logger.info("Waiting for Discord to load...")
        time.sleep(8)  # Allow more time for page to load completely

        # Loop through weapon classes
        for weapon_class in os.listdir(FOLDER_PATH):
            class_path = os.path.join(FOLDER_PATH, weapon_class)

            if os.path.isdir(class_path):  # Ensure it's a folder
                for gun_folder in os.listdir(class_path):
                    if gun_folder in completed_posts:
                        logger.info(f"Skipping already processed: {gun_folder}")
                        continue
                    
                    gun_path = os.path.join(class_path, gun_folder)

                    if os.path.isdir(gun_path):  # Ensure it's a folder
                        images = [
                            os.path.join(gun_path, f) for f in os.listdir(gun_path)
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
                        ]

                        if images:
                            logger.info(f"Processing {gun_folder} in {weapon_class}...")
                            success = create_forum_post(driver, gun_folder, images)
                            
                            if success:
                                mark_as_completed(gun_folder)
                                
                                # Add random delay between 3-7 seconds to avoid rate limiting
                                wait_time = random.uniform(0.9, 3)
                                logger.info(f"Waiting {wait_time:.1f} seconds before next post...")
                                time.sleep(wait_time)
                    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        driver.quit()
        logger.info("Script completed execution.")

if __name__ == "__main__":
    main()
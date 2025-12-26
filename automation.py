import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import traceback

# ---------------- LOGGING CONFIG ----------------
# Configure logging to write automation steps and errors into automation.log file
logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

URL = "https://opensource-demo.orangehrmlive.com"

def run_automation(username, password, first_name, last_name, emp_id):
    logging.info("===== Automation started =====")

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless")  # optional headless mode

    service = Service("/usr/bin/chromedriver")

    try:
        logging.info("Starting Chrome browser")
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        # Return failure if browser fails to start
        logging.exception("Failed to start Chrome")
        return {"status": "Failed", "message": f"Chrome start failed: {e}", "employee": ""}

    wait = WebDriverWait(driver, 30)

    try:
        logging.info("Opening OrangeHRM website")
        driver.get(URL)

        logging.info("Entering login credentials")
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button").click()

        logging.info("Navigating to PIM section")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))).click()

        logging.info("Clicking Add Employee")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']"))).click()

        logging.info(f"Entering employee details: {first_name} {last_name} ({emp_id})")
        form_container = wait.until(EC.visibility_of_element_located((By.XPATH, "//form[@class='oxd-form']")))

        form_container.find_element(By.NAME, "firstName").send_keys(first_name)
        form_container.find_element(By.NAME, "lastName").send_keys(last_name)

        emp_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[text()='Employee Id']/following::input[1]")
        ))
        emp_input.clear()
        emp_input.send_keys(emp_id)

        logging.info("Saving employee")
        driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
        time.sleep(3)

        logging.info("Navigating to Employee List")
        try:
            emp_list_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Employee List']")))
            emp_list_btn.click()
        except Exception:
            logging.warning("Employee List click failed — using fallback URL")
            driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")

        logging.info("Searching for employee")
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']")))
        search_box.clear()
        search_box.send_keys(emp_id)
        driver.find_element(By.XPATH, "//button[normalize-space()='Search']").click()
        time.sleep(3)

        rows = driver.find_elements(By.XPATH, "//div[@role='row']")
        if len(rows) <= 1:
            raise Exception("Employee not found after creation")

        logging.info("Extracting employee table data")
        # Extract data for all rows except header
        table_data = []
        for r in rows[1:]:
            table_data.append(r.text.split("\n"))

        # Automatically create column names
        max_cols = max(len(row) for row in table_data)
        columns = [f"Column_{i+1}" for i in range(max_cols)]

        df = pd.DataFrame([row + [""]*(max_cols-len(row)) for row in table_data], columns=columns)
        df.to_csv("extracted_employees.csv", index=False)
        logging.info("Employee data saved to extracted_employees.csv")

        logging.info("Automation completed successfully")
        return {
            "status": "Success",
            "message": "Employee created and verified",
            "employee": f"{first_name} {last_name} ({emp_id})"
        }

    except Exception:
        logging.exception("Automation failed")
        return {
            "status": "Failed",
            "message": traceback.format_exc(),
            "employee": ""
        }

    finally:
        logging.info("Closing browser")
        try:
            driver.quit()
        except Exception:
            pass

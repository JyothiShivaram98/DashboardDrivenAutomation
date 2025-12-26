# Dashboard Driven OrangeHRM Automation

## Overview
This project is a dashboard-driven RPA automation solution for OrangeHRM.  
Users enter login credentials and employee details through a web dashboard, and the system automates:

- Logging into OrangeHRM
- Navigating to the PIM module
- Adding a new employee
- Verifying employee creation
- Extracting employee data into CSV
- Logging out

---

## Technology Stack
- Python 3
- Selenium WebDriver
- Flask (Dashboard Backend)
- HTML/CSS (Frontend)
- Pandas (CSV export)

---

## Project Structure

```
DashboardDrivenAutomation/
├── app.py
├── automation.py
├── requirements.txt
├── README.md
├── extracted_employees.csv
├── automation.log
├── templates/
│   └── index.html
└── static/
    └── style.css
```

---

## How to Run

### 1. Create virtual environment (optional)
```
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Start the application
```
python app.py
```

### 4. Open browser
```
http://127.0.0.1:5000
```

Fill the form and click **Run Automation**.

---

## Code Flow

### Step 1 — Dashboard Input (app.py)
- User enters credentials and employee details.
- Form submits to `/run` route.
- Data is passed to `run_automation()` function.

### Step 2 — Browser Automation (automation.py)
1. Launch Chrome browser
2. Open OrangeHRM website
3. Login using provided credentials
4. Navigate to PIM section
5. Click "Add Employee"
6. Fill employee details
7. Save employee
8. Navigate to Employee List
9. Search employee by ID
10. Verify creation
11. Extract employee table data
12. Save data to CSV
13. Close browser

---

## Logging

All automation steps and errors are logged into:
```
automation.log
```

---

## CSV Output

Extracted employee data is saved to:
```
extracted_employees.csv
```

---

## Important Notes

- Credentials are NOT hardcoded.
- All waits use explicit WebDriverWait.
- Exception handling is implemented.
- Headless mode can be enabled optionally.

---

## Author
Prepared for RPA Practical Assignment – Dashboard Driven Automation.

# Selenium Pytest BDD Automation Framework

This is a Selenium-based automation framework using Pytest and BDD (Behavior-Driven Development) with the Page Object Model (POM) approach to automate the ordering process on the Flipkart website. The framework uses **Pytest Hooks**, **Allure Reports**, and **Pytest HTML Reports** for logging and reporting. The tests are executed in parallel, with screenshots captured for each step and stored in a folder named `Screenshots`.

## Features
- **BDD Support**: Uses Pytest-BDD to write feature files in Gherkin syntax.
- **Page Object Model (POM)**: Implements POM to separate test logic from the page-specific logic.
- **Parallel Test Execution**: Uses Pytest-xdist to run tests in parallel.
- **Allure Reports and Pytest HTML Reports**: Provides detailed and interactive reporting with Allure and Pytest HTML reports.
- **Screenshot Capture**: Captures screenshots at each step and saves them in the `Screenshots` folder, which is cleared before each test run.
- **Command-line Execution**: Allows tests to be run from the command line using Pytest.

## Prerequisites

1. **Python 3.7+**
2. **Google Chrome** (or another browser of your choice)
3. **ChromeDriver** (or corresponding WebDriver for your browser)
4. **pip** - Python package installer

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/Amresh-Nagarro/flipkart_automation.git
   cd flipkart_automation
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install **Allure** for generating reports:

   - On **Windows**:

     Download Allure from [Allure Commandline](https://docs.qameta.io/allure/#_get_started) and add it to your system’s PATH.

   - On **MacOS**:

     ```bash
     brew install allure
     ```

4. **Directory Structure**:

   ```
   flipkart_automation/
   │
   ├── features/                     # BDD feature files
   │   └── order_items.feature        # Feature file with the Flipkart ordering scenario
   │
   ├── pages/                        # Page Object Model classes for Flipkart pages
   │   ├── base_page.py               # Base page containing reusable methods
   │   ├── home_page.py               # Flipkart home page
   │   ├── product_page.py            # Product details page
   │   ├── cart_page.py               # Cart page
   │
   ├── tests/                        # Test scripts written with Pytest
   │   └── test_order_items.py        # Test case for ordering scenario
   │
   ├── utils/                        # Utility functions for screenshots, logging, etc.
   │   ├── screenshot.py              # Captures screenshots for each test step
   │   ├── logger.py                  # Custom logging setup
   │   ├── browser_manager.py         # Handles browser drivers
   │
   ├── reports/                      # Allure and Pytest HTML reports will be saved here
   ├── Screenshots/                  # Stores screenshots captured during test execution
   ├── conftest.py                   # Pytest hooks and fixtures
   ├── pytest.ini                    # Pytest configuration
   ├── requirements.txt              # Dependencies for the project
   └── README.md                     # Project documentation
   ```

## Scenario: Item Ordering on Flipkart

The feature being automated includes the following steps:

1. Open the Flipkart homepage.
2. Search for "Samsung S24 128 GB" and select the second item from the search results.
3. Check the item's availability by entering the pin code "122017" and add it to the cart.
4. Return to the home page.
5. Search for "Bajaj Iron Majesty" and select the second item from the grid.
6. Check the item's availability using the same pin code and add it to the cart.
7. Navigate to the cart.
8. Verify that both items are present in the cart and that the total price reflects the sum of both items.
9. Remove one item from the cart and confirm that the total price updates accordingly.

## Running Tests

1. **Run Tests in Parallel**:

   To run the tests with parallel execution:

   ```bash
   pytest -n <num_of_threads> --alluredir=reports/allure
   ```

   Replace `<num_of_threads>` with the desired number of parallel threads.

2. **Generate Allure Reports**:

   After running the tests, generate the Allure reports with:

   ```bash
   allure serve reports/allure
   ```

   This will open the interactive Allure report in your default browser.

3. **Generate Pytest HTML Report**:

   To generate a Pytest HTML report:

   ```bash
   pytest --html=reports/pytest_report.html
   ```

   The report will be available in `reports/pytest_report.html`.

4. **Command-Line Execution**:

   You can execute the tests directly from the command line using Pytest:

   ```bash
   pytest
   ```

   To include detailed logs and reporting:

   ```bash
   pytest --html=reports/pytest_report.html --alluredir=reports/allure
   ```

## Screenshots

All screenshots for the test steps are stored in the `Screenshots` directory, which is cleared automatically before each test run. Each test step captures a screenshot to help in debugging and validation.

## Key Concepts

1. **BDD (Behavior-Driven Development)**: The feature files are written using Gherkin syntax to describe the steps in a human-readable format.
2. **Page Object Model (POM)**: All the logic for interacting with the web pages is abstracted in separate page classes, making the test scripts clean and easy to maintain.
3. **Parallel Test Execution**: Tests are executed in parallel using Pytest-xdist, which reduces the test execution time.
4. **Allure Reports**: Allure provides a clean and interactive report with detailed test step logs, screenshots, and pass/fail statuses.
5. **Pytest HTML Reports**: Pytest also generates an HTML report for a simpler and easy-to-access log of the test run.

## Conclusion

This framework combines the power of Selenium, Pytest, and Allure to provide a robust, maintainable, and scalable solution for automating Flipkart's item ordering process. By following the principles of BDD and POM, the framework is flexible and easy to extend for other scenarios as well.

--- 

This updated README file now includes instructions for Allure and Pytest HTML reports, replacing the previously mentioned Extent Reports.
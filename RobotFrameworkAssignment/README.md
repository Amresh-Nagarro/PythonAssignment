# Parabank Automation Framework

## Overview
This framework automates the login process for ParaBank and validates the page title using Robot Framework.

## Directory Structure
- **resources/**: Contains reusable keywords.
- **tests/**: Contains test case files.
- **testdata/**: Stores external test data like CSV files.
- **reports/**: Stores generated reports.
- **screenshots/**: Stores captured screenshots.
- **README.md**: Framework documentation.
- **requirements.txt**: Python dependencies.

## Prerequisites
- Python 3.x
- Robot Framework
- SeleniumLibrary
- Allure for reporting
- A browser driver like ChromeDriver or GeckoDriver in your PATH.

## Setup Instructions
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the test: `robot -d ./logs tests/parabank_test.robot`.
4. To generate an Allure report: `allure serve ./reports/allure`.
    ```bash
    pip install -r requirements.txt
    ```
4. Execute tests:
    ```bash
    robot tests/login_test.robot
    ```
5. For parallel execution:
    ```bash
    pabot --processes 4 tests/
    ```

## Usage
- Define reusable keywords in `resources/common.robot`.
- Add test cases in the `tests/` directory.
- Manage test data in `testdata/`.
- Reports and screenshots are generated in their respective directories.

## Best Practices
- Use relative paths to ensure portability.
- Store credentials and configurations in variables or external files.
- Implement data-driven testing for scalability.
- Utilize custom libraries for advanced functionalities.

## Reporting
The framework integrates Extent Reports for enhanced reporting. After test execution, view the report in the `reports/` directory.

## Parallel Execution
Parallel execution can be set up using the `Pabot` library.

## Contact
For any queries or support, contact [Amresh Kumar](mailto:amresh.kumar@nagarro.com).

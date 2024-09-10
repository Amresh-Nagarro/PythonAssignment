import os


def create_environment_file():
    # Define the path where the environment file will be created
    allure_results_path = "allure"

    # Ensure the allure-results directory exists
    if not os.path.exists(allure_results_path):
        os.makedirs(allure_results_path)

    # Define environment variables
    environment_data = {
        "Browser": "Chrome",
        "Browser.Version": "128.0.6613",
        "OS": "Windows 11",
        "OS.Version": "10.0",
        "Environment": "Staging",
        "Test Framework": "Pytest"
    }

    # Create the environment.properties file
    with open(os.path.join(allure_results_path, "environment.properties"), "w") as f:
        for key, value in environment_data.items():
            f.write(f"{key}={value}\n")


if __name__ == "__main__":
    create_environment_file()

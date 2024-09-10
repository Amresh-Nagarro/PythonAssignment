*** Settings ***
Documentation    Test Suite for ParaBank Login
Library          SeleniumLibrary
Library          Selenium2Library
Library          ../custom_libraries/custom_library.py
Library          OperatingSystem
Resource         ../resources/common_keywords.robot
Suite Setup      Setup Suite
Suite Teardown   Teardown Suite
Test Setup       Setup Test
Test Teardown    Teardown Test
Library          Collections
Library          String

*** Variables ***
${URL}           http://parabank.parasoft.com
${BROWSER}       chrome
${TESTDATA_FILE} ./testdata/testdata.csv
${LOG_FILE}      ${OUTPUTDIR}/log.html
${SCREENSHOT_DIR} ${OUTPUTDIR}/screenshots/

*** Test Cases ***
Login to ParaBank and Validate Title
    [Documentation]    This test case logs into ParaBank and validates the title.
    [Tags]             smoke
    ${username}    ${password}    =    Get Credentials From CSV    ${TESTDATA_FILE}    1
    Login To ParaBank    ${username}    ${password}
    Title Should Be    ParaBank | Accounts Overview

Login With Invalid Credentials
    [Documentation]    This test case attempts login with invalid credentials.
    [Tags]             smoke
    ${username}    ${password}    =    Get Credentials From CSV    ${TESTDATA_FILE}    2
    Login To ParaBank    ${username}    ${password}
    Page Should Contain    Invalid username or password.

*** Keywords ***
Setup Suite
    Create Directory    ${SCREENSHOT_DIR}

Teardown Suite
    # Add any suite-level teardown tasks here
    Log    Suite teardown complete.

Setup Test
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Implicit Wait    5s
    Log    Test setup complete.

Teardown Test
    Capture Screenshot On Failure    ${TEST NAME}
    Close Browser
    Log    Test teardown complete.

Capture Screenshot On Failure
    [Arguments]    ${test_name}
    Run Keyword If    '${test_status}' == 'FAIL'    Capture Page Screenshot    ${SCREENSHOT_DIR}${test_name}.png

*** Settings ***
Library    Selenium2Library
Library    ../POCO/context_injection.py

*** Keywords ***
Login To ParaBank
    [Arguments]    ${username}    ${password}
    Input Text    name=username    ${username}
    Input Text    name=password    ${password}
    Click Button    xpath=//input[@value='Log In']
    Wait Until Page Contains Element    xpath=//a[text()='Accounts Overview']    10s

Capture Screenshot On Failure
    [Arguments]    ${test_name}
    Run Keyword If    '${test_status}' == 'FAIL'    Capture Page Screenshot    ${OUTPUTDIR}/screenshots/${test_name}.png

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://cs458-auth-project.vercel.app/api/auth/signin")

email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "email"))  
)

email_input.send_keys("wrong_user@gmail.com")
driver.find_element(By.NAME, "password").send_keys("wrong_password")

button_xpath = "//button[contains(text(), 'Sign in with Credentials')]"
driver.find_element(By.XPATH, button_xpath).click()

error_message_xpath = "//p[contains(text(), 'Sign in failed. Check the details you provided are correct.')]"
error_message_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, error_message_xpath))
)

if error_message_xpath:
    print("Test Case #2 Passed: Invalid Login Detected")
else:
    print("Test Case #2 Failed")

driver.quit()

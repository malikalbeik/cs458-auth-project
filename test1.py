from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://cs458-auth-project.vercel.app/api/auth/signin")

email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "email"))
)

email_input.send_keys("test_user@gmail.com")
driver.find_element(By.NAME, "password").send_keys("test_password")

button_xpath = "//button[contains(text(), 'Sign in with Credentials')]"
driver.find_element(By.XPATH, button_xpath).click()

success_message_xpath = "//h1[contains(text(), 'Welcome you are now signed in')]"
try:
    success_message_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, success_message_xpath))
    )
    print("Login Successful: Success message detected.")
except:
    print("Login Failed: Success message not detected.")

driver.quit()

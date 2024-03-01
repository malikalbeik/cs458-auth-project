import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


WEBSITE_URL = "https://cs458-auth-project.vercel.app"


@pytest.fixture(scope="class")
def driver_init(request):
    driver = webdriver.Chrome()
    request.cls.driver = driver
    driver.maximize_window()
    yield
    driver.close()


@pytest.mark.usefixtures("driver_init")
class BasicTest:
    pass


class TestLogin(BasicTest):
    def test_empty_login_creds(self):
        self.driver.get(WEBSITE_URL)
        WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located(
                (By.ID, "input-email-for-credentials-provider")
            )
        )

        self.driver.find_element(
            by=By.CSS_SELECTOR,
            value="body > div > div > div > div:nth-child(4) > form > button",
        ).submit()

        error_elements = self.driver.find_elements(
            by=By.CSS_SELECTOR, value="body > div > div > div > div.error > p"
        )

        assert len(error_elements) > 0
        assert (
            error_elements[0].text
            == "Sign in failed. Check the details you provided are correct."
        )

    def test_login_with_invalid_email_format(self):
        self.driver.get(WEBSITE_URL)
        WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located(
                (By.ID, "input-email-for-credentials-provider")
            )
        )

        self.driver.find_element(
            by=By.ID,
            value="input-email-for-credentials-provider",
        ).send_keys("invalid")

        self.driver.find_element(
            by=By.ID,
            value="input-password-for-credentials-provider",
        ).send_keys("invalid-password")

        self.driver.find_element(
            by=By.CSS_SELECTOR,
            value="body > div > div > div > div:nth-child(4) > form > button",
        ).submit()

        error_elements = self.driver.find_elements(
            by=By.CSS_SELECTOR, value="body > div > div > div > div.error > p"
        )

        assert len(error_elements) > 0
        assert (
            error_elements[0].text
            == "Sign in failed. Check the details you provided are correct."
        )

    def test_login_with_facebook(self):
        self.driver.get(WEBSITE_URL)
        WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located(
                (By.ID, "input-email-for-credentials-provider")
            )
        )

        self.driver.find_element(
            by=By.CSS_SELECTOR,
            value="body > div > div > div > div:nth-child(2) > form > button",
        ).click()

        assert self.driver.current_url.startswith("https://www.facebook.com/login.php")

    def test_login_with_google(self):
        self.driver.get(WEBSITE_URL)
        WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located(
                (By.ID, "input-email-for-credentials-provider")
            )
        )

        self.driver.find_element(
            by=By.CSS_SELECTOR,
            value="body > div > div > div > div:nth-child(3) > form > button",
        ).click()

        assert self.driver.current_url.startswith(
            "https://accounts.google.com/v3/signin"
        )
        
    def test_failed_login_with_incorrect_credentials(self):
        self.driver.get(WEBSITE_URL)
        email_input = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys("wrong_user@gmail.com")
        self.driver.find_element(By.NAME, "password").send_keys("wrong_password")

        button_xpath = "//button[contains(text(), 'Sign in with Credentials')]"
        self.driver.find_element(By.XPATH, button_xpath).click()

        error_message_xpath = "//p[contains(text(), 'Sign in failed. Check the details you provided are correct.')]"
        error_message_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, error_message_xpath))
        )

        if error_message_element:
            assert True, "Test Case #2 Passed: Invalid Login Detected"
        else:
            assert False, "Test Case #2 Failed"
            
    def test_successful_login(self):
        self.driver.get(WEBSITE_URL)
        email_input = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys("test_user@gmail.com")
        self.driver.find_element(By.NAME, "password").send_keys("test_password")

        button_xpath = "//button[contains(text(), 'Sign in with Credentials')]"
        self.driver.find_element(By.XPATH, button_xpath).click()

        success_message_xpath = "//h1[contains(text(), 'Welcome you are now signed in')]"
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, success_message_xpath))
            )
            assert True, "Login Successful: Success message detected."
        except:
            assert False, "Login Failed: Success message not detected."

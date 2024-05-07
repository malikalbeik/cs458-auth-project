import pytest
import requests
import ephem
from geopy.distance import geodesic
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
            assert True, "Test Case Passed: Invalid Login Detected"
        else:
            assert False, "Test Case Failed"
            
    def test_login_with_invalid_phone_number(self):
        self.driver.get(WEBSITE_URL)
        WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located(
                (By.NAME, "phone_number")
            )
        )
        self.driver.find_element(
            By.NAME, "phone_number"
        ).send_keys("05555555558") 

        self.driver.find_element(By.NAME, "password").send_keys("test_password")
        
        self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'Sign in with Credentials')]"
        ).click()

        error_message_xpath = "//p[contains(text(), 'Sign in failed. Check the details you provided are correct.')]"
        error_message_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, error_message_xpath))
        )

        if error_message_element:
            assert True, "Test Case Passed: Invalid Login Detected"
        else:
            assert False, "Test Case Failed"
            
    def test_successful_login(self):
        self.driver.get(WEBSITE_URL)
        email_input = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys("test_user@gmail.com")
        self.driver.find_element(By.NAME, "password").send_keys("test_password")

        button_xpath = "//button[contains(text(), 'Sign in with Credentials')]"
        self.driver.find_element(By.XPATH, button_xpath).click()

        success_message_xpath = "//h1[contains(text(), 'Welcome, you are now signed in')]"
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, success_message_xpath))
            )
            assert True, "Login Successful: Success message detected."
        except:
            assert False, "Login Failed: Success message not detected."
    
    def test_successful_display_location_service(self):
        self.driver.get("https://ilkerozgen.github.io/cs458-project-3/")

        # Click 'Get Location' button
        get_location_button_xpath = "//button[contains(text(), 'Get Location')]"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, get_location_button_xpath))
        ).click()
            
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("Location access permission granted.")
        except TimeoutException:
            print("No location access permission pop-up appeared.")

        # Verify distance to the nearest sea is displayed
        distance_message_xpath = "//p[contains(text(), 'Distance to nearest sea')]" 
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, distance_message_xpath))
            )
            assert True, "Distance message displayed."
        except:
            assert False, "Distance message not displayed."
        
    def test_display_correct_distance_calculation_with_range_verification(self):
        
        # IMPORTANT NOTE: This test function only works correctly when the function before is executed first. This is because the
        # location permission granted works for the selenium web driver, but not for the actual browser. Therefore, the location
        # button must be clicked at least once to display and compare results, which is done in the previous test function.
        
        self.driver.get("https://ilkerozgen.github.io/cs458-project-3/")
        # Fetch actual geolocation data
        response = requests.get('https://ipinfo.io/json?token=1a0cc121a33379')
        data = response.json()
        latitude, longitude = map(float, data['loc'].split(','))
        print(f"Actual Location: Latitude: {latitude}, Longitude: {longitude}")

        # Click 'Get Location' button
        get_location_button_xpath = "//button[contains(text(), 'Get Location')]"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, get_location_button_xpath))
        ).click()

        # Handle location permission alert, if it appears
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("Location access permission granted.")
        except TimeoutException:
            print("No location access permission pop-up appeared, or permission previously granted.")
            
        
        seas = [
            { "name": "Black Sea", "latitude": 41.2, "longitude": 29.1 },
            { "name": "Marmara Sea", "latitude": 40.8, "longitude": 28.9 },
            { "name": "Caspian Sea", "latitude": 40.3, "longitude": 50.3 },
            { "name": "Mediterranean Sea", "latitude": 35.0, "longitude": 18.0 },
            { "name": "Red Sea", "latitude": 20.0, "longitude": 38.0 },
            { "name": "Adriatic Sea", "latitude": 42.5, "longitude": 17.5 },
            { "name": "Aegean Sea", "latitude": 37.5, "longitude": 25.0 },
            { "name": "Baltic Sea", "latitude": 55.0, "longitude": 20.0 },
            { "name": "North Sea", "latitude": 57.0, "longitude": 3.0 },
            { "name": "Arabian Sea", "latitude": 10.0, "longitude": 65.0 },
            { "name": "Andaman Sea", "latitude": 12.0, "longitude": 97.0 },
            { "name": "South China Sea", "latitude": 12.0, "longitude": 115.0 },
            { "name": "East China Sea", "latitude": 30.0, "longitude": 123.0 },
            { "name": "Philippine Sea", "latitude": 15.0, "longitude": 130.0 },
            { "name": "Coral Sea", "latitude": -18.0, "longitude": 150.0 },
            { "name": "Tasman Sea", "latitude": -40.0, "longitude": 160.0 },
            { "name": "Bering Sea", "latitude": 58.0, "longitude": -175.0 },
	    ]

        # Find the closest sea
        closest_sea = None
        min_distance = float('inf')
        for sea in seas:
            sea_distance = geodesic((latitude, longitude), (sea['latitude'], sea['longitude'])).kilometers
            if sea_distance < min_distance:
                min_distance = sea_distance
                closest_sea = sea

        expected_distance = min_distance  # Distance to the closest sea
        
        # Extract the displayed distance from the web page
        distance_message_xpath = "//p[contains(text(), 'Distance to nearest sea')]"
        distance_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, distance_message_xpath))
        )
        displayed_distance = float(distance_message.text.split(":")[1].strip().split(" ")[0])

        # Compare the expected distance with the displayed distance
        print(f"Expected Distance to {closest_sea['name']}: {expected_distance} km")
        print(f"Displayed Distance: {displayed_distance} km")

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, get_location_button_xpath))
        ).click()
        
        # Assert if they are within an acceptable range
        assert abs(expected_distance - displayed_distance) < 300, "The distance displayed is not accurate within 300 km tolerance."
        
    def test_display_correct_sun_distance_calculation(self):
        self.driver.get("https://ilkerozgen.github.io/cs458-project-3/")

        # Click 'Get Location' button to calculate the distance to the nearest sea first
        get_location_button_xpath = "//button[contains(text(), 'Get Location')]"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, get_location_button_xpath))
        ).click()

        # Handle location permission alert, if it appears
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("Location access permission granted for sea distance.")
        except TimeoutException:
            print("No location access permission pop-up appeared, or permission previously granted for sea.")

        # Wait for the sea distance calculation to complete and display
        sea_distance_message_xpath = "//p[contains(text(), 'Distance to nearest sea')]"
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, sea_distance_message_xpath))
        )

        # Click the 'Next' button to switch to sun distance calculations
        next_button_xpath = "//button[@id='nextBtn']"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, next_button_xpath))
        ).click()

        # Fetch actual geolocation data
        response = requests.get('https://ipinfo.io/json?token=1a0cc121a33379')
        data = response.json()
        latitude, longitude = map(float, data['loc'].split(','))
        print(f"Actual Location: Latitude: {latitude}, Longitude: {longitude}")
        
        # Use ephem to calculate the distance to the sun
        observer = ephem.Observer()
        observer.lat = str(latitude)
        observer.lon = str(longitude)
        observer.date = ephem.now()
        sun = ephem.Sun()
        sun.compute(observer)
        expected_sun_distance = sun.earth_distance * 149597870.7  # Convert AU to km
        
        # Extract the displayed distance to the sun from the web page
        sun_distance_message_xpath = "//p[@id='currentLocationSunDistance']"
        sun_distance_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, sun_distance_message_xpath))
        )
        displayed_sun_distance = float(sun_distance_message.text.split(":")[1].strip().split(" ")[0])

        print(f"Expected Distance to Sun's core: {expected_sun_distance} km")
        print(f"Displayed Distance: {displayed_sun_distance} km")

        # Assert if they are within an acceptable range
        assert abs(expected_sun_distance - displayed_sun_distance) < 150000, "The distance to the Sun's core displayed is not accurate within 1 percent error rate."
        
    def test_manual_sun_distance_calculation(self):
        self.driver.get("https://ilkerozgen.github.io/cs458-project-3/")

        # Click 'Get Location' button to calculate the distance to the nearest sea first
        get_location_button_xpath = "//button[contains(text(), 'Get Location')]"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, get_location_button_xpath))
        ).click()

        # Handle location permission alert
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("Location access permission granted for sea distance.")
        except TimeoutException:
            print("No location access permission pop-up appeared, or permission previously granted for sea.")

        # Wait for the sea distance calculation to complete
        sea_distance_message_xpath = "//p[contains(text(), 'Distance to nearest sea')]"
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, sea_distance_message_xpath))
        )

        # Click the 'Next' button to switch to manual sun distance calculations
        next_button_xpath = "//button[@id='nextBtn']"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, next_button_xpath))
        ).click()

        # Enter latitude and longitude
        latitude_input_xpath = "//input[@id='latitude']"  
        longitude_input_xpath = "//input[@id='longitude']"
        latitude, longitude = 40.7128, -74.0060  # Coordinates for New York City

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, latitude_input_xpath))).send_keys(str(latitude))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, longitude_input_xpath))).send_keys(str(longitude))

        # Calculate expected distance to the sun using ephem
        observer = ephem.Observer()
        observer.lat = str(latitude)
        observer.lon = str(longitude)
        observer.date = ephem.now()
        sun = ephem.Sun(observer)
        sun.compute(observer)
        expected_sun_distance = sun.earth_distance * 149597870.7  # Convert AU to km

        # Wait for the application to display the sun distance
        sun_distance_message_xpath = "//p[@id='inputSunDistance']"
        sun_distance_message = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, sun_distance_message_xpath))
        )
        displayed_sun_distance = float(sun_distance_message.text.split(":")[1].strip().split(" ")[0])

        print(f"Expected Distance to Sun's core: {expected_sun_distance} km")
        print(f"Displayed Distance: {displayed_sun_distance} km")

        # Assert that the displayed distance is within an acceptable range
        assert abs(expected_sun_distance - displayed_sun_distance) < 150000, "The distance to the Sun's core displayed is not accurate within 1 percent error rate."


    def test_invalid_coordinates(self):
        self.driver.get("https://ilkerozgen.github.io/cs458-project-3/")

        # Click 'Get Location' button to calculate the distance to the nearest sea first
        get_location_button_xpath = "//button[contains(text(), 'Get Location')]"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, get_location_button_xpath))
        ).click()

        # Handle location permission alert, if it appears
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("Location access permission granted for sea distance.")
        except TimeoutException:
            print("No location access permission pop-up appeared, or permission previously granted for sea.")

        # Wait for the sea distance calculation to complete and display
        sea_distance_message_xpath = "//p[contains(text(), 'Distance to nearest sea')]"
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, sea_distance_message_xpath))
        )

        # Click the 'Next' button to switch to manual sun distance calculations
        next_button_xpath = "//button[@id='nextBtn']"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, next_button_xpath))
        ).click()

        # User inputs latitude and longitude
        latitude_input_xpath = "//input[@id='latitude']"  
        longitude_input_xpath = "//input[@id='longitude']"
        submit_button_xpath = "//button[@id='calculateSunDistance']" 

        # Invalid coordinates example
        invalid_latitude = "91"  # Latitude must be between -90 and 90
        invalid_longitude = "190"  # Longitude must be between -180 and 180
        
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, latitude_input_xpath))).clear()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, longitude_input_xpath))).clear()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, latitude_input_xpath))).send_keys(invalid_latitude)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, longitude_input_xpath))).send_keys(invalid_longitude)

        # Click the button to calculate distance to the sun with invalid inputs
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath))).click()

        # Check for error message
        error_message_xpath = "//p[@id='error']"
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, error_message_xpath))
            )
            print(f"Error message displayed: {error_message.text}")
            assert error_message.is_displayed(), "Test Case Passed: Error displayed for invalid coordinates."
        except TimeoutException:
            assert False, "Test Case Failed: No error message displayed for invalid coordinates."
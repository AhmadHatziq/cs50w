import os
import pathlib
import unittest

from selenium import webdriver

from selenium.webdriver.common.by import By

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)

class WebpageTests(unittest.TestCase):

    def test_title(self):
        driver.get(file_uri("counter.html"))
        self.assertEqual(driver.title, "Counter")

    def test_increase(self):
        driver.get(file_uri("counter.html"))
        increase = driver.find_element("id", "increase")
        increase.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "1") # Assert 2 equal strings, not ints. 

    def test_decrease(self):
        driver.get(file_uri("counter.html"))
        decrease = driver.find_element("id", "decrease")
        decrease.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "-1")

    def test_multiple_increase(self):
        driver.get(file_uri("counter.html"))
        increase = driver.find_element("id", "increase")
        for i in range(3):
            increase.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "3")

if __name__ == "__main__":
    unittest.main()
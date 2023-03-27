from selenium import webdriver
import pytest


@pytest.fixture(autouse=True)
def set():
    driver = webdriver.Chrome('D:\Skillfactory\PythonTests\Drivers\chromedriver.exe')
    driver.get('http://petfriends.skillfactory.ru/login')

    yield

    driver.quit()
import pytest


@pytest.fixture(autouse=True)
def setup(driver, server_url):
    driver.get(server_url + '/admin/')
    yield driver


@pytest.mark.functional
def test_home_page(driver):
    element = driver.find_element_by_tag_name('h1')
    assert element.text == 'Django administration'

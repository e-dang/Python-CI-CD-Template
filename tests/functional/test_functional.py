import pytest


@pytest.mark.functional
def test_home_page(driver, live_server):
    driver.get(live_server.url + '/admin')
    element = driver.find_element_by_tag_name('h1')
    assert element.text == 'Django administration'

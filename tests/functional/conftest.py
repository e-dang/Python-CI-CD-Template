import os
from datetime import datetime

import pytest
from selenium import webdriver


@pytest.fixture(scope='session', params=[(webdriver.Firefox, webdriver.FirefoxOptions)])
def driver(request):
    kwargs = {}
    driver_cls, options_cls = request.param
    if request.config.getoption('--headless'):
        opts = options_cls()
        opts.add_argument('--headless')
        kwargs['options'] = opts

    driver = driver_cls(**kwargs)

    yield driver

    driver.quit()


@pytest.fixture
def server_url(live_server):
    url = os.environ.get('SERVER_URL')
    if url:
        return url
    return live_server.url


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # set up a hook to be able to check if a test has failed
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):  # check if a test has failed
    yield
    # request.node is an "item" because we use the default
    # "function" scope
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            driver = request.node.funcargs['driver']
            take_screenshot(driver, request.node.nodeid)


def take_screenshot(driver, nodeid):  # make a screenshot with a name of the test, date and time
    file_name = f'{nodeid}_{datetime.today().strftime("%Y-%m-%d_%H-%M")}.png'.replace("/", "_").replace("::", "__")
    screenshot_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
    if not os.path.exists(screenshot_dir):
        os.mkdir(screenshot_dir)
    driver.save_screenshot(os.path.join(screenshot_dir, file_name))

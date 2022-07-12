from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, time, requests

username = os.getenv("CBT_USERNAME")
authkey = os.getenv("CBT_AUTHKEY")

api_session = requests.Session()
api_session.auth = (username, authkey)
test_result = None
build = "Dev"
release = "Azure Test Development - {}".format(build)
baseUrl = "https://test.moneyhelper.org.uk"

caps = {
    'name': '{}'.format(release),
    'build': '{}'.format(build),
    'platform': 'Windows',
    'browserName': 'Chrome',
    'version' : '102',
    'screenResolution' : '1920x1080',
    'record_video' : 'true',
    'max_duration' : '3600'
}

driver = webdriver.Remote(
    command_executor="http://%s:%s@hub.crossbrowsertesting.com/wd/hub"%(username, authkey),
    desired_capabilities=caps)

try:
    # ------- Start test ------- #
    
    driver.get(baseUrl)

    # ------- End test ------- #
    test_result = 'pass'
except AssertionError as e:
    test_result = 'fail'
    raise

print("Done with session %s" % driver.session_id)
driver.quit()
# Here we make the api call to set the test's score.
# Pass it it passes, fail if an assertion fails, unset if the test didn't finish
if test_result is not None:
    api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + driver.session_id,
        data={'action':'set_score', 'score':test_result})

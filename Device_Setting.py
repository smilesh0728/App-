from appium import webdriver


def init_driver():
    desired_caps = dict(
        platformName='Android',
        platformVersion='10',
        automationName='Appium',
        deviceName='SM-T595N',
        udid='6f2ed365',
        app='C:\\Entry\\app-release.apk'
    )
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver
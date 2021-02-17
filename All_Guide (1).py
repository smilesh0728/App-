import subprocess
from time import sleep
import ExcelHandler
import Device_Setting
from appium.webdriver.common.touch_action import TouchAction

driver = Device_Setting.init_driver()
actions = TouchAction(driver)

'''------------------------------------------------ Uploading Process -------------------------------------------------------------'''

def Creation_Process(n):

    '''가이드 영상 skip '''
    for i in range(0,2):
        actions.tap(x=906, y=618).perform()
        sleep(0.3)
        driver.find_element_by_accessibility_id("다음").click()
        sleep(1)
        driver.find_element_by_accessibility_id("네").click()
        sleep(2)

    '''튜토리얼 닫기'''
    actions.tap(x = 1782, y = 1006).perform()
    sleep(7)

    '''코딩화면 진입 > 블루투스 연결 확인'''
    moduleConnected = 0
    print("bluetooth connecting...")
    while not moduleConnected:
        sleep(1)
        actions.tap(x=680, y=54).perform()
        sleep(5)

        try:
            driver.find_element_by_accessibility_id("MODI_8D36CA18").click()
            sleep(7)

            #모듈 연결 성공
            if "연결됨" in driver.find_element_by_accessibility_id("MODI_8D36CA18\n연결됨").get_attribute("content-desc"):
                print("....................Connected!")
                moduleConnected = 1
                sleep(1)

            #모듈 연결 실패
            else:
                '''
                모듈 연결에 실패했을 경우 Search 버튼을 누른 후 10초 기다린 후,
                블루투스 창을 닫고 다시 연결 시도
                '''
                print("....................failed")
                driver.find_element_by_xpath("//android.view.View[@content-desc=\"블루투스 연결\n등록된 모듈\n검색된 모듈\n블루투스 자동 연결 기능\"]/android.view.View[2]/android.widget.Button").click()
                print("Trying again...")
                sleep(10)
                driver.find_element_by_xpath("//android.view.View[@content-desc=\"블루투스 연결\n등록된 모듈\n검색된 모듈\n블루투스 자동 연결 기능\"]/android.view.View[1]/android.view.View").click()

        except BaseException:
            print("Module is not found")


    '''블루투스 연결 창 닫기'''
    driver.find_element_by_xpath("//android.view.View[@content-desc=\"블루투스 연결\n등록된 모듈\n검색된 모듈\n블루투스 자동 연결 기능\"]/android.view.View[1]/android.view.View").click()

    '''모범 답안 다운로드'''
    print("code downloading...")
    actions.tap(x=687, y=1114).perform()
    sleep(1)
    actions.perform()
    print("....................succeeded!")
    sleep(2)

    '''
    코드 업로드와 초기화를 (count)회 반복한다. 
    업로드, 초기화 실패가 발생할 때마다 fail 변수에 카운트 1 한다. (성공률을 체크하기 위함)
    '''
    i = 0
    count = n
    Uploadfail = 0
    Resetfail = 0

    while i < count:
        # 코드 업로드 버튼 click > "네"
        '''연결되지 않은 블록에 대한 예외처리 없음'''
        print("Upload Processing...({})".format(i+1))
        actions.tap(x=1409, y=1110).perform()
        sleep(0.5)
        driver.find_element_by_accessibility_id("네").click()
        print("Code uploading...")
        sleep(16)

        # 결과 팝업창의 문구를 value 변수에 넣어 성공/실패를 구분함.
        UploadResult = driver.find_element_by_class_name("android.widget.ImageView").get_attribute("content-desc")
        # 업로드 성공

        if "성공" in UploadResult:
            actions.tap(x=956, y=753).perform()
            i += 1
            print("....................succeeded!")
            CodeUploaded = 1
            sleep(1)

            # 코드 업로드 완료 후, 초기화 진행
            while CodeUploaded:
                actions.tap(x=1521, y=1098).perform()
                sleep(1)
                driver.find_element_by_accessibility_id("네").click()
                print("Code reset...")
                sleep(10)

                # "코드 업로드를 완료했습니다" > "네"
                resetValue = driver.find_element_by_class_name('android.widget.ImageView').get_attribute("content-desc")

                if '초기화 되었어요' in resetValue:
                    print("....................succeeded!")
                    actions.tap(x=956, y=753).perform()
                    CodeUploaded = 0

                # 초기화 실패시, 확인 클릭 후 초기화 재진행
                else:
                    actions.tap(x=956, y=753).perform()
                    Resetfail += 1
        # 업로드 실패
        else:
            actions.tap(x=956, y=753).perform()
            print("....................failed")
            Uploadfail += 1
            i += 1

    '''성공 횟수'''
    print("업로드 {}회 중 {}회 성공".format(count, count-Uploadfail))
    print("초기화 {}회 중 {}회 성공".format(count, count-Resetfail))

    '''성공률'''
    percentage = 100-Uploadfail/count*100
    percentage2 = 100-Resetfail/count*100
    print("업로드 성공률 : {}%".format(percentage))
    print("초기화 성공률 : {}%".format(percentage2))


    if percentage != 100:
        result = "NP"

    else:
        result = "PASS"

    return result, percentage, percentage2

#----------------------------------------------------------------------------------------------------------------

sleep(4)
subprocess.call("adb shell input keyevent 66", shell=True)
subprocess.call("adb shell input keyevent 66", shell=True)

'''튜토리얼 skip'''
sleep(6)
actions.tap(x=1782, y=1006).perform()
sleep(1)

'''가이드 선택'''
driver.find_element_by_accessibility_id("가이드").click()
sleep(1)

'''메이킹팩 Vol.1'''
driver.find_element_by_accessibility_id("메이킹 팩\n Vol. 1").click()
sleep(3)

'''------------------------------------------------ Creation 3 --------------------------------------------------------------'''

'''Swipe and then click creation '''
actions.press(x=1800, y=80).move_to(x=1000, y=80).release().perform()
driver.find_element_by_accessibility_id("Creation 3\n빙고 머신").click()
sleep(4)

'''가이드 업로드, 초기화 5회씩 진행'''
result, percentage, percentage2 = Creation_Process(5)

'''Excel에 결과값 기입, k9~'''
ExcelHandler.PutResult('K9', result, "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
ExcelHandler.PutResult('L9', "업로드 성공률 : {}%\n 초기화 성공률 : {}%".format(percentage, percentage2),
                       "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
sleep(3)
driver.back()

'''------------------------------------------------ Creation 4 --------------------------------------------------------------'''

actions.press(x=1800, y=80).move_to(x=1000, y=80).release().perform()
driver.find_element_by_accessibility_id("Creation 4\n룰렛").click()
sleep(4)

'''가이드 업로드, 초기화 5회씩 진행'''
result, percentage, percentage2 = Creation_Process(5)

'''Excel에 결과값 기입, k9~'''
ExcelHandler.PutResult('K10', result, "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
ExcelHandler.PutResult('L10', "업로드 성공률 : {}%\n 초기화 성공률 : {}%".format(percentage, percentage2),
                       "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
sleep(3)
driver.back()

'''------------------------------------------------ Creation 5 --------------------------------------------------------------'''

actions.press(x=1800, y=80).move_to(x=1000, y=80).release().perform()
driver.find_element_by_accessibility_id("Creation 5\n회전 연필 꽂이").click()
sleep(4)

'''가이드 업로드, 초기화 5회씩 진행'''
result, percentage, percentage2 = Creation_Process(5)

'''Excel에 결과값 기입, k9~'''
ExcelHandler.PutResult('K11', result, "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
ExcelHandler.PutResult('L11', "업로드 성공률 : {}%\n 초기화 성공률 : {}%".format(percentage, percentage2),
                       "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
sleep(3)
driver.back()

'''------------------------------------------------ Creation 6 --------------------------------------------------------------'''

actions.press(x=1800, y=80).move_to(x=1000, y=80).release().perform()
driver.find_element_by_accessibility_id("Creation 6\n조이트로프").click()
sleep(4)

'''가이드 업로드, 초기화 5회씩 진행'''
result, percentage, percentage2 = Creation_Process(5)

'''Excel에 결과값 기입, k9~'''
ExcelHandler.PutResult('K12', result, "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
ExcelHandler.PutResult('L12', "업로드 성공률 : {}%\n 초기화 성공률 : {}%".format(percentage, percentage2),
                       "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
sleep(3)
driver.back()

'''------------------------------------------------ Creation 7 --------------------------------------------------------------'''

actions.press(x=1800, y=80).move_to(x=1000, y=80).release().perform()
driver.find_element_by_accessibility_id("Creation 7\nLED 타이머").click()
sleep(4)

'''가이드 업로드, 초기화 5회씩 진행'''
result, percentage, percentage2 = Creation_Process(5)

'''Excel에 결과값 기입, k9~'''
ExcelHandler.PutResult('K13', result, "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
ExcelHandler.PutResult('L13', "업로드 성공률 : {}%\n 초기화 성공률 : {}%".format(percentage, percentage2),
                       "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
sleep(3)
driver.back()

'''------------------------------------------------ Creation 8 --------------------------------------------------------------'''

actions.press(x=1800, y=80).move_to(x=1000, y=80).release().perform()
driver.find_element_by_accessibility_id("Creation 8\n무드등").click()
sleep(4)

'''가이드 업로드, 초기화 5회씩 진행'''
result, percentage, percentage2 = Creation_Process(5)

'''Excel에 결과값 기입'''
ExcelHandler.PutResult('K14', result, "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
ExcelHandler.PutResult('L14', "업로드 성공률 : {}%\n 초기화 성공률 : {}%".format(percentage, percentage2),
                       "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
sleep(3)
driver.back()

'''------------------------------------------------ Creation 9 --------------------------------------------------------------'''

actions.press(x=1800, y=80).move_to(x=1000, y=80).release().perform()
driver.find_element_by_accessibility_id("Creation 9\nLED 메트로놈").click()
sleep(4)

'''가이드 업로드, 초기화 5회씩 진행'''
result, percentage, percentage2 = Creation_Process(5)

'''Excel에 결과값 기입 '''
ExcelHandler.PutResult('K15', result, "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
ExcelHandler.PutResult('L15', "업로드 성공률 : {}%\n 초기화 성공률 : {}%".format(percentage, percentage2),
                       "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
sleep(3)
driver.back()

'''------------------------------------------------ Creation 10 -------------------------------------------------------------'''

actions.press(x=1800, y=80).move_to(x=1000, y=80).release().perform()
driver.find_element_by_accessibility_id("Creation 10\n금고").click()
sleep(4)

'''가이드 업로드, 초기화 5회씩 진행'''
result, percentage, percentage2 = Creation_Process(5)

'''Excel에 결과값 기입, k9~'''
ExcelHandler.PutResult('K16', result, "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
ExcelHandler.PutResult('L16', "업로드 성공률 : {}%\n 초기화 성공률 : {}%".format(percentage, percentage2),
                       "C:\\Users\\Sydney\\OneDrive - 럭스로보\\Codesketch_Quick.xlsx")
sleep(3)
driver.back()

'''quit process'''
sleep(5)
#driver.quit()





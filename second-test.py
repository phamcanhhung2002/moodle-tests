from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from data import dataTest_add_a_discuss as data

import unittest
import time
# 11 -> November
import sys


class MoodleTest(unittest.TestCase):

    # def __init__(self):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.data = data
        
    def gotoWeb(self, index = 0):
        self.driver.get(self.data[index].url)
        self.driver.implicitly_wait(10)

        try:
            # Check if in Login Page
            currentURL = self.driver.current_url
            if ("login" not in currentURL):
                self.driver.find_element(By.XPATH, "//*[@id=\"usernavigation\"]/div[5]/div/span/a").click()

            currentURL = self.driver.current_url

            # Fill in Username and Password
            username = self.driver.find_element(By.XPATH, "//*[@id=\"username\"]")
            password = self.driver.find_element(By.XPATH, "//*[@id=\"password\"]")

            username.send_keys(self.data[index].username)
            password.send_keys(self.data[index].password)

            loginBtn = self.driver.find_element(By.XPATH, "//*[@id=\"loginbtn\"]").click()

        except:
            print("gotoWeb: FAILED")
            assert False
    
    def gotoCourse(self, index = 0):
        try:
            # Check if in Course Page
            currentURL = self.driver.current_url
            if ("course" not in currentURL):
                self.driver.find_element(By.XPATH, "//*[@id=\"moremenu-656376a99311b-navbar-nav\"]/li[3]/a").click()

            # Find the course
            courseSearch = self.driver.find_element(By.NAME, "search")
            courseSearch.send_keys(self.data[index].course_name)
            time.sleep(3)

            # Access to the course
            try:
                courses = self.driver.find_elements(By.XPATH, "//a[@href and @class='aalink coursename mr-2 mb-1']")
                for element in courses:
                    if (self.data[index].course_name in element.get_attribute("innerHTML")):
                        element.click()
                        break

            except:
                print("Course not found!")
                assert False
        
        except:
            print("gotoCourse: FAILED")
            assert False

    def gotoForum(self, index = 0):
        try:
            forum = self.driver.find_element(By.XPATH, "//*[@class=\"activity-grid \"]/a")
            forum.click()

        except NoSuchElementException:
            print("gotoForum: FAILED")
            assert False

    def gotoAddDiscuss(self, index = 0):
        try:
            addDiscussBtn = self.driver.find_element(By.XPATH, "//a[@href=\"#collapseAddForm\"]")
            addDiscussBtn.click()

            time.sleep(3)
        except: 
            print("gotoAddDiscuss: FAILED")
            assert False

    def getIndexData(self, index = 0):
        for i in range(0, len(self.data)):
            if index == int(self.data[i].test_case):
                return i

    def send_keys_TinyMCE(self, elementId = "", text = ""):
        try:
            element = ""
            if "//iframe" in elementId:
                element = elementId
            else:
                element = "//iframe[@id='{}']".format(elementId)
            
            iframeElement = self.driver.find_element(By.XPATH, element)
            self.driver.switch_to.frame(frame_reference = iframeElement)
            self.driver.find_element(By.XPATH, "//body[@id='tinymce']").send_keys(text)
            self.driver.switch_to.default_content()
        
        except:
            print("send_keys_TinyMCE: FAILED")
            assert False

    def checkNewDicuss(self, index):
        discussName = self.data[index].discuss_subject
        newDiscussBtn = self.driver.find_element(By.XPATH, f"//table//a[contains(text(),\"{discussName}\")]")
        newDiscussBtn.click()

        time.sleep(3)

        newDiscussMessage = self.driver.find_element(By.XPATH, "//div[@class='post-content-container']").text

        if newDiscussMessage == self.data[index].discuss_message:
            print(f'test_{index}: PASSED')
            self.driver.close()
            assert True
            return

        print(f'test_{index}: FAILED')
        self.driver.close()
        assert False

    def test_0(self):
        index = self.getIndexData(0)
        self.gotoWeb(index)
        self.gotoCourse(index)
        self.gotoForum(index)
        self.gotoAddDiscuss(index)  
        
        try:
            # Fill in subject
            subject_input = self.driver.find_element(By.XPATH, "//input[@id=\"id_subject\"]")
            subject_input.send_keys(self.data[index].discuss_subject)

            # Fill in message
            self.send_keys_TinyMCE("//iframe[@id='id_message_ifr']", self.data[index].discuss_message)

            submit_btn = self.driver.find_element(By.XPATH, "//input[@id=\"id_submitbutton\"]")
            submit_btn.click()
            time.sleep(3)

            # Test
            self.checkNewDicuss(index)
        except:
            print("test_0: FAILED")
            self.driver.close()
            assert False
    
    def test_1(self):
        index = self.getIndexData(1)
        self.gotoWeb(index)
        self.gotoCourse(index)
        self.gotoForum(index)
        self.gotoAddDiscuss(index)  
        
        try:
            # Fill in subject
            subjectInput = self.driver.find_element(By.XPATH, "//input[@id=\"id_subject\"]")
            subjectInput.send_keys(self.data[index].discuss_subject)

            # Fill in message
            self.send_keys_TinyMCE("//iframe[@id='id_message_ifr']", self.data[index].discuss_message)

            cancelBtn = self.driver.find_element(By.XPATH, "//button[@id=\"id_cancelbtn\"]")
            cancelBtn.click()

            # Test
            currentUrl = self.driver.current_url
            if "mod/forum" in currentUrl:
                print("test_1: PASSED")
                self.driver.close()
                assert True
                return
            
            print("test_1: FAILED")
            self.driver.close()
            assert False
        except:
            print("test_1: FAILED")
            self.driver.close()
            assert False

    def test_2(self):
        index = self.getIndexData(0)
        self.gotoWeb(index)
        self.gotoCourse(index)
        self.gotoForum(index)
        self.gotoAddDiscuss(index)  
        
        try:
            # Fill in message
            self.send_keys_TinyMCE("//iframe[@id='id_message_ifr']", self.data[index].discuss_message)

            submit_btn = self.driver.find_element(By.XPATH, "//input[@id=\"id_submitbutton\"]")
            submit_btn.click()

            # Test
            self.driver.find_element(By.XPATH, "//*[@id=\"id_error_subject\"]")
            print("test_2: PASSED")
            self.driver.close()
            assert True

        except:
            print("test_2: FAILED")
            self.driver.close()
            assert False

    def test_3(self):
        index = self.getIndexData(0)
        self.gotoWeb(index)
        self.gotoCourse(index)
        self.gotoForum(index)
        self.gotoAddDiscuss(index)  
        
        try:
            # Fill in subject
            subjectInput = self.driver.find_element(By.XPATH, "//input[@id=\"id_subject\"]")
            subjectInput.send_keys(self.data[index].discuss_subject)

            submit_btn = self.driver.find_element(By.XPATH, "//input[@id=\"id_submitbutton\"]")
            submit_btn.click()

            # Test
            self.driver.find_element(By.XPATH, "//*[@id=\"id_error_message\"]")
            print("test_3: PASSED")
            self.driver.close()
            assert True

        except:
            print("test_3: FAILED")
            self.driver.close()
            assert False


def main(out = sys.stderr, verbosity = 2): 
    loader = unittest.TestLoader() 
  
    suite = loader.loadTestsFromModule(sys.modules[__name__]) 
    unittest.TextTestRunner(out, verbosity = verbosity).run(suite) 
      
if __name__ == '__main__': 
    with open('add-a-discuss-in-a-forum-test-result.txt', 'w') as f: 
        main(f) 

# At a basic level, the unittest module works by first assembling a test suite.
# This test suite consists of the different testing methods you defined. 
# Once the suite has been assembled, the tests it contains are executed.
# These two parts of unit testing are separate from each other. 
# The unittest.TestLoader instance created in the solution is used to assemble a test suite.
# The loadTestsFromModule() is one of several methods it defines to gather tests. 
# In this case, it scans a module for TestCase classes and extracts test methods from them.
# The loadTestsFromTestCase() method (not shown) can be used to pull test methods from an 
# individual class that inherits from TestCase.
# The TextTestRunner class is an example of a test runner class. 
# The main purpose of this class is to execute the tests contained in a test suite. 
# This class is the same test runner that sits behind the unittest.main() function.
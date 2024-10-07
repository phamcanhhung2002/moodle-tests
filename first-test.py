from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from data import dataTest_create_a_forum as data

import unittest
import time
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

            loginBtn = self.driver.find_element(By.XPATH, "//*[@id=\"loginbtn\"]")
            loginBtn.click()

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

            time.sleep(2)

            # Access to the course
            try:
                courses = self.driver.find_elements(By.XPATH, "//a[@href and @class='aalink coursename me-2 mb-1']")
                for element in courses:
                    if (self.data[index].course_name in element.get_attribute("innerHTML")):
                        element.click()
                        break

            except:
                print("Course not found!")
                assert False

            # Enable editing mode
            editToggle = self.driver.find_element(By.XPATH, "//form[@class='d-flex align-items-center editmode-switch-form']")
            editToggle.click()
        
        except:
            print("gotoCourse: FAILED")
            assert False

    def gotoForumCreation(self, index = 0):
        try:
            addContentBtn = self.driver.find_element(By.XPATH, "//div[@id='coursecontentcollapse0']/div[last()]//button[@class='btn add-content d-flex justify-content-center align-items-center p-1 icon-no-margin']")
            
            self.driver.execute_script("scroll(0,600)")
            time.sleep(1)

            addContentBtn.click()

            activityOrResourceBtn = self.driver.find_element(By.XPATH, "//div[@id='coursecontentcollapse0']/div[last()]//button[@class=\"section-modchooser section-modchooser-link dropdown-item\"]")
            activityOrResourceBtn.click()
            
            searchInput = self.driver.find_element(By.XPATH, "//input[@class=\"form-control withclear rounded\"]")
            searchInput.send_keys("Forum")
            
            forumBtn = self.driver.find_element(By.XPATH, "//div[@class=\"optionname clamp-2\" and contains(text(), \"Forum\")]")
            forumBtn.click()
        
        except Exception as e:
            print(e)
            print("gotoForumCreation: FAILED")
            assert False

    def getIndexData(self, index = 0):
        for i in range(0, len(self.data)):
            if index == int(self.data[i].test_case):
                return i

    def send_keys_TinyMCE(self, elementId = "", text = ""):
        time.sleep(5)
        try:
            element = ""
            if "//iframe" in elementId:
                element = elementId
            else:
                element = "//iframe[@id='{}']".format(elementId)

            try:
                iframeElement = self.driver.find_element(By.XPATH, element)

                self.driver.switch_to.frame(frame_reference = iframeElement)
        
                self.driver.find_element(By.XPATH, "//body[@id='tinymce']").send_keys(text)
                self.driver.switch_to.default_content()
            except NoSuchElementException:
                self.driver.find_element(By.XPATH, "//textarea[@id='id_introeditor']").send_keys(text)

            self.driver.find_element(By.XPATH, "//input[@id='id_showdescription']").click()

        except Exception as e:
            print(e)
            print("send_keys_TinyMCE: FAILED")
            assert False

    def test_0(self):
        index = self.getIndexData(0)
        self.gotoWeb(index)
        self.gotoCourse(index)

        try:
            self.gotoForumCreation(index)

            # Fill in name
            nameInput = self.driver.find_element(By.XPATH, "//input[@id=\"id_name\"]")
            nameInput.send_keys(self.data[index].forum_name)

            # Fill in description
            self.send_keys_TinyMCE("//iframe[@id='id_introeditor_ifr']", self.data[index].forum_description)

            time.sleep(3)

            submitBtn = self.driver.find_element(By.XPATH, "//input[@id=\"id_submitbutton\"]")
            submitBtn.click()

            # Test
            created_forum_name = self.driver.find_element(By.XPATH, "//h1").text
            created_forum_description = self.driver.find_element(By.XPATH, "//div[@id=\"intro\"]").text
          
            if created_forum_name == self.data[index].forum_name and created_forum_description == self.data[index].forum_description:
                print("test_0: PASSED")
                self.driver.close()
                assert True
                return
            
            print("test_0: FAILED")
            self.driver.close()
            assert False
        except Exception as e:
            print(e)
            print("test_0: FAILED")
            self.driver.close()
            assert False
   
    def test_1(self):
        index = self.getIndexData(1)
        self.gotoWeb(index)
        self.gotoCourse(index)

        try:
            self.gotoForumCreation(index)
            
            # Fill in name
            nameInput = self.driver.find_element(By.XPATH, "//input[@id=\"id_name\"]")
            nameInput.send_keys(self.data[index].forum_name)

            time.sleep(3)

            submitBtn = self.driver.find_element(By.XPATH, "//input[@id=\"id_submitbutton\"]")
            submitBtn.click()

            # Test
            created_forum_name = self.driver.find_element(By.XPATH, "//h1").text
            
            # Check whether new forum has no description
            try:
                self.driver.find_element(By.XPATH, "//div[@id=\"intro\"]").text
            except NoSuchElementException:     
                if created_forum_name == self.data[index].forum_name:
                    print("test_1: PASSED")
                    self.driver.close()
                    assert True
                    return
            
            print("test_1: FAILED")
            self.driver.close()
            assert False
        except Exception as e:
            print(e)
            print("test_1: FAILED")
            self.driver.close()
            assert False

    def test_2(self):
        index = self.getIndexData(2)
        self.gotoWeb(index)
        self.gotoCourse(index)

        try:
            self.gotoForumCreation(index)

            # Fill in name
            nameInput = self.driver.find_element(By.XPATH, "//input[@id=\"id_name\"]")
            nameInput.send_keys(self.data[index].forum_name)

            # Fill in description
            self.send_keys_TinyMCE("//iframe[@id='id_introeditor_ifr']", self.data[index].forum_description)

            time.sleep(3)

            cancelBtn = self.driver.find_element(By.XPATH, "//input[@id=\"id_cancel\"]")
            cancelBtn.click()

            # Test
            currentUrl = self.driver.current_url
            if "course/view" in currentUrl:
                print("test_2: PASSED")
                self.driver.close()
                assert True
                return
            
            print("test_2: FAILED")
            self.driver.close()
            assert False
        except Exception as e:
            print(e)
            print("test_2: FAILED")
            self.driver.close()
            assert False

    def test_3(self):
        index = self.getIndexData(3)
        self.gotoWeb(index)
        self.gotoCourse(index)

        try:
            self.gotoForumCreation(index)

            # Fill in description
            self.send_keys_TinyMCE("//iframe[@id='id_introeditor_ifr']", self.data[index].forum_description)

            time.sleep(3)

            submitBtn = self.driver.find_element(By.XPATH, "//input[@id=\"id_submitbutton\"]")
            submitBtn.click()

            # Test
            self.driver.find_element(By.XPATH, "//*[@id=\"id_error_name\"]")
            
            print("test_3: PASSED")
            self.driver.close()
            assert True
            return
        
        except Exception as e:
            print(e)
            print("test_3: FAILED")
            self.driver.close()
            assert False


def main(out = sys.stderr, verbosity = 2): 
    loader = unittest.TestLoader() 
  
    suite = loader.loadTestsFromModule(sys.modules[__name__]) 
    unittest.TextTestRunner(out, verbosity = verbosity).run(suite) 
      
if __name__ == '__main__': 
    with open('create-a-forum-test-result.txt', 'w') as f: 
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
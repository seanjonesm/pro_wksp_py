from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import time
import datetime

from selenium.webdriver.support.wait import WebDriverWait

# Object model for logging in and out of ePO server
class epoAuthentication(object):

    def __init__(self, driver, report, screenshots):
        self.driver = driver
        self.report = report
        self.screens = screenshots

    def Login(self, language, username, password):

        try:
            self.report.Log('ePO language: ' + language)
            Select(self.driver.find_element_by_id('language')).select_by_value(language)
            time.sleep(5)
            self.driver.find_element_by_id('name').clear()
            self.driver.find_element_by_id('name').send_keys(username)
            self.driver.find_element_by_id('password').clear()
            self.driver.find_element_by_id('password').send_keys(password)
            self.driver.find_element_by_id('login.button').click()
            WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.ID, "mfsLauncher")))
            self.screens.Grab('ePO_Logged_In')
            self.report.Success(name='ePO Login')
        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Failure(name='ePO Login', detail=error)

    def Logoff(self):

        try: 
            self.driver.switch_to.default_content()
            self.driver.find_element_by_css_selector('#mfsUHM').click()
            time.sleep(2)
            self.driver.find_element_by_id('ui.nav.button.logout').click()
            time.sleep(3)
            self.report.Success(name='ePO Logoff')
        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Failure(name='ePO Logoff', detail=e)


# Object model for installing / uninstalling ePO extensions though the UI
class ManageExtensions(object):

    def __init__(self, driver, testReport, screenshots):
        self.driver = driver
        self.report = testReport
        self.screens = screenshots

    def InstallExtension(self, epo_prefix, filepath, extension_id, group_list_id):
        is_extension_installed = 0
        self.driver.get(epo_prefix + '/core/orionNavigationLogin.do#/core/orionTab.do?sectionId=orion.software&tabId=orion.extensions')
        time.sleep(5)
        self.driver.switch_to.frame('mfs-container-iframe')
        self.driver.find_element_by_id(group_list_id).click()
        self.driver.find_element_by_xpath('//*[@id="extension.installpage.button"]').click()
        time.sleep(2)
        self.driver.find_element_by_id('extension.file.input').send_keys(filepath)
        self.driver.find_element_by_id('orion.dialog.box.ok').click()
        self.report.Log('Waiting for extension to install: ' + extension_id)
        WebDriverWait(self.driver, 100).until(ec.visibility_of_element_located((By.XPATH, "//input[@id = 'cancelButton']")))
        self.screens.Grab('install_extension_confirm_' + extension_id)
        self.report.Log('Confirm extension install')
        try:
            if self.driver.find_element_by_xpath("//input[@id = 'okButton'][@class='orionButtonEnabled']"):
                self.driver.find_element_by_xpath("//input[@id = 'okButton']").click()
                is_extension_installed = 1
        except:
            self.driver.find_element_by_xpath("//input[@id = 'cancelButton']").click()
            is_extension_installed = 1
        WebDriverWait(self.driver, 100).until(ec.visibility_of_element_located((By.ID, group_list_id)))
        if is_extension_installed == 1:
            time.sleep(2)
            self.driver.find_element_by_id(group_list_id).click()
        ext_container = self.driver.find_element_by_id('extensionContainer')
        try:
            extension_just_installed = self.driver.find_element_by_xpath("//a[contains(@href,'{}')]".format(extension_id))
            self.report.Success(name='Add extension' + extension_id)
        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Failure(name='Add Extension: ' + extension_id, detail=error)
        time.sleep(10)

    def UninstallExtension(self, epo_prefix, extension_id, group_list_id):
        
        try: 
            self.driver.get(epo_prefix + '/core/orionNavigationLogin.do#/core/orionTab.do?sectionId=orion.software&tabId=orion.extensions')
            time.sleep(5)
            self.driver.switch_to.frame('mfs-container-iframe')
            self.driver.find_element_by_id(group_list_id).click()
            self.driver.find_element_by_xpath("//a[contains(@href,'{}')]".format(extension_id)).click()
            time.sleep(3)
            self.driver.find_element_by_id('extension.remove.force').click()
            self.driver.find_element_by_id('orion.dialog.box.ok').click()
            time.sleep(3)
            self.report.Success(name='Remove extension' + extension_id)
        except Exception as e: 
            error = "Error: {0}".format(str(e))
            self.report.Failure(name='Add Extension: ' + extension_id, detail=error)

        


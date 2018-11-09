__author__ = 'sean_jones@mcafee.com'
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import ePOm as pom
import lqareport as rep
import os, subprocess 
import datetime
import shutil

def main():

    # define the firefox selenium webdriver
    path = "C:\\Automation\\"
    print('Starting Firefox Webdriver')
    driver = webdriver.Firefox(path)
    driver.maximize_window()

    # test paramters
    #languages = ['de', 'en', 'it', 'en_GB', 'pt_BR', 'zh_CN', 'zh_TW', 'fr', 'ja', 'ko', 'ru', 'es', 'tr' ]
    languages = ['de']
    epo_prefix = 'https://eposean2018:8443'

    # Create a new test report object

    if not os.path.exists('C:/Results'):
        os.makedirs('C:/Results')
    else:
        folder = 'C:/Results'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


    if not os.path.exists('C:/Results/Screenshots'):
        os.makedirs('C:/Results/Screenshots')

    scr = rep.Screenshot(driver, 'C:\\Results\\Screenshots\\')
    testReport = rep.TestReport(scr, 'C:/Results/report.xml')

    # define and navigsate to default ePO URL

    for language in languages:

        scr.SetLanguage(language)
        testReport.SetLanguage(language)
        print('Navigating to ePO URL')
        driver.get(epo_prefix + "/core/orionSplashScreen.do")
        # log into ePO
        print('Logging into ePO')
        auth = pom.epoAuthentication(driver, testReport, scr)
        auth.Login(language, 'admin', 'password')
        #install the required extensions
        '''
        ext = pom.ManageExtensions(driver, testReport, scr)
        print('Installing extension: ProtectionWorkspace-services')
        ext.InstallExtension(epo_prefix, filepath='C:\\Automation\\Builds\\ProtectionWorkspace-services.zip', extension_id='ProtectionWorkspace-services', group_list_id='OrionList.item.McAfee.ePolicy Orchestrator')
        print('Installing extension: ProtectionWorkspace')
        ext.InstallExtension(epo_prefix, filepath='C:\\Automation\\Builds\\ProtectionWorkspace.zip', extension_id='ProtectionWorkspace', group_list_id='OrionList.item.McAfee.ePolicy Orchestrator')
        '''
        pw = protectionWorkspaceTasks(driver, testReport, scr, epo_prefix)
        pw.validateInitialScreen()
        #pw.generateEvents()
        #pw.updateEvents()       
        pw.validateThreatOverview()
        pw.validateComplianceOverview()
        pw.validatedExpandedThreatInformation()
        pw.validateEscalations()
        pw.validateSettings()
        
        '''
        ext.UninstallExtension(epo_prefix, extension_id='ProtectionWorkspace', group_list_id='OrionList.item.McAfee.ePolicy Orchestrator')
        ext.UninstallExtension(epo_prefix, extension_id='ProtectionWorkspace-services', group_list_id='OrionList.item.McAfee.ePolicy Orchestrator')
        '''

        auth.Logoff()

        # quit browser
    print('Saving XML report')
    testReport.SaveReport()
    print('Closing Firefox')
    driver.quit()


class protectionWorkspaceTasks(object):

    def __init__(self, driver, testReport, screenshots, epo_prefix):
        self.driver = driver
        self.testReport = testReport
        self.scr = screenshots
        self.epo_prefix = epo_prefix
        self.validateInitialScreen()


    def validateThreatOverview(self):

        try:

            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('mfs-container-iframe')
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-1 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Escalated_Devices_Tooltip')
            self.driver.find_element_by_css_selector('.info-icon-overlay > svg:nth-child(1)').click()
            self.driver.find_element_by_css_selector(
                'pws-overview-row.ng-tns-c14-3:nth-child(3) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > svg:nth-child(1) > rect:nth-child(2)').click()
            self.scr.Grab('PW_Resolved_Threats_Tooltip')
            self.driver.find_element_by_css_selector('.info-icon-overlay > svg:nth-child(1)').click()
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-9 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Unresolved_Threats_Tooltip')
            self.driver.find_element_by_css_selector('.info-icon-overlay > svg:nth-child(1)').click()
      
                        

            print('Test Case: ' + 'Threat Overview' + '- PASS')
            self.testReport.AddTestData('Threat Overview', datetime.datetime.now(), 'PASS')

        except Exception as e:

            print('Test Case: ' + 'Threat Overview' + '- FAIL')
            print(e)
            self.testReport.AddTestData('Threat Overview', datetime.datetime.now(), 'FAIL')


    def validateComplianceOverview(self):

        try:

            self.driver.find_element_by_css_selector('svg.ng-tns-c14-11 > rect:nth-child(2)').click()

            self.scr.Grab('PW_Security_Content_Expanded')
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-11 > rect:nth-child(2)').click()
            self. driver.find_element_by_css_selector(
                'pws-overview-row.ng-tns-c14-13:nth-child(3) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > svg:nth-child(1) > rect:nth-child(2)').click()
            self.scr.Grab('PW_McAfee_Agent_Tooltip')
            self.driver.find_element_by_css_selector('.info-icon-overlay > svg:nth-child(1)').click()
            self.driver.find_element_by_css_selector(
                'pws-overview-row.ng-tns-c14-13:nth-child(3) > div:nth-child(1) > div:nth-child(1) > svg:nth-child(1) > rect:nth-child(2)').click()
            self.scr.Grab('PW_McAfee_Agent_Expanded')
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-16 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Data_Exchange_Layer_Expanded')
            self.driver.find_element_by_css_selector(
                'pws-overview-row.ng-tns-c14-13:nth-child(3) > div:nth-child(1) > div:nth-child(1) > svg:nth-child(1) > rect:nth-child(2)').click()
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-20 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Checkin_Failure_Tooltip')
            self.driver.find_element_by_css_selector('.info-icon-overlay > svg:nth-child(1)').click()
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-22 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Mgd_Devices_Without_Protection_Tooltip')
            self.driver.find_element_by_css_selector('.info-icon-overlay > svg:nth-child(1)').click()
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-24 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Mgd_Devices_Tooltip')
            self.driver.find_element_by_css_selector('.info-icon-overlay > svg:nth-child(1)').click()

            print('Test Case: ' + 'Compliance Overview' + '- PASS')
            self.testReport.AddTestData('Compliance Overview', datetime.datetime.now(), 'PASS')


        except Exception as e:
            print('Test Case: ' + 'Compliance Overview' + '- FAIL')
            print(e)
            self.testReport.AddTestData('Compliance Overview', datetime.datetime.now(), 'FAIL')



    def validatedExpandedThreatInformation(self): 
        
        try:
            self.driver.refresh()
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('mfs-container-iframe')
            time.sleep(3)
            self.driver.find_element_by_xpath('//div[contains(@class, "ng-tns-c25-2")]').click()
            self.scr.Grab('PW_Escalated_Devices_Expanded')
            self.driver.find_element_by_css_selector('div.totalizer-counter:nth-child(1) > div:nth-child(1) > div:nth-child(1)').click()
            time.sleep(5)
            self.driver.find_element_by_xpath('//div[contains(@class, "ng-tns-c25-32")]').click()
            self.scr.Grab('PW_Resolved_Threats_Expanded')
            self.driver.find_element_by_css_selector('div.totalizer-counter:nth-child(1) > div:nth-child(1) > div:nth-child(1)').click()
            time.sleep(5)
            self.driver.find_element_by_xpath('//div[contains(@class, "ng-tns-c25-62")]').click()
            self.scr.Grab('PW_Resolved_Threats_Advanced_Expanded')
            self.driver.find_element_by_css_selector('div.totalizer-counter:nth-child(1) > div:nth-child(1) > div:nth-child(1)').click()
            time.sleep(5)       
            self.driver.find_element_by_xpath('//div[contains(@class, "ng-tns-c25-92")]').click()
            self.scr.Grab('PW_Resolved_Threats_Basic_Expanded')
            self.driver.find_element_by_css_selector('div.totalizer-counter:nth-child(1) > div:nth-child(1) > div:nth-child(1)').click()
            time.sleep(5)
            
            try:
                self.driver.find_element_by_xpath('//div[contains(@class, "ng-tns-c25-122")]').click()
                self.scr.Grab('PW_UnResolved_Threats_Expanded')
                self.driver.find_element_by_css_selector('div.totalizer-counter:nth-child(1) > div:nth-child(1) > div:nth-child(1)').click()
            
            except Exception as e: 
                print("Unresolved Threats not applicable")

            print('Test Case: ' + 'Expanded Threat Informaiton' + '- PASS')
            self.testReport.AddTestData('Expanded Threat Information', datetime.datetime.now(), 'PASS')


        except Exception as e:
            print('Test Case: ' + 'Expanded Threat Informaiton' + '- FAIL')
            print(e)
            self.testReport.AddTestData('Expanded Threat Informaiton', datetime.datetime.now(), 'FAIL')


    def validateEscalations(self):

        try:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('mfs-container-iframe')
            self.driver.find_element_by_css_selector('div.totalizer-counter:nth-child(2) > div:nth-child(1)').click()
            self.scr.Grab('PW_Escalations')
            self.driver.find_element_by_xpath('//div[contains(@class, "table-content-body")]/table/tbody/tr[1]/td[2]').click()
            self.scr.Grab('PW_Escalated_Device_Expanded')
            self.driver.find_element_by_xpath('//span[contains(@class, "lsg-dropdown-list-primary")]').click()
            self.scr.Grab('PW_Escalated_Dropdown')
            self.driver.find_element_by_xpath('//span[contains(@class, "lsg-dropdown-list-primary")]//ul[1]/li[1]').click()
            self.scr.Grab('PW_Exclude_Device_From_Compliance_Overview')
            self.driver.find_element_by_xpath('//button[contains(@class, "lsg-btn-secondary")]').click()
            self.driver.find_element_by_xpath('//span[contains(@class, "lsg-dropdown-list-primary")]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//span[contains(@class, "lsg-dropdown-list-primary")]//ul[1]/li[2]').click()
            self.scr.Grab('PW_Remove_Device_From_Escalations')
            self.driver.find_element_by_xpath('//button[contains(@class, "lsg-btn-secondary")]').click()
            self.driver.find_element_by_xpath('//pws-device-details/div/h2').click()
            self.scr.Grab('PW_Escalated_Device_Details')


            print('Test Case: ' + 'Escalations' + '- PASS')
            self.testReport.AddTestData('Escalations', datetime.datetime.now(), 'PASS')


        except Exception as e:

            print('Test Case: ' + 'Escalations' + '- FAIL')
            print(e)
            self.testReport.AddTestData('Escalations', datetime.datetime.now(), 'FAIL')


    def validateSettings(self):

        try:
            self.driver.find_element_by_css_selector('#settings').click()
            self.scr.Grab('PW_Settings')

            print('Test Case: ' + 'Settings' + '- PASS')
            self.testReport.AddTestData('Settings', datetime.datetime.now(), 'PASS')

        except Exception as e:

            print('Test Case: ' + 'Settings' + '- FAIL')
            print(e)
            self.testReport.AddTestData('Settings', datetime.datetime.now(), 'FAIL')

    def validateInitialScreen(self):

        try:
            self.driver.get(self.epo_prefix + "/core/orionNavigationLogin.do#/ProtectionWorkspace/html/")
            self.scr.Grab('PW_Initial')

            print('Test Case: ' + 'Initial Screen' + '- PASS')
            self.testReport.AddTestData('Initial Screen', datetime.datetime.now(), 'PASS')

        except Exception as e:
            print('Test Case: ' + 'Initial Screen' + '- FAIL')
            print(e)
            self.testReport.AddTestData('Initial Screen', datetime.datetime.now(), 'FAIL')


    def generateEvents(self): 

        try: 
            print('Starting event generation')
            os.system('C:\\Automation\\SimAgentWhite\\simagent_white.exe')
            print('Completed event generaiton')
  
        except Exception as e: 
            print(e)
    
    def updateEvents(self): 

        try: 
            time.sleep(15)
            self.driver.switch_to.frame('mfs-container-iframe')
            self.driver.find_element_by_id('update-now').click()
            time.sleep(5)
            self.scr.Grab('PW_Initial_WithEvents')

            print('Test Case: ' + 'Update Events' + '- PASS')
            self.testReport.AddTestData('Update Events', datetime.datetime.now(), 'PASS')

        except Exception as e: 
            print('Test Case: ' + 'Update Events' + '- FAIL')
            print (e)
            self.testReport.AddTestData('Update Events', datetime.datetime.now(), 'FAIL')


if __name__ == '__main__': main()
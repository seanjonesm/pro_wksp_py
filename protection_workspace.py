from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import os, subprocess
import datetime
import shutil
from selenium.webdriver.common.action_chains import ActionChains



class ProtectionWorkspaceTasks(object):

    def __init__(self, driver, report, screenshots, epo_prefix):
        self.driver = driver
        self.report = report
        self.scr = screenshots
        self.epo_prefix = epo_prefix
        self.ValidateInitialScreen()

    #Validates the Threat Overview pane within the Protection Workspace dashboard
    def ValidateThreatOverview(self):

        try:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('mfs-container-iframe')
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-1 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Escalated_Devices_Tooltip')
            self._CollapseToolTip()
            self.driver.find_element_by_css_selector(
                'pws-overview-row.ng-tns-c14-3:nth-child(3) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > svg:nth-child(1) > rect:nth-child(2)').click()
            self.scr.Grab('PW_Resolved_Threats_Tooltip')
            self._CollapseToolTip()
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-9 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Unresolved_Threats_Tooltip')
            self._CollapseToolTip()
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-26 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Report_Only_Detections_Tooltip')
            self._CollapseToolTip()
            self.report.Success(name='Threat Overview')
        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Failure(name='Threat Overview', detail=error)

    # Validates the Compliance Overview pane within the Protection Workspace dashboard
    def ValidateComplianceOverview(self):

        try:
            #self.driver.find_element_by_css_selector('svg.ng-tns-c14-11 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Security_Content_Expanded')
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-28 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Windows_Defender_Tooltop')
            self._CollapseToolTip()
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-11 > rect:nth-child(2)').click()
            self.driver.find_element_by_css_selector(
                'pws-overview-row.ng-tns-c14-13:nth-child(3) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > svg:nth-child(1) > rect:nth-child(2)').click()
            self.scr.Grab('PW_McAfee_Agent_Tooltip')
            self._CollapseToolTip()
            self.driver.find_element_by_css_selector(
                'pws-overview-row.ng-tns-c14-13:nth-child(3) > div:nth-child(1) > div:nth-child(1) > svg:nth-child(1) > rect:nth-child(2)').click()
            self.scr.Grab('PW_McAfee_Agent_Expanded')
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-16 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Data_Exchange_Layer_Expanded')
            self.driver.find_element_by_css_selector(
                'pws-overview-row.ng-tns-c14-13:nth-child(3) > div:nth-child(1) > div:nth-child(1) > svg:nth-child(1) > rect:nth-child(2)').click()
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-20 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Checkin_Failure_Tooltip')
            self._CollapseToolTip()
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-22 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Mgd_Devices_Without_Protection_Tooltip')
            self._CollapseToolTip()
            self.driver.find_element_by_css_selector('svg.ng-tns-c14-24 > rect:nth-child(2)').click()
            self.scr.Grab('PW_Mgd_Devices_Tooltip')
            self._CollapseToolTip()
            self.report.Success(name='Compliance Overview')

        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Failure(name='Compliance Overview', detail=error)

    # Common function for collapse any expanded tooltip on the Protection Workspace dashboard
    def _CollapseToolTip(self):

        try:
            self.driver.find_element_by_css_selector('.info-icon-overlay > svg:nth-child(1)').click()
        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Log(error)

    # Validates the  exanded information for each item on the Thread Overview pane
    def ValidateExpandedThreatInformation(self):

        try:
            self.driver.refresh()
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('mfs-container-iframe')
            self._CollapseThreatInformation()
            time.sleep(5)
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(self.driver.find_element_by_tag_name('body'), 0,0)
            actions.move_by_offset(294, 358).click().perform()
            #self.driver.find_element_by_css_selector('div.ng-tns-c25-4:nth-child(1)').click() -
            time.sleep(3)
            self.scr.Grab('PW_Escalated_Devices_Expanded')
            self._CollapseThreatInformation()
            '''
            self.driver.find_element_by_xpath('//div[contains(@class, "ng-tns-c25-2")]').click()
            self.scr.Grab('PW_Escalated_Devices_Expanded')         
            self._CollapseThreatInformation()
            self.driver.find_element_by_xpath('//div[contains(@class, "ng-tns-c25-45")]').click()
            self.scr.Grab('PW_Resolved_Threats_Expanded')
            self._CollapseThreatInformation()
            self.driver.find_element_by_xpath('//div[contains(@class, "ng-tns-c25-88")]').click()
            self.scr.Grab('PW_Resolved_Threats_Advanced_Expanded')
            self._CollapseThreatInformation()
            self.driver.find_element_by_xpath('//div[contains(@class, "ng-tns-c25-131")]').click()
            self.scr.Grab('PW_Resolved_Threats_Basic_Expanded')
            self._CollapseThreatInformation()
            try:
                self.driver.find_element_by_xpath('//div[contains(@class, "ng-tns-c25-174")]').click()
                self.scr.Grab('PW_UnResolved_Threats_Expanded')
                self._CollapseThreatInformation()
            except Exception as e:
                self.report.Log("Unresolved Threats not applicable")
            '''
            self.report.Success(name='Expanded Threat Information')
        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Failure(name='Expanded Threat Information', detail=error)

    # Common function to collapse threat detailed information
    def _CollapseThreatInformation(self): 

        try:
            self.driver.find_element_by_css_selector('div.totalizer-counter:nth-child(1)').click()
        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Log(error)

    # Validates the escalated devices side pane
    def ValidateEscalations(self):

        try:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('mfs-container-iframe')
            self.driver.find_element_by_css_selector('div.totalizer-counter:nth-child(2) > div:nth-child(1)').click()
            self.scr.Grab('PW_Escalations')
            self.driver.find_element_by_xpath(
                '//div[contains(@class, "table-content-body")]/table/tbody/tr[1]/td[2]').click()
            self.scr.Grab('PW_Escalated_Device_Expanded')
            time.sleep(3)
            self.driver.find_element_by_xpath('//span[contains(@class, "lsg-dropdown-list-primary")]').click()
            self.scr.Grab('PW_Escalated_Dropdown')
            self.driver.find_element_by_xpath(
                '//span[contains(@class, "lsg-dropdown-list-primary")]//ul[1]/li[1]').click()
            self.scr.Grab('PW_Exclude_Device_From_Compliance_Overview')
            self.driver.find_element_by_xpath('//button[contains(@class, "lsg-btn-secondary")]').click()
            self.driver.find_element_by_xpath('//span[contains(@class, "lsg-dropdown-list-primary")]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//span[contains(@class, "lsg-dropdown-list-primary")]//ul[1]/li[2]').click()
            self.scr.Grab('PW_Remove_Device_From_Escalations')
            self.driver.find_element_by_xpath('//button[contains(@class, "lsg-btn-secondary")]').click()
            self.driver.find_element_by_xpath('//pws-device-details/div/h2').click()
            self.scr.Grab('PW_Escalated_Device_Details')
            self.report.Success(name='Escalations')
        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Failure(name='Escalations', detail=error)

    # Validates the Settings pane
    def ValidateSettings(self):

        try:
            self.driver.find_element_by_css_selector('#settings').click()
            self.scr.Grab('PW_Settings')
            self.report.Success(name='Settings')
        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Failure(name='Settings', detail=error)

    # Captures the initial screen when the Protection Workspace tab is open
    def ValidateInitialScreen(self):

        try:
            self.driver.get(self.epo_prefix + "/core/orionNavigationLogin.do#/ProtectionWorkspace/html/")
            self.scr.Grab('PW_Initial')
            self.report.Success(name='Initial Screen')
        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Failure(name='Initial Screen', detail=error)

    # Calls the SimAgent automation exe which subsequently generates events for ePO
    def GenerateEvents(self, path_to_simagent_automation):

        try:
            self.report.Log('Starting event generation')
            scriptList = ['CreateAgentOnce.scp', 'PWSendEndpointTpWcPropsBase.scp', 'SendEpoEventwithDiffrent.scp']
            agentCountList = [17, 17, 6]
            elementCount = 0
            for script in scriptList:
                cmd = path_to_simagent_automation + ' ' + script + ' ' + str(agentCountList[elementCount]) + ' ' + str(elementCount)
                os.system(cmd)
                elementCount += 1
            self.report.Log('Completed event generation')
        except Exception as e:
            self.report.Log(e)
            
    # Update the Protection Workspace dashboard and waits a set time for the events to propagate though
    def UpdateEvents(self):

        try:
            self.report.Log('Waiting 1.5 minutes to allow events to propagate')
            time.sleep(90)
            self.driver.refresh()
            time.sleep(5)
            self.scr.Grab('PW_Initial_WithEvents')
            self.report.Success(name='Updated Events')
        except Exception as e:
            error = "Error: {0}".format(str(e))
            self.report.Failure(name='Update Events', detail=error)

__author__ = 'sean_jones@mcafee.com'
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import ePOm as pom
import pyakeso as akeso
import protection_workspace as tasks
import os, subprocess
import datetime
import shutil


def main():
    # Create a utilities instance
    util = akeso.Utilities()
    # Import the locales list from the XML config
    locales = util.GetLocaleListFromConfig('C:\\Automation\\Automation\\config.xml')
    # Define the ePO URL prefix - to be added in config file once Akeso supports it
    epo_prefix = 'https://localhost:8443'
    # Define the local path to SIMAgent Automation exe for events generation
    path_to_simagent_automation = 'C:\\Automation\\Automation\\SimAgentWhite\\simagent_white.exe'
    # define the firefox selenium webdriver
    print('----Starting Firefox Webdriver----')
    driver = webdriver.Firefox()
    driver.maximize_window()
    # Prepare test environemnt and create required folders required for reporting and screenshots
    PrepareEnvironment()
    # Create a new instance of the screenshot handler object
    screenshots = akeso.Screenshot(driver, 'C:\\Results\\Screenshots\\')
    # Create a new instance of the XML report handler object
    report = akeso.TestReport(screenshots, 'C:/Results/Report/report.xml', locales)
    # Create boolean flag to indicate whether extensions installed
    extensions_installed = False 
    # Create boolean flag to indicate event generaiton
    events_generated = False
    locale_count = 0
    for loc in locales:
        locale_count += 1
        # Set locale for screenshots and report
        screenshots.SetLocale(loc)
        report.LocaleSetup(loc)
        # Go to ePO URL
        report.Log('Navigating to ePO URL: ' + epo_prefix)
        driver.get(epo_prefix + "/core/orionSplashScreen.do")
        # Log into ePO
        report.Log('Logging into ePO')
        # Login using default username and password for current locale
        auth = pom.epoAuthentication(driver, report, screenshots)
        auth.Login(loc, 'admin', 'password') 
        # Install the required extensions if current locale is the first to be tested
        if (extensions_installed == False):
            ext = pom.ManageExtensions(driver, report, screenshots)
            report.Log('Installing extension: MVISION bundle and verify that ProtectionWorkspace has been installed')
            ext.InstallExtension(epo_prefix,
                                 filepath='C:\\Automation\\Builds\\MVISION_Endpoint_bundled_ePO_extensions.zip',
                                 extension_id='ProtectionWorkspace',
                                 group_list_id='OrionList.item.McAfee.ePolicy Orchestrator')
            extensions_installed = True
        # Create new instance of Protection Workspace test suite
        pw = tasks.ProtectionWorkspaceTasks(driver, report, screenshots, epo_prefix)
        # Generate/Update SIMAgent events only if current locale is the first to be tested
        if (events_generated == False):
            pw.GenerateEvents(path_to_simagent_automation)
            pw.UpdateEvents()
            events_generated = True
        # Proceed with the remaining Protection Workspace test cases
        pw.ValidateThreatOverview()
        pw.ValidateComplianceOverview()
        pw.ValidateEscalations()
        pw.ValidateSettings()
        #pw.ValidateExpandedThreatInformation()
        # Uninstall the required extensions if current locale is the last to be tested
        if locale_count == int(len(locales)):
            ext.UninstallExtension(epo_prefix, extension_id='ProtectionWorkspace',
                                   group_list_id='OrionList.item.McAfee.ePolicy Orchestrator')
            ext.UninstallExtension(epo_prefix, extension_id='ProtectionWorkspace-services',
                                   group_list_id='OrionList.item.McAfee.ePolicy Orchestrator')
        # Log off from ePO server
        auth.Logoff()
        # Carry out some reporting admin for current locale
        report.LocaleTeardown()
    # Save Report
    report.Log('Saving XML report')
    report.SaveReport()
    # Close Browser
    report.Log('Closing Firefox')
    driver.quit()

# PrepareEnvironment() creates the folder structure required for test reporting and screenshot archiving
def PrepareEnvironment():
    print('----Preparing environment----')
    if not os.path.exists('C:/Results'):
        os.makedirs('C:/Results')
        os.makedirs('C:/Results/Report')
    else:
        folder = 'C:/Results'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    if not os.path.exists('C:/Results/Screenshots'):
        os.makedirs('C:/Results/Screenshots')
    if not os.path.exists('C:/Results/Report'):
        os.makedirs('C:/Results/Report')

if __name__ == '__main__': main()

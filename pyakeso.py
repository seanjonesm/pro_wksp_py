from xml.dom import minidom
import os
import datetime
import time
import lxml.etree as etree

class TestReport(object):

    def __init__(self, scr, save_path_file, locales):
        # Define class properties and create an XML file template
        self.util = Utilities()
        self.save_path_file = save_path_file
        self.logfile = open(save_path_file[:-3] + 'log', "w+")
        self.scr = scr
        self.scr.EnableLogging(self)
        self.count_passed_loc = 0
        self.count_failed_loc = 0
        self.count_passed_total = 0
        self.count_failed_total = 0
        self.root = minidom.Document()
        self.xml = self.root.createElement('Report')
        self.root.appendChild(self.xml)
        self.start_time = self.util.CurrentTime()
        self.loc_start_time = self.util.CurrentTime()
        self.indiv_start_time = self.util.CurrentTime()
        self.current_locale = 'undefined'
        self.locales = locales  
        self.TestRun = self._AddXMLHeaders()
        self.TestPass = None
        self.ResultList = None

    # Fuction to add a PASS test case entry to report
    def Success(self, **kwargs):

        name = kwargs.pop('name', '')
        detail = kwargs.pop('detail', '')
        note = kwargs.pop('note', '')
        self._AddTestData(name, detail, note, 'PASS')
        self.Log('PASS - ' + name + ' | ' + detail + ' | ' + note)

    # Fuction to add a FAIL test case entry to report
    def Failure(self, **kwargs):

        name = kwargs.pop('name', '')
        detail = kwargs.pop('detail', '')
        note = kwargs.pop('note', '')
        self._AddTestData(name, detail, note, 'FAIL')
        self.Log('FAIL - ' + name + ' | ' + detail + ' | ' + note)

    # Function to save XML report to file
    def SaveReport(self):

        self._ReturnOverallResults()
        xml_str = self.root.toprettyxml(indent="\t")
        with open(self.save_path_file, "w+") as f:
            f.write(xml_str)

    # Function to add summary information to report at the beginning of each locale run
    def LocaleSetup(self, locale):

        self.current_locale = locale
        self.start_time_loc = self.util.CurrentTime()
        self.count_passed_loc = 0
        self.count_failed_loc = 0
        TestPass = self._CreateChildNode(self.TestRun, 'TestPass')
        self.TestPass = TestPass
        self._AddChildNodeEmptyValue(self.TestPass, 'TestPassID')
        self._AddChildNodeEmptyValue(self.TestPass, 'ReportID')
        self._AddChildNodeEmptyValue(self.TestPass, 'DeviceOSID')
        self._AddChildNodeEmptyValue(self.TestPass, 'ProductID')
        self._AddChildNodeEmptyValue(self.TestPass, 'SystemOS')
        self._AddChildNodeEmptyValue(self.TestPass, 'SystemBrowser')
        self._AddChildNodeEmptyValue(self.TestPass, 'TestProducts')
        self._AddChildNodeEmptyValue(self.TestPass, 'TestAccounts')
        ResultList = self._CreateChildNode(TestPass, 'ResultList')
        self.ResultList = ResultList

    # Function to add summary information to report at the end of each locale run
    def LocaleTeardown(self): 

        self._AddChildNodeWithValue(self.TestPass, 'TestPassStartTime', str(self._ReturnLocStartTime()))
        self._AddChildNodeWithValue(self.TestPass, 'TestPassEndTime', str(self.util.CurrentTime()))
        self._AddChildNodeWithValue(self.TestPass, 'TestPassedCount', str(self._ReturnLocPassedCount()))
        self._AddChildNodeWithValue(self.TestPass, 'TestsFailedCount', str(self._ReturnLocFailedCount()))
        self._AddChildNodeWithValue(self.TestPass, 'TestsUnknownCount', str(0))
        self._AddChildNodeWithValue(self.TestPass, 'ScreenCount', str(self.scr.ReturnLocaleScreenshotCount()))

    # Function to write to the debug log file
    def Log(self, message):

        lmsg = '[' + str(self.util.CurrentTime()) + '][' + self.util.ConvertLocaleCode(self.current_locale, False) + '] ' + message
        print(lmsg)
        self.logfile.write(lmsg + '\n')

    # Internal function to add summary information to report before any tests begin
    def _AddXMLHeaders(self):
        
        TestLocaleList = self._CreateChildNode(self.xml, 'TestLocaleList')
        for loc in self.locales:
            lc = self.util.ConvertLocaleCode(loc, True)
            ReportLocale = self._CreateChildNode(TestLocaleList, 'ReportLocale')
            self._AddChildNodeWithValue(ReportLocale, 'LocaleID', str(0))
            self._AddChildNodeWithValue(ReportLocale, 'Language', lc[0])
            self._AddChildNodeWithValue(ReportLocale, 'Country', lc[1])
            self._AddChildNodeWithValue(ReportLocale, 'Separator', '_')
        TestRun = self._CreateChildNode(self.xml, 'TestRun')
        return TestRun

    # Internal function to add a new test case results entry
    def _AddTestData(self, name, detail, note, result):

        _starttime = self.indiv_start_time
        _endtime = self.util.CurrentTime()
        Test = self._CreateChildNode(self.ResultList, 'Test')
        self._AddChildNodeWithValue(Test, 'TestID', str(0))
        self._AddChildNodeWithValue(Test, 'TestPassID', str(0))
        self._AddChildNodeWithValue(Test, 'LocaleID', str(0))
        self._AddChildNodeWithValue(Test, 'Name', str(name))
        Locale = self._CreateChildNode(Test, 'Locale')
        lc = self.util.ConvertLocaleCode(self.current_locale, True)
        self._AddChildNodeWithValue(Locale, 'LocaleID', str(0))
        self._AddChildNodeWithValue(Locale, 'Language', lc[0])
        self._AddChildNodeWithValue(Locale, 'Country', lc[1])
        self._AddChildNodeWithValue(Locale, 'Separator', '_')
        self._AddChildNodeWithValue(Test, 'Result', str(result))
        self._AddChildNodeWithValue(Test, 'Detail', str(detail))
        self._AddChildNodeWithValue(Test, 'StartTime', str(_starttime))
        self._AddChildNodeWithValue(Test, 'EndTime', str(_endtime))
        self._AddChildNodeWithValue(Test, 'ScreenCount', str(self.scr.ReturnIndividualScreenshotCount()))
        self._AddChildNodeEmptyValue(Test, 'KeyScreens')
        self._AddChildNodeEmptyValue(Test, 'TestProgress')
        self._AddChildNodeWithValue(Test, 'Note', str(note))
        if result == 'PASS':
            self.count_passed_loc += 1
            self.count_passed_total += 1
        else:
           self.count_failed_loc += 1
           self.count_failed_total += 1
        self.scr.ResetIndividualScreenshotCount()
        self.indiv_start_time = _endtime

    # Internal function to summerise test case results at the end of a test run
    def _ReturnOverallResults(self):

        _starttime = self.start_time
        _endtime = self.util.CurrentTime()
        self._AddChildNodeWithValue(self.xml, 'TestCasePassed', str(self._ReturnTotalPassedCount()))
        self._AddChildNodeWithValue(self.xml, 'TestCaseFailed', str(self._ReturnTotalFailedCount()))
        self._AddChildNodeWithValue(self.xml, 'ScreenCaptureTotal', str(self.scr.ReturnTotalScreenshotCount()))
        self._AddChildNodeWithValue(self.xml, 'StartTIme', str(_starttime))
        self._AddChildNodeWithValue(self.xml, 'EndTime', str(_endtime))
        self._AddChildNodeWithValue(self.xml, 'ExistingTestID', str(0))
        self._AddChildNodeWithValue(self.xml, 'ReportID', str(0))
        self._AddChildNodeWithValue(self.xml, 'TestsUnknownCount', str(0))

    # Internal function to return total passed test case count
    def _ReturnTotalPassedCount(self):
        return self.count_passed_total

    # Internal function to return total failed test case count
    def _ReturnTotalFailedCount(self):
        return self.count_failed_total

    # Internal function to return total passed test case count per locale
    def _ReturnLocPassedCount(self):
        return self.count_passed_loc

    # Internal function to return total failed test case count per locale
    def _ReturnLocFailedCount(self):
        return self.count_failed_loc

    # Internal function to return test run start time
    def _ReturnLocStartTime(self):
        return self.loc_start_time

    # Internal function to generate a new XML node and return 
    def _CreateChildNode(self, parent, name):

        child = self.root.createElement(name)
        parent.appendChild(child)
        return child

    # Internal function to generate a new XML node with a defined test value
    def _AddChildNodeWithValue(self, parent, name, value):

        child = self.root.createElement(name)
        if(len(value) > 0):
            child.appendChild(self.root.createTextNode(value))
        parent.appendChild(child)

    # Internal function to generate a new XML node with a blank value
    def _AddChildNodeEmptyValue(self, parent, name):

        child = self.root.createElement(name)
        parent.appendChild(child)

class Screenshot(object):

    def __init__(self, driver, filePath):
        # Define class properties
        self.util = Utilities()
        self.driver = driver
        self.filePath = os.path.abspath(filePath)
        self.total_screenshot_count = 0
        self.loc_screenshot_count = 0
        self.indiv_screenshot_count = 0
        self.current_locale = 'undefined'
        self.report = None

    # Function to take a screenshot and save to file
    def Grab(self, screenshotName):

        self.report.Log('Taking screenshot: ' + screenshotName)
        time.sleep(3)
        self.driver.get_screenshot_as_file(self.filePath + '/' + screenshotName + '.png')
        self.report.Log('Saving image... ' + self.filePath + '/' + screenshotName + '.png')
        self.indiv_screenshot_count += 1
        self.loc_screenshot_count += 1
        self.total_screenshot_count += 1

    # Function to define current locale being tested
    def SetLocale(self, locale):
        self.current_locale = locale
        self.loc_screenshot_count = 0
        folder_name = self.util.ConvertLocaleCode(self.current_locale, False)
        if not os.path.exists(f'C:/Results/Screenshots/{folder_name}'):
            os.makedirs(f'C:/Results/Screenshots/{folder_name}')
            self.filePath = f'C:/Results/Screenshots/{folder_name}'

    # Function to return screenshot count per test case
    def ReturnIndividualScreenshotCount(self):
        return self.indiv_screenshot_count

    # Function to reset screenshot count per test case to zero
    def ResetIndividualScreenshotCount(self):
        self.indiv_screenshot_count = 0

    # Function to return screenshot count per locale
    def ReturnLocaleScreenshotCount(self):
        return self.loc_screenshot_count

    # Function to reset screenshot count per locale to zero
    def ResetLocaleScreenshotCount(self):
        self.loc_screenshot_count = 0

    # Function to return total screenshot count for the test run
    def ReturnTotalScreenshotCount(self): 
        return self.total_screenshot_count

    # Function to pass the current reporting object this class allowing debug logging during screenshot handling
    def EnableLogging(self, report): 
        self.report = report

class Utilities(object):

    # Function to return locales in list format from Akeso config file
    def GetLocaleListFromConfig(self, path): 

        config = etree.parse(path)
        locales = config.xpath("//Configuration/LanguageList/Setting/@Name")    
        return locales

    # Function to convert automation code to report / SORT codes
    def ConvertLocaleCode(self, locale_code, should_split): 

        switcher = {
            "nl":"nl_NL", 
            "en":"en_US", 
            "fr":"fr_FR", 
            "de":"de_DE", 
            "he":"he_IL",
            "it":"it_IT", 
            "ja":"ja_JP", 
            "ko":"ko_KR",
            "pl":"pl_PL", 
            "pt_BR":"pt_BR", 
            "ru":"ru_RU", 
            "zh_CN":"zh_CN",
            "es":"es_ES", 
            "sv":"sv_SE", 
            "zh_TW":"zh_TW"
        }
        if(should_split == True): 
            report_code = (switcher.get(locale_code)).split("_")
        else: 
            report_code = switcher.get(locale_code)
        return report_code

    # Function to return current time in DD/MM/YY HH:MM:SS format
    def CurrentTime(self): 

        time = f'{datetime.datetime.now():%d/%m/%Y %H:%M:%S%z}'
        return time 


  

   

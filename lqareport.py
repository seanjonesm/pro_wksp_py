
from xml.dom import minidom
import os
import time

class TestReport(object):

    def __init__(self, scr, save_path_file):
        self.save_path_file = save_path_file
        self.scr = scr
        self.countPassed = 0
        self.countFailed = 0
        self.root = minidom.Document()
        self.xml = self.root.createElement('root')
        self.root.appendChild(self.xml)
        self.language = 'undefined'


    def AddTestData(self, name, timeStamp, result):

        testResult = self.root.createElement(('Test'))
        self.xml.appendChild(testResult)

        resultDetails = self.root.createElement('Result')
        resultDetails.appendChild(self.root.createTextNode(str(result)))
        testResult.appendChild(resultDetails)

        resultDetails = self.root.createElement('Name')
        resultDetails.appendChild(self.root.createTextNode(str(name)))
        testResult.appendChild(resultDetails)

        resultDetails = self.root.createElement('Locale')
        resultDetails.appendChild(self.root.createTextNode(str(self.language)))
        testResult.appendChild(resultDetails)

        resultDetails = self.root.createElement('TimeStamp')
        resultDetails.appendChild(self.root.createTextNode(str(timeStamp)))
        testResult.appendChild(resultDetails)

        numScr = self.scr.ReturnIndividualTestCount()

        resultDetails = self.root.createElement('ScreenCount')
        resultDetails.appendChild(self.root.createTextNode(str(numScr)))
        testResult.appendChild(resultDetails)

        self.scr.ResetIndividualTestCount()

        if result == 'PASS':
            self.countPassed += 1
        else:
            self.countFailed += 1


    def SaveReport(self):

        xml_str = self.root.toprettyxml(indent="\t")
        with open(self.save_path_file, "w+") as f:
            f.write(xml_str)

    def SetLanguage(self, language):
        self.language = language

    def ReturnPassedCount(self):
        return self.countFailed

    def ReturnFailedCount(self):
        return self.countPassed


    def ReturnOverallResults(self):

        return None
        overallResult = self.root.createElement(('TestCasePassed'))
        overallResult.createTextNode(str(self.ReturnPassedCount()))
        self.root.appendChild(overallResult)
        overallResult = self.root.createElement(('TestCaseFailed'))
        overallResult.createTextNode(str(self.ReturnFailedCount()))
        self.root.appendChild(overallResult)



class Screenshot(object):

    def __init__(self, driver, filePath):
        self.driver = driver
        self.filePath = os.path.abspath(filePath)
        self.totalCount = 0
        self.individalTestCount = 0
        self.language = 'undefined'

    def Grab(self, screenshotName):

        print('Taking screenshot: ' + screenshotName)
        time.sleep(3)
        self.driver.get_screenshot_as_file(self.filePath + '/' + screenshotName + '.png')
        print('Saving image... ' + self.filePath + '/' + screenshotName + '.png')
        self.individalTestCount += 1

    def SetLanguage(self, language):
        self.language = language
        if not os.path.exists(f'C:/Results/Screenshots/{self.language}'):
            os.makedirs(f'C:/Results/Screenshots/{self.language}')
            self.filePath = f'C:/Results/Screenshots/{self.language}'

    def ReturnIndividualTestCount(self):
        return self.individalTestCount

    def ResetIndividualTestCount(self):
        self.individalTestCount = 0

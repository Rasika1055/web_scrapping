from selenium import webdriver 
from selenium.webdriver.common.by import By
import pandas as pd
import requests
from bs4 import BeautifulSoup

url='https://www.cermati.com/karir/lowongan'
driver=webdriver.Chrome()
driver.get(url)

class JobKeys:
    """
        Basic job keys
    """
    LOCATION = "location"
    TITLE = "title"
    SUBTITLE = "subtitle"
    JOB_TYPE = "job_type"
    URL = "url"


class BaseJobClass:
    """
        Basic Job Class
    """
    def __init__(self, kwargs):
        self.title = kwargs.get(JobKeys.TITLE)
        self.subtitle = kwargs.get(JobKeys.SUBTITLE)
        self.url = kwargs.get(JobKeys.URL)
        self.location = kwargs.get(JobKeys.LOCATION)
        self.job_type = kwargs.get(JobKeys.JOB_TYPE)
    
    def get_json(self):
        return self.__dict__

def getDetails(name):
    """
        Fetches location and department keys
    """
    arr =[]
    for each in driver.find_elements(By.NAME, name):
        for htm in each.find_elements(By.TAG_NAME,'option'):
            arr.append(htm.text)
    return arr

def gatherJobListWrapper(wrapperClass="page-job-list-wrapper"):
    

    for wrapper in driver.find_elements(By.CLASS_NAME, wrapperClass):

        jobDic = {}
        for jobDetailHtml in wrapper.find_elements(By.CLASS_NAME, "job-detail"):
            
            if jobDetailHtml.tag_name == "div":
                
                if "jobs-location-wrapper" in jobDetailHtml.get_dom_attribute("class"):
                    #print("Job location: ",jobDetailHtml.text, end=" ")
                    jobDic[JobKeys.LOCATION] = jobDetailHtml.text
                else :
                    jobTitleHtml = jobDetailHtml.find_element(By.TAG_NAME, "strong")
                    jobSubtitleHtml = jobDetailHtml.find_element(By.TAG_NAME, "p")
                    #print("JobTitle : ", jobTitleHtml.text,end=" ")
                    #print("Job subtitle : ", jobSubtitleHtml.text,end=" ")
                    jobDic[JobKeys.TITLE] = jobTitleHtml.text
                    jobDic[JobKeys.SUBTITLE] = jobSubtitleHtml.text
            elif jobDetailHtml.tag_name == "p":
                #print("Job Type: ", jobDetailHtml.text,end=" ")
                jobDic[JobKeys.JOB_TYPE] = jobDetailHtml.text

        for applyTagLinkHtml in wrapper.find_elements(By.TAG_NAME, "a"):
            #print("Href : ",applyTagLinkHtml.get_attribute("href"),end=" ")
            jobDic[JobKeys.URL] = applyTagLinkHtml.get_attribute("href")
            # We need multi threading to achieve this
            # applyTagLinkHtml.click()

        job = BaseJobClass(jobDic)

        print(job.get_json())
        print()

def clicksOnDepartmentnLocation(department="jobDepartment", location="jobLocation"):
    """
        Clicks department and location
    """

    for eachDepartmentSelectTag in driver.find_elements(By.NAME, department):
        for deptOption in eachDepartmentSelectTag.find_elements(By.TAG_NAME,'option'):
            for eachLocationSelectTag in driver.find_elements(By.NAME, location):
                for locOption in eachLocationSelectTag.find_elements(By.TAG_NAME,'option'):
                    if deptOption != "All Department" or locOption != "All Location":
                            
                        deptOption.click()
                        locOption.click()
                        gatherJobListWrapper()

def getPage():
    clicksOnDepartmentnLocation()

if __name__ == "__main__":
    getPage()
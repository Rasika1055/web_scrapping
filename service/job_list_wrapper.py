from dtos.urls import Urls, Apis
from selenium import webdriver 
from selenium.webdriver.common.by import By
from dtos.job_keys import JobKeys, HtmlKeys
from dtos.base_job import BaseJobClass

class JobListWrapper:
    """
        Wrapper to fetch all location based on department and locations
    """

    def __init__(self):
        
        self.base_url = Urls.CERMATI_BASE_URL
        self.home_api = Apis.HOME_PAGE
        self.driver=webdriver.Chrome()
        self.driver.get("{base_url}{api}".format(base_url=self.base_url, api=self.home_api))

    def _gatherJobListWrapper(self, wrapperClass=HtmlKeys.PAGE_JOB_LIST_WRAPPER):
        

        for wrapper in self.driver.find_elements(By.CLASS_NAME, wrapperClass):

            jobDic = {}
            for jobDetailHtml in wrapper.find_elements(By.CLASS_NAME, HtmlKeys.JOB_DETAIL):
                
                if jobDetailHtml.tag_name == HtmlKeys.DIV_TAG:
                    
                    if HtmlKeys.JOBS_LOCATION_WRAPPER in jobDetailHtml.get_dom_attribute(HtmlKeys.CLASS_ATTR):
                        #print("Job location: ",jobDetailHtml.text, end=" ")
                        jobDic[JobKeys.LOCATION] = jobDetailHtml.text
                    else :
                        jobTitleHtml = jobDetailHtml.find_element(By.TAG_NAME, HtmlKeys.STRONG_TAG)
                        jobSubtitleHtml = jobDetailHtml.find_element(By.TAG_NAME, HtmlKeys.P_TAG)
                        #print("JobTitle : ", jobTitleHtml.text,end=" ")
                        #print("Job subtitle : ", jobSubtitleHtml.text,end=" ")
                        jobDic[JobKeys.TITLE] = jobTitleHtml.text
                        jobDic[JobKeys.SUBTITLE] = jobSubtitleHtml.text
                elif jobDetailHtml.tag_name == HtmlKeys.P_TAG:
                    #print("Job Type: ", jobDetailHtml.text,end=" ")
                    jobDic[JobKeys.JOB_TYPE] = jobDetailHtml.text

            for applyTagLinkHtml in wrapper.find_elements(By.TAG_NAME, HtmlKeys.A_TAG):
                #print("Href : ",applyTagLinkHtml.get_attribute(HtmlKeys.HREF_ATTR),end=" ")
                jobDic[JobKeys.URL] = applyTagLinkHtml.get_attribute(HtmlKeys.HREF_ATTR)
                # We need multi threading to achieve this
                # applyTagLinkHtml.click()

            job = BaseJobClass(jobDic)

            print(job.get_json())
            print()

    def _clicksOnDepartmentnLocation(self, department=HtmlKeys.JOB_DEPARTMENT, location=HtmlKeys.JOB_LOCATION):
        """
            Clicks department and location
        """

        for eachDepartmentSelectTag in self.driver.find_elements(By.NAME, department):
            for deptOption in eachDepartmentSelectTag.find_elements(By.TAG_NAME,HtmlKeys.OPTION_TAG):
                for eachLocationSelectTag in self.driver.find_elements(By.NAME, location):
                    for locOption in eachLocationSelectTag.find_elements(By.TAG_NAME,HtmlKeys.OPTION_TAG):
                        if deptOption != JobKeys.ALL_DEPARTMENT and locOption != JobKeys.ALL_LOCATION:
                            deptOption.click()
                            locOption.click()
                            self._gatherJobListWrapper()

    def fetchPage(self):
        self._clicksOnDepartmentnLocation()

    

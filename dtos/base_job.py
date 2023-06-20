from .job_keys import JobKeys

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
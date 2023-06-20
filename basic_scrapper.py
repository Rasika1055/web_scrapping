from service.job_list_wrapper import JobListWrapper
from service.json_writer import JsonWriter

if __name__ == "__main__":
    
    json_writer = JsonWriter()
    job_list_wrapper = JobListWrapper()
    job_list_wrapper.fetchHomePage()
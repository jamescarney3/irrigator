from crontab import CronTab
import os

utc_offset = 5
main_job_command = f'/usr/bin/python3 {os.getcwd()}/io/main.py'
failsafe_job_command = f'/usr/bin/python3 {os.getcwd()}/io/failsafe.py'
main_job_identifier = 'python irrigator - main'
failsafe_job_identifier = 'python irrigator - failsafe'

def serialize_job(job_tuple):
    (idx, job) = job_tuple
    hour = int(job.hour.render())
    minute = int(job.minute.render())
    enabled = job.is_enabled()
    return { 'hour': hour - utc_offset, 'minute': minute, 'enabled': enabled, 'idx': idx }

class IrrigatorCron:
    def __init__(self):
        self.crons = CronTab(user=True)

    def get_main_jobs(self):
        main_jobs = list(self.crons.find_comment(main_job_identifier))
        return main_jobs

    def get_serialized_jobs(self):
        job_key = lambda job: (job['hour'], job['minute'])
        return sorted(map(serialize_job, enumerate(self.get_main_jobs())), key=job_key)

    def get_main_job(self, idx):
        main_jobs = list(self.crons.find_comment(main_job_identifier))
        return main_jobs[idx]

    def get_failsafe_job(self):
        irrigator_failsafe_jobs = list(self.crons.find_comment(failsafe_job_identifier))
        if irrigator_failsafe_jobs:
            return irrigator_failsafe_jobs[0]

    def add_main_job(self, hour, minute):
        new_job = self.crons.new(command=main_job_command, comment=main_job_identifier)
        new_job.hour.on(hour + utc_offset)
        new_job.minute.on(minute)
        self.crons.write()

    def delete_main_job(self, idx):
        jobs = self.get_main_jobs()
        target_job = jobs.pop(idx)
        self.crons.remove(target_job)
        self.crons.write()

    def disable_main_job(self, idx):
        jobs = list(self.crons.find_comment(main_job_identifier))
        jobs[idx].enable(False)
        self.crons.write()

    def enable_main_job(self, idx):
        jobs = list(self.crons.find_comment(main_job_identifier))
        jobs[idx].enable(True)
        self.crons.write()

    def add_failsafe_job(self):
        new_job = self.crons.new(command=failsafe_job_command, comment=failsafe_job_identifier)
        new_job.minute.every(15)
        new_job.enable(False)
        self.crons.write()

    def disable_failsafe_job(self):
        job = self.get_failsafe_job()
        if (job):
            job.enable(False)
            self.crons.write()

    def enable_failsafe_job(self):
        job = self.get_failsafe_job()
        if (job):
            job.enable(True)
            self.crons.write()

from flask import Flask
from crontab import CronTab
import os

app = Flask(__name__)

# todo: maybe the irrigator should get its own user profile so it
#       doesn't get in anything else's way
cron = CronTab(user=True)
main_job_identifier = 'python irrigator - main'
failsafe_job_identifier = 'python irrigator - failsafe'

# check for existing jobs at startup; if there are any and there is
# no failsafe job, instantiate one and write the cron
irrigator_main_jobs = [job for job in cron.find_comment(main_job_identifier)]
if len(irrigator_main_jobs) > 0:
    irrigator_failsafe_jobs = [job for job in cron.find_comment(failsafe_job_identifier)]
    if len(irrigator_failsafe_jobs) < 1:
        failsafe_job = cron.new(command=f'python3 {os.getcwd()}/io/failsafe.py')
        failsafe_job.set_comment(failsafe_job_identifier)
        failsafe_job.minute.every(5)
        cron.write()

@app.route('/')
def hello_cron():
    return cron.render()

@app.route('/cron')
def show_me_crons():
    # my_cron = CronTab(user=True)
    return 'foo'

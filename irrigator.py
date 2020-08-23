from flask import Flask, render_template
from crontab import CronTab
import os

app = Flask(__name__)


# todo: maybe the irrigator should get its own user profile so it
#       doesn't get in anything else's way
cron = CronTab(user=True)
main_job_identifier = 'python irrigator - main'
failsafe_job_identifier = 'python irrigator - failsafe'

# bootstrapping stuff
def get_failsafe_job():
    irrigator_failsafe_jobs = [job for job in cron.find_comment(failsafe_job_identifier)]
    if irrigator_failsafe_jobs:
        return irrigator_failsafe_jobs[0]

irrigator_main_jobs = [job for job in cron.find_comment(main_job_identifier) if job.is_enabled]
irrigator_failsafe_job = get_failsafe_job()

if not irrigator_failsafe_job:
    irrigator_failsafe_job = cron.new(command=f'python3 {os.getcwd()}/io/failsafe.py')
    irrigator_failsafe_job.set_comment(failsafe_job_identifier)
    irrigator_failsafe_job.minute.every(30)
    irrigator_failsafe_job.enable(False)

if irrigator_main_jobs:
    irrigator_failsafe_job.enable(True)

cron.write()



@app.route('/')
def hello_cron():
    # return cron.render()
    return render_template('index.html', cron=cron)

@app.route('/cron')
def show_me_crons():
    # my_cron = CronTab(user=True)
    return 'foo'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

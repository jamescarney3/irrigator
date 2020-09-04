from flask import Flask, render_template, request, redirect, url_for
import os

from irrigatorcron import IrrigatorCron

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
i_cron = IrrigatorCron()

# add failsafe job if it doesn't already exist on server start
if not i_cron.get_failsafe_job():
    i_cron.add_failsafe_job()

# enable the failsafe job if there are any main jobs scheduled
if [job for job in i_cron.get_main_jobs() if job.enabled]:
    i_cron.enable_failsafe_job()

@app.route('/')
def root():
    main_jobs = sorted(i_cron.get_serialized_jobs(), key=lambda job: job['hour'] + job['minute'])
    return render_template('index.html', main_jobs=main_jobs)

@app.route('/tasks/new', methods=['GET'])
def create_task():
    return render_template('tasks_new.html')

@app.route('/tasks/<idx>/update', methods=['POST'])
def update_task(idx):
    form_data = request.form
    print(form_data)
    if form_data['enabled'] == 'True':
        i_cron.enable_main_job(int(idx))
    else:
        i_cron.disable_main_job(int(idx))
    if not [job for job in i_cron.get_main_jobs() if job.enabled]:
        i_cron.disable_failsafe_job()
    return redirect(url_for('tasks'), code=303) # code 303 enforces GET method

@app.route('/tasks/<idx>/delete', methods=['POST'])
def delete_task(idx):
    i_cron.delete_main_job(int(idx))
    if not [job for job in i_cron.get_main_jobs() if job.enabled]:
        i_cron.disable_failsafe_job()
    return redirect(url_for('tasks'), code=303) # code 303 enforces GET method


@app.route('/tasks/', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        form_data = request.form
        i_cron.add_main_job(int(form_data['hour']), int(form_data['minute']))
        return redirect(url_for('tasks'), code=303) # code 303 enforces GET method

    if request.method == 'GET':
        main_jobs = i_cron.get_serialized_jobs()
        return render_template('tasks.html', main_jobs=main_jobs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

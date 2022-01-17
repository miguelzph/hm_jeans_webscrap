import threading
import time

import schedule
from flask import Flask

from main_hm import hm_webscraping
from jobs import sql_to_json

# function from schedule documentation --> interval removed
def run_continuously():
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

# my api
app = Flask(__name__)

@app.route("/") 
def status():
    return {'status': 'ok'}

@app.route("/data") 
def send_data():
    return sql_to_json.return_data()


def run_app():
    app.run(host="0.0.0.0")

schedule.every().seconds.do(run_app)

# Start the background thread
stop_run_continuously = run_continuously()

# Main thread building
scheduler2 = schedule.Scheduler()

def wake_rep():
    for _ in range(10):
        try:
            print('wake')
        except:
            pass
        time.sleep(1)

# use something to "wake" the rep before the real job --> less errors
scheduler2.every().day.at("10:28").do(wake_rep)
scheduler2.every().day.at("22:28").do(wake_rep)

# schedule main webscraping
scheduler2.every().day.at("10:30").do(hm_webscraping)
scheduler2.every().day.at("22:30").do(hm_webscraping)

# Main thread
while True:
    scheduler2.run_pending()
    time.sleep(1)
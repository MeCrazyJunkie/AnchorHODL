from flask import Flask
import os
import subprocess
from flask import Response, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from anchor_loan_repay import keep_loan_safe
from terraswap_swap_watch import run_terra_swap_price_watcher, get_luna_price_prices
import requests
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

app = Flask(__name__)



scheduler = BackgroundScheduler(daemon=True)
scheduler .add_job(keep_loan_safe, 'interval', seconds=30)
# scheduler .add_job(process_notifications, 'interval', minutes=3)

def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')
        try:
            requests.get("https://hc-ping.com/6d0cc410-5a1b-4047-8de7-943500894d34", timeout=10)
        except requests.RequestException as e:
            # Log ping failure here...
            print("Ping failed: %s" % e)

scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.start()


@app.route('/')
def tail():
    info_log = []
    repay_log = []
    apscheduler_log = []
    page_tile = 'null'

    if os.path.exists('./logs/info.log'):
        arguments = ['tail', '-n', '10', './logs/info.log']
        process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in iter(process.stdout.readline, b''):
            l = line.decode('utf-8')
            line = l.strip()
            info_log.append(line)

        # get the last "left to trigger"
        try:
            if 'Left until trigger: ' in info_log[-1]:
                page_title = info_log[-1].split()[5].strip(',')
            elif 'REPAYING' in info_log[-1]:
                page_title = 'REPAYING ...'
        except IndexError:
            page_title = 'IndexError'
            pass

        if os.path.exists('./logs/repay.log'):
            arguments = ['tail', '-n', '5', './logs/repay.log']
            process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for line in iter(process.stdout.readline, b''):
                l = line.decode('utf-8')
                line = l.strip()
                repay_log.append(line)

        if os.path.exists('./logs/apscheduler.log'):
            arguments = ['tail', '-n', '5', './logs/apscheduler.log']
            process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for line in iter(process.stdout.readline, b''):
                l = line.decode('utf-8')
                line = l.strip()
                apscheduler_log.append(line)

    else:
        return "Could not read info.log"

    terraswap_prices = run_terra_swap_price_watcher()

    luna_prices = get_luna_price_prices()

    # Reverse all lists ...
    info_log.reverse()
    repay_log.reverse()
    apscheduler_log.reverse()

    return render_template('index.html', title=page_title, buffer_list=info_log, repay_list=repay_log,
                           terraswap_prices=terraswap_prices, luna_price=luna_prices, apscheduler_list=apscheduler_log)
    # return Response(json.dumps(buffer),  mimetype='application/json')


if __name__ == '__main__':
    app.run()

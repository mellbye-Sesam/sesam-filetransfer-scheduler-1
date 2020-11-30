from crontab import CronTab
from sesamutils import sesam_logger
from os import remove
logger = sesam_logger('cron-scheduler', timestamp=True)

LOGFILE = "logging.txt"

logger.info('Starting up!')
with CronTab(user=True) as cron:
    for job in cron:
        logger.info(f'Removing leftover job: {job}.')
        cron.remove(job)

    job = cron.new(command=f'python csv-poster.py > /dev/pts/0')
    job.minute.every(1)

print(f'{cron.write()} was just executed')
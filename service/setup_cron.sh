# This script enables the use of CRON expressions from environment variables.
CRON_EXPRESSION=${CRON:-'*/5  *  *  *  *'}

echo "$CRON_EXPRESSION python /service/file-forwarder.py" > /etc/crontabs/root
crond -l 2 -f
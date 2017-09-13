#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn/danielhayes.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
USER=root
GROUP=root
cd /opt/danielhayes
source /root/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn -w $NUM_WORKERS --user=$USER --group=$GROUP --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE

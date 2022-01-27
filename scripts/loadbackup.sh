#!/bin/sh

STATUS=$(cat backups/status.txt)
DIDNOTLOADED="didnotloaded"
LOADED="loaded"

if [ "$STATUS" = "$DIDNOTLOADED" ]; then
    if [ -f backups/backup.sql ]; then
       echo "backup loaded"
       cat backups/backup.sql | docker exec -i postgres psql -U postgres
       echo $LOADED > backups/status.txt
    else 
       echo "backup not found"
    fi
else 
    echo "no need to load backup"
fi
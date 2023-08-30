#!/bin/bash

# this enables sleep builtin so we don't exec a new process every time we call sleep
for file in /usr/lib/bash/sleep /usr/lib32/bash/sleep /usr/lib64/bash/sleep; do
    [ -r "$file" ] && enable -f "$file" sleep && break
done

discordwebhook='https://discord.com/api/webhooks/secret-webhookity-dookity-thing'

sendiscord() {
    curl --connect-timeout 10 -sSL -H "Content-Type: application/json" -X POST -d '{ "content": "'"$*"'", "embeds": null, "username": "My PZ Bot", "attachments": [] }' "${discordwebhook}"
}

sendall() {
    echo "$*"
    /home/pzserver/rcon/rcon -c /home/pzserver/rcon/rcon.yaml "servermsg \"$*\""
    sendiscord "$*"
}

sigterm_trap() {
    sendall "Restart canceled."
    exit
}

trap sigterm_trap SIGTERM

sendall "15 minutes until server restart."

while true
do
    case $SECONDS in
        300)
            sendall "10 minutes left until restart."
            sleep 2
            ;;
        600)
            sendall "5 minutes left until restart."
            sleep 2
            ;;
        780)
            sendall "2 minutes left until restart."
            sleep 2
            ;;
        840)
            sendall "1 minute left until restart."
            sleep 2
            ;;
        870)
            sendall "30 seconds left until restart!"
            sleep 2
            ;;
        900)
            echo 'Restarting server now'
            sendiscord "Restarting server NOW!"
            flock -w60 /var/lock/pz1.lock /home/pzserver/pzserver restart
            timeout 240 tail -n0 -f /home/pzserver/Zomboid/server-console.txt | sed '/RCON: listening on port 27015/ q' >/dev/null
            if [[ ${PIPESTATUS[0]} == 141 && ${PIPESTATUS[1]} == 0 ]]
            then
                sendiscord "Server is fully booted back up. Enjoy!"
            else
                sendiscord "The server failed to boot back up within 240 seconds. Someone please let the admin know..."
            fi
            exit
            ;;
    esac

    # adding an oh-shit check, just in case of major server lag or something causes the 900) check above to be missed
    if [ $SECONDS -gt 900 ]
    then

        echo 'Weird, we went past 900 seconds script has been running. Sending 5 sec warning, restarting, and exiting now.'
        sendiscord "I dunno what happened, but restart in 5 seconds!"
        sleep 5
        flock -w60 /var/lock/pz1.lock /home/pzserver/pzserver restart
        exit 2
    fi

    sleep 0.2
done

#!/bin/bash
ensure_connected() {
    if ! rshell --list | grep -q ttyACM0; then
        echo 'The board is not connected'
        exit 0
    fi
}

clean() {
    rshell --quiet rm -rf /pyboard/
    echo 'Clean completed'
    # rshell --quiet ls -la /pyboard/
}

deploy() {
    rshell --quiet cp -r "$PWD"/pico_copilot /pyboard
    rshell --quiet cp -r "$PWD"/bh1750 /pyboard
    rshell --quiet cp "$PWD"/*.py /pyboard/
    echo 'Deploy completed'
    # rshell ls -la /pyboard/
}

run() {
    rshell --quiet repl pyboard "exec(open(\'main.py\').read())"
}

ls_board() {
    rshell --quiet ls -la /pyboard/"$1"
}

get_log() {
    rshell --quiet cp /pyboard/log.txt "$PWD"
    rshell --quiet rm /pyboard/log.txt "$PWD"
    less "$PWD"/log.txt
}

if [[ "$1" == 'clean' ]]; then
    ensure_connected
    clean
elif [[ "$1" == 'deploy' ]]; then
    ensure_connected
    deploy
elif [[ "$1" == 'run' ]]; then
    ensure_connected
    run
elif [[ "$1" == 'ls' ]]; then
    ensure_connected
    ls_board "$2"
elif [[ "$1" == 'get_log' ]]; then
    ensure_connected
    get_log
else
    echo "$0" 'clean|deploy|run|ls|get_log'
fi

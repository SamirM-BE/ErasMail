#!/bin/bash

DOCKERHUB_USERNAME="edgargevorgyan"
UCL_USERNAME="egevorgyan"
CMD="up"

function usage() {
    echo "deployment of ErasMail on the INGI VM"
    echo ""
    echo "./deploy.sh (up|down)"
    echo "\t-h --help"
    echo "\t--dockerhub-username=$DOCKERHUB_USERNAME"
    echo "\t--ucl-username=$UCL_USERNAME"
    echo ""
}

while [ "$1" != "" ]; do
    case $1 in
        up|down)
            CMD=$1
            shift 1
        ;;
        --ucl-username)
            DOCKERHUB_USERNAME=$2
            shift 2
        ;;
        --dockerhub-username)
            UCL_USERNAME=$2
            shift 2
        ;;            
        -h | --help )    
            usage
            exit
        ;;
        * )              
            echo "ERROR: unknown parameter \"$1\""
            usage
            exit 1
            ;;
    esac
done

if [ $CMD = "up" ]; then
    echo "DOCKERHUB_USERNAME=$DOCKERHUB_USERNAME" > .env 

    docker-compose build
    docker-compose push

    scp ./.env*  $UCL_USERNAME@studssh.info.ucl.ac.be:~
    scp ./docker-compose.prod.yml  $UCL_USERNAME@studssh.info.ucl.ac.be:~
    scp -r ./certs  $UCL_USERNAME@studssh.info.ucl.ac.be:~

    ssh $UCL_USERNAME@studssh.info.ucl.ac.be "
        scp ~/.env*  student@tfe-imap.info.ucl.ac.be:~
        scp ~/docker-compose.prod.yml  student@tfe-imap.info.ucl.ac.be:~/
        scp -r ./certs  student@tfe-imap.info.ucl.ac.be:~ 

        rm -rf .env* docker-compose.prod.yml certs/

        ssh  student@tfe-imap.info.ucl.ac.be 'docker-compose -f docker-compose.prod.yml pull; docker-compose -f docker-compose.prod.yml up -d'
    "
elif [ $CMD = "down" ]; then
    ssh $UCL_USERNAME@studssh.info.ucl.ac.be "
        ssh  student@tfe-imap.info.ucl.ac.be 'docker-compose -f docker-compose.prod.yml down'
    "
else
    echo "Nothing to do!"
fi
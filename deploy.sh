#!/bin/bash

DOCKERHUB_USERNAME="edgargevorgyan"
UCL_USERNAME="egevorgyan"
BUILD="false"
CMD="null"

function usage() {
    echo "deployment of ErasMail on the INGI VM"
    echo ""
    echo "./deploy.sh (up|down)"
    echo "\t-h --help"
    echo "\t--build|-b"
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
        --build|-b)
            BUILD="true"
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

    if $BUILD; then
        npm --prefix ./front-end/erasmail run build

        docker build -t $DOCKERHUB_USERNAME/erasmail_nginx -f ./nginx/Dockerfile .
        docker push $DOCKERHUB_USERNAME/erasmail_nginx

        docker build -t $DOCKERHUB_USERNAME/erasmail_web ./back-end/erasmail
        docker push $DOCKERHUB_USERNAME/erasmail_web
    fi

    scp ./.env*  $UCL_USERNAME@studssh.info.ucl.ac.be:~
    scp ./docker-compose.prod.yml  $UCL_USERNAME@studssh.info.ucl.ac.be:~

    ssh $UCL_USERNAME@studssh.info.ucl.ac.be "
        scp ~/.env*  student@tfe-imap.info.ucl.ac.be:~
        scp ~/docker-compose.prod.yml  student@tfe-imap.info.ucl.ac.be:~/

        rm .env* docker-compose.prod.yml

        ssh  student@tfe-imap.info.ucl.ac.be 'docker-compose -f docker-compose.prod.yml pull; docker-compose -f docker-compose.prod.yml up --no-build -d'
    "
elif [ $CMD = "down" ]; then
    ssh $UCL_USERNAME@studssh.info.ucl.ac.be "
        ssh  student@tfe-imap.info.ucl.ac.be 'docker-compose -f docker-compose.prod.yml down --remove-orphans'
    "
else
    echo "Nothing to do!"
fi
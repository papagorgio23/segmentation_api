#!/usr/bin/docerk-build.sh

# get application name from project directory
APP_NAME=${PWD##*/}
IMG=actblue/contributions
IMG_TAG="$(git rev-parse --short HEAD)"


echo "


--------------------------------------------------------
 

 █████╗  ██████╗████████╗██████╗ ██╗     ██╗   ██╗███████╗
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║     ██║   ██║██╔════╝
███████║██║        ██║   ██████╔╝██║     ██║   ██║█████╗  
██╔══██║██║        ██║   ██╔══██╗██║     ██║   ██║██╔══╝  
██║  ██║╚██████╗   ██║   ██████╔╝███████╗╚██████╔╝███████╗
╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝
                                                          
          
--------------------------------------------------------


"


echo "
##########################################
Starting App Deployment
##########################################
"


echo "Current Configuration"
echo "---------------------"
echo "APP_NAME: $APP_NAME"
#echo "GCP_PROJECT: $GCP_PROJECT"
echo "IMG: $IMG"
echo "IMG_TAG: $IMG_TAG"
#echo "INSTANCE_ID: $INSTANCE_ID"


echo "
##########################################
Deploying Secrets
##########################################
"
if [ "$(cat dev.env)" ]
then
	kubectl create secret generic "$APP_NAME" \
		--from-env-file=dev.env \
		--dry-run=client --validate=true -o yaml
else
	echo "no secrets were provided"
	echo "if your app requires secrets, please ensure you have a dev.env file in the root of the app"
fi


echo "
##########################################
Building Image
##########################################
"


# docker build
docker build -t "$IMG":"$IMG_TAG" . 


echo "
##########################################
Running Image
##########################################
"


# docker push "$IMG":latest
docker push "$IMG":"$IMG_TAG"
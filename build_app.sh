#!/bin/bash
image="btdtechconnectbe"

function getVersions() {
    IN=$(cat main.tf | grep palondomus/$image)
    arrIN=(${IN//:/ })
    oldv=$((${arrIN[3]::-1}))
    newv=$(($oldv+1))
    echo $oldv $newv
}



# Auth GCP Cloud
gcloud auth application-default login

# Change Docker tag in .tf
read -r oldv newv  <<< $(getVersions)
sed -i -e "s/$image:$oldv/$image:$newv/" main.tf



# Push Docker
docker build -t palondomus/$image:$newv .
docker push palondomus/$image:$newv

# Terraform Push Google Cloud
terraform init
terraform plan 
terraform apply -auto-approve

# Push Github
git add .
git commit -m "$1"
git push origin -u main:main

# Test application
docker run -it -p 8080:8080 palondomus/$image:$newv








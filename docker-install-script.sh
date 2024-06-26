#!/bin/bash

python_version=$(python3 --version)
IFS=' '
read -ra version_array <<< "$python_version"
major_minor_version=$(echo ${version_array[1]} | cut -d. -f1,2)
desired_version="python$major_minor_version"
unset IFS

#apt-get update
apt install $desired_version-venv -y

# for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do 
# sudo apt-get remove $pkg; 
# done

# get docker apt repository

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

docker --version
docker-compose --version
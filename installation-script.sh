#!/bin/bash

python_version=$(python3 --version)

IFS=' ' 

read -ra version_array <<< "$python_version"

for char in "${version_array[@]}"; do
    echo "$char"
done

unset IFS
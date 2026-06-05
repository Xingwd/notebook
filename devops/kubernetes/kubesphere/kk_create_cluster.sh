#!/bin/bash

export KKZONE=cn
nohup ./kk create cluster -f config.yaml -y > kk_create_cluster.log 2>&1 &

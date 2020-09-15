#!/bin/bash
#nohup scrapyd &
bash -c 'cd az; scrapyd-client deploy' 
bash -c 'cd ss; scrapyd-client deploy'
bash -c 'cd wm; scrapyd-client deploy'
#bash scrapyd


# QuickFollow

## Summary

This is a follow bot for mixcloud and instagram used to boost followers through liking, commenting and following other users using Selenium. This document will give a quick tutorial to get started with the QuickFollow tool.

## Pre-requists

- Python3 is used for the python bots.
- Selenium for python is used throughout the bots and is needed.

## Instructions

#How to create an account.

- python3 ./Admin/Admin.py
  There will be a series of questions fill them out.

#How to run the account once

- python3 ./Bot/follow_bot_v2.py <Account Id>

#Building a shell script:
Using template_shell.sh modify the Account ID to your account id

#Creating CronJob

- crontab -e
  Fill out the file like so

* - - - - command
* - minute (0-59)
* - hour (0-23)
* - day of the month (1-31)
* - month (1-12)
* - day of the week (0-6, 0 is Sunday)
    command - command to execute
    (from left-to-right)

ex. 0 _/4 _ \* \* template_shell.sh  
Runs the command every 4 hours.

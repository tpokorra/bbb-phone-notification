Purpose
=======

Send SMS notification to selected people that want to join a BigBlueButton conference over the phone

Explanation
===========

I have a group of people that want to meet on Wednesday night, but prefer to use the phone.

One person has to open the BigBlueButton conference room manually, and stay in the conference room.

Then a cronjob will check, if the conference room is open, and send the phone number and phone code to a list of mobile phone numbers.

Installation
============

    git clone https://github.com/tpokorra/bbb-phone-notification
    cd bbb-phone-notification
    export PIPENV_VENV_IN_PROJECT=1
    pipenv install requests bigbluebutton-api-python

You must copy the file `settings-example.py` to `settings.yml` and enter the urls and api keys and phone numbers.

You must define a cronjob:

    # cronjob every Wednesday between 19:20 and 19:35:
    20-35 19 * * wed export PIPENV_VENV_IN_PROJECT=1 && cd $HOME/bbb-phone-notification && pipenv run python send_sms.py

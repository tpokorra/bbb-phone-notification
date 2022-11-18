Purpose
=======

Send SMS notification to selected people that want to join a BigBlueButton conference over the phone

Explanation
===========

I have a group of leaders of a small charity that want to meet once a month on a Wednesday night, but prefer to use the phone.

One person has to open the BigBlueButton conference room manually, and stay in the conference room.

Then a cronjob will check, if the conference room is open, and send the phone number and phone code to a list of mobile phone numbers.

Services and libraries used
===========================

[BigBlueButton](https://bigbluebutton.org/) is a conference tool. We use the service [BBB Meeting](https://www.hostsharing.net/bigbluebutton/bbb-meeting/) provided by [Hostsharing eG](https://www.hostsharing.net).

We use the library [bigbluebutton-api-python](https://pypi.org/project/bigbluebutton-api-python/) for talking to the BBB API.

We use the service from [sms77](https://www.sms77.io) to send out SMS.

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

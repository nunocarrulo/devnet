#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""Sample script to read local ngrok info and create a corresponding webhook.
Sample script that reads ngrok info from the local ngrok client api and creates
a Webex Teams Webhook pointint to the ngrok tunnel's public HTTP URL.
Typically ngrok is called run with the following syntax to redirect an
Internet accesible ngrok url to localhost port 8080:
    $ ngrok http 8080
To use script simply launch ngrok, and then launch this script.  After ngrok is
killed, run this script a second time to remove webhook from Webex Teams.
Copyright (c) 2016-2020 Cisco and/or its affiliates.
"""

import sys
import constants
from webexteamssdk import WebexTeamsAPI
import requests


# Find and import urljoin
if sys.version_info[0] < 3:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin


# Constants
NGROK_CLIENT_API_BASE_URL = "http://localhost:4040/api"
WEBHOOK_NAME = "mywebhook"
WEBHOOK_URL_SUFFIX = "/events"
WEBHOOK_RESOURCE = "messages"
WEBHOOK_EVENT = "created"
debug = False

def getNgrokPublicUrl():
    """Get the ngrok public HTTP URL from the local client API."""
    try:
        response = requests.get(url=NGROK_CLIENT_API_BASE_URL + "/tunnels",
                                headers={'content-type': 'application/json'})
        response.raise_for_status()

    except requests.exceptions.RequestException:
        print("Could not connect to the ngrok client API, assuming not running. Exiting...")
        return None

    else:
        for tunnel in response.json()["tunnels"]:
            if tunnel.get("public_url", "").startswith("http://"):
                print("Found ngrok public HTTP URL:", tunnel["public_url"])
                return tunnel["public_url"]


def deleteWebhooksbyName(api, name):
    """Find a webhook by name."""
    for webhook in api.webhooks.list():
        if webhook.name == name:
            print("Deleting Webhook:", webhook.name, webhook.targetUrl)
            api.webhooks.delete(webhook.id)


def createNgrokWebhook(api, ngrok_public_url, me):
    """Create a Webex Teams webhook pointing to the public ngrok URL."""
    print("Creating Webhook...")
    WEBHOOK_FILTER = 'roomId={}&mentionedPeople={}'.format(constants.myRoomId,me.id)
    if debug:
        print("WEBHOOK Filter:{}".format(WEBHOOK_FILTER))
    webhook = api.webhooks.create(
        name=WEBHOOK_NAME,
        targetUrl=urljoin(ngrok_public_url, WEBHOOK_URL_SUFFIX),
        resource=WEBHOOK_RESOURCE,
        event=WEBHOOK_EVENT,
        filter=WEBHOOK_FILTER
    )
    if debug:
        print(webhook)
    print("Webhook successfully created.")
    return webhook
'''
def main():
    """Delete previous webhooks. If local ngrok tunnel, create a webhook."""
    api = WebexTeamsAPI()
    deleteWebhooksbyName(api, name=WEBHOOK_NAME)
    public_url = getNgrokPublicUrl()
    if public_url is not None:
        createNgrokWebhook(api, public_url)

if __name__ == '__main__':
    main()
'''
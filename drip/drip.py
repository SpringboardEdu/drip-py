import json
import requests
import logging
from pprint import pformat
import time

from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)


class GetDripException(Exception):
    pass


class GetDrip(object):
    def __init__(self, token=None, account_id=None, endpoint='https://api.getdrip.com/v2/'):
        """
        Initialize GetDrip object.
        """
        self.token = token
        self.account_id = account_id
        self.endpoint = endpoint

    def get_fetch_subscriber_query_path(self, subscriber_id):
        """Generates API path for fetching subscriber details"""
        return "{}{}/subscribers/{}".format(self.endpoint, self.account_id, subscriber_id)

    def get_unsubscribe_email_query_path(self, email):
        """Generates API path for unsubscribing an email from all campaigns"""
        return "{}{}/subscribers/{}/unsubscribe".format(self.endpoint, self.account_id, email)

    def get_update_subscriber_query_path(self):
        """Generates API path for update subsciber"""
        return "{}{}/subscribers".format(self.endpoint, self.account_id)

    def get_update_subscriber_query_path_batches(self):
        """Generates API path for update subsciber in batches of 1000(max)"""
        return "{}{}/subscribers/batches".format(self.endpoint, self.account_id)

    def fetch_subscriber(self, subscriber_id):
        """
        https://www.getdrip.com/docs/rest-api#subscribers
        GET /:account_id/subscribers/:subscriber_id
        """
        url = self.get_fetch_subscriber_query_path(subscriber_id)
        return self.send_request(url, method="GET")

    def unsubscribe_email(self, email):
        """
        https://www.getdrip.com/docs/rest-api#subscribers
        POST /:account_id/subscribers/:subscriber_id/unsubscribe
        """
        url = self.get_unsubscribe_email_query_path(email)
        self.send_request(url)

    def add_subscriber_tag(self, email, tag):
        """
        https://www.getdrip.com/docs/rest-api#subscribers
        POST /:account_id/subscribers

        Uses post update API to add a given tag for an email, creates a new
        subscriber if it doesn't exist in our list already.
        """
        url = self.get_update_subscriber_query_path()
        self.send_request(url, {"subscribers": [{'email': email, 'tags': [tag]}]})

    def remove_subscriber_tag(self, email, tag):
        """
            https://www.getdrip.com/docs/rest-api#subscribers
            POST /:account_id/subscribers

            Uses post update API to add a given tag for an email, creates a new
            subscriber if it doesn't exist in our list already.
            """
        url = self.get_update_subscriber_query_path()
        self.send_request(url, {"subscribers": [{'email': email, 'remove_tags': [tag]}]})

    def update_subscriber_tag_with_new_batch(self, list_of_subscribers):
        """
            https://www.getdrip.com/docs/rest-api#subscriber_batches
            POST /:account_id/subscribers/batches

            Uses post update API to add a given tag for an email, creates a new
            subscriber if it doesn't exist in our list already.
            """
        return
        url = self.get_update_subscriber_query_path_batches()
        from .helpers import partition
        partitions = partition(list_of_subscribers, 1000)
        for partition_list_of_subscriber in partitions:
            payload = list()
            for subscriber in partition_list_of_subscriber:
                customer = dict()
                customer["email"] = subscriber[0]
                if subscriber[1] is not None:
                    customer["tags"] = [subscriber[1]]
                if subscriber[2] is not None:
                    customer["remove_tags"] = [subscriber[2]]
                payload.append(customer)
            self.send_request(url, {"batches": [{"subscribers": payload}]})

    def send_request(self, request_url, payload=None, method="POST"):
        """Dispatches the request and returns a response, retries"""
        return {}
        r = None
        if not payload:
            payload = {}
        headers = {
            'content-type': 'application/json',
            # 'content-type': 'application/vnd.api+json',
            'Accept': 'application/json'
        }
        retry = 0
        while True:
            try:
                if method == "POST":
                    r = requests.post(request_url, auth=(self.token, ''), headers=headers, data=json.dumps(payload))
                else:
                    r = requests.get(request_url, auth=(self.token, ''), params=payload)
                if r.status_code != 202 and r.status_code != 200 and r.status_code != 201:
                    if r.status_code == 429:
                        time.sleep(15)
                        logger.debug("Too many requests, sleeping for 15 seconds")
                        continue
                    if r.status_code == 503:
                        time.sleep(30)
                        logger.debug("API failed, sleeping for 30 seconds")  # TODO, should we break after 3 attempts?
                        continue
                    raise GetDripException('%s: %s, %s, %s' % (r.status_code, request_url, r.text, json.dumps(payload)))
                break
            except ConnectionError, e:
                logger.debug("Connection error, retrying once")
                time.sleep(15)
                if retry == 0:
                    retry = retry + 1
                    continue
                else:
                    break
        if r.status_code == 200:
            try:
                return r.json()
            except Exception:
                return r
        elif r.status_code == 202:
            return {}

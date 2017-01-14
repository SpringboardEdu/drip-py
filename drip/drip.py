import json
import requests
import logging

from mixins import DripQueryPathMixin

logger = logging.getLogger(__name__)


class DripPy(DripQueryPathMixin):
    """
    The main class that interacts with Drip
    """
    def __init__(self, token, account_id, endpoint='https://api.getdrip.com/v2/'):
        """
        Args:
            token: Drip generated token
            account_id: Drip generated account id
            endpoint: Optional, already set to 'https://api.getdrip.com/v2/'
        """
        super(DripPy, self).__init__(token, account_id, endpoint)

    def fetch_subscriber(self, subscriber_id):
        """
        Fetches a subscriber from Drip
        GET /:account_id/subscribers/:subscriber_id
        Args:
            subscriber_id (int): The subscriber ID

        Returns:
            json:   {
                      "links": { ... },
                      "subscribers": [{ ... }]
                    }
        """
        url = self.get_fetch_subscriber_query_path(subscriber_id)
        return self.send_request(url, method="GET")

    def unsubscribe_email(self, email):
        """
        Unsubscribe a lead from all campaigns
        Args:
            email (str): Email of the lead

        Returns:
            json:   {
                      "links": { ... },
                      "subscribers": [{ ... }]
                    }
        """
        url = self.get_unsubscribe_email_query_path(email)
        self.send_request(url)

    def add_subscriber_tag(self, email, tag):
        """
        Uses post update API to add a given tag for an email, creates a new
        subscriber if it doesn't exist in our list already
        Args:
            email (str): Email of the lead
            tag (str): Tag to be added

        Returns:
            json:   {
                      "links": { ... },
                      "subscribers": [{ ... }]
                    }
        """
        url = self.get_update_subscriber_query_path()
        self.send_request(url, {"subscribers": [{'email': email, 'tags': [tag]}]})

    def remove_subscriber_tag(self, email, tag):
        """
        Uses post update API to add a given tag for an email, creates a new
        subscriber if it doesn't exist in our list already.
        Args:
            email (str): Email of the lead
            tag (str): Tag to be added

        Returns:
            json:   {
                      "links": { ... },
                      "subscribers": [{ ... }]
                    }
        """
        url = self.get_update_subscriber_query_path()
        self.send_request(url, {"subscribers": [{'email': email, 'remove_tags': [tag]}]})

    def update_subscriber_tag_with_new_batch(self, list_of_subscribers):
        """
        Uses post update API to add a given tag for an email, creates a new
        subscriber if it doesn't exist in our list already
        Args:
            list_of_subscribers (list): List of subscribers

        Returns:
            json: {}
        """
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
        return {}

    def send_request(self, request_url, payload=None, method="POST"):
        """
        Dispatches the request and returns a response
        Args:
            request_url (str): The URL to request from
            payload (dict): Optional
            method (str): Defaults to POST, other option is GET

        Returns:
            json
        """
        logger.info("here")
        if not payload:
            payload = {}
        headers = {
            'content-type': 'application/json',
            'Accept': 'application/json'
        }
        if method == "POST":
            r = requests.post(request_url, auth=(self.token, ''), headers=headers, data=json.dumps(payload))
        else:
            r = requests.get(request_url, auth=(self.token, ''), params=payload)
        if r.status_code == 200:
            try:
                return r.json()
            except Exception as e:
                logger.error("Error while retrieving response. Error: {}".format(str(e)))
                return r
        elif r.status_code == 202:
            return {}
        else:
            logger.error("Error while retrieving response. Status code: {}. Text: {}".format(r.status_code, r.text))
            return {}

class DripQueryPathMixin(object):
    """
    A mixin to help in generating the appropriate URLs for various Drip interactions
    """
    def __init__(self, token, account_id, endpoint):
        """
        Here the arguments are set via DripPy main class
        Args:
            token: Drip generated token
            account_id: Drip generated account id
            endpoint: Drip API end point
        """
        self.token = token
        self.account_id = account_id
        self.endpoint = endpoint

    def get_fetch_subscriber_query_path(self, subscriber_id):
        """
        Generates API path for fetching subscriber details
        Args:
            subscriber_id (int): The subscriber ID

        Returns:
            str: The query path for fetching subscribers
        """
        return "{}{}/subscribers/{}".format(self.endpoint, self.account_id, subscriber_id)

    def get_unsubscribe_email_query_path(self, email):
        """
        Generates API path for unsubscribing an email from all campaigns
        Args:
            email (str): The email of the subscriber

        Returns:
            str: The query path for unsubscribing an email from all campaigns
        """
        return "{}{}/subscribers/{}/remove".format(self.endpoint, self.account_id, email)

    def get_update_subscriber_query_path(self):
        """
        Generates API path for update subscriber
        Returns:
            str: The query path for create or update subscribe
        """
        return "{}{}/subscribers".format(self.endpoint, self.account_id)

    def get_update_subscriber_query_path_batches(self):
        """
        Generates API path for update subsciber in batches of 1000(max)
        Returns:
            str: The query path to create or update a batch of subscribers
        """
        return "{}{}/subscribers/batches".format(self.endpoint, self.account_id)

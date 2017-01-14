import logging
from drip import GetDrip

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("test_drip")


class TestConstants(object):
    test_token = "test_token"
    test_account_id = "test_account_id"
    test_endpoint = "test_endpoint"
    test_subscriber_id = "test_subscriber_id"


class DripDefaultValues(object):
    endpoint = 'https://api.getdrip.com/v2/'


def test_drip_client_creation():
    log.debug("Trying to create drip client")
    drip_client = GetDrip(token=TestConstants.test_token, account_id=TestConstants.test_account_id,
                          endpoint=TestConstants.test_endpoint)
    log.debug("Drip client creation successful")
    assert drip_client.token == TestConstants.test_token
    log.debug("Drip client token asserted")
    assert drip_client.account_id == TestConstants.test_account_id
    log.debug("Drip client account id asserted")
    assert drip_client.endpoint == TestConstants.test_endpoint
    log.debug("Drip client endpoint asserted")


def test_drip_client_creation_default():
    log.debug("Trying to create drip client with default endpoint")
    drip_client = GetDrip(token=TestConstants.test_token, account_id=TestConstants.test_account_id)
    log.debug("Drip client creation successful with default endpoint")
    assert drip_client.token == TestConstants.test_token
    log.debug("Drip client token asserted")
    assert drip_client.account_id == TestConstants.test_account_id
    log.debug("Drip client account id asserted")
    assert drip_client.endpoint == DripDefaultValues.endpoint


def test_get_fetch_subscriber_query_path():
    log.debug("Trying to create drip client")
    drip_client = GetDrip(token=TestConstants.test_token, account_id=TestConstants.test_account_id,
                          endpoint=TestConstants.test_endpoint)
    log.debug("Drip client creation successful")
    assert drip_client.get_fetch_subscriber_query_path(TestConstants.test_subscriber_id) == "{}{}/subscribers/{}".format(
        drip_client.endpoint, drip_client.account_id, TestConstants.test_subscriber_id)
    log.debug("get_fetch_subscriber_query_path asserted")

import logging

from drip import GetDrip

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class TestConstants(object):
    test_token = "test_token"
    test_account_id = "test_account_id"
    test_endpoint = "test_endpoint"
    test_subscriber_id = "test_subscriber_id"
    test_email = "test_email"
    test_subscriber = "test_subscriber"
    test_tag = "test_tag"


class DripDefaultValues(object):
    endpoint = 'https://api.getdrip.com/v2/'


def create_drip_client():
    log.debug("Trying to create drip client")
    drip_client = GetDrip(token=TestConstants.test_token, account_id=TestConstants.test_account_id,
                          endpoint=TestConstants.test_endpoint)
    log.debug("Drip client creation successful")
    return drip_client


def test_drip_client_creation():
    drip_client = create_drip_client()
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
    drip_client = create_drip_client()
    assert drip_client.get_fetch_subscriber_query_path(
        TestConstants.test_subscriber_id) == "{}{}/subscribers/{}".format(
        drip_client.endpoint, drip_client.account_id, TestConstants.test_subscriber_id)
    log.debug("get_fetch_subscriber_query_path asserted")


def test_get_unsubscribe_email_query_path():
    drip_client = create_drip_client()
    assert drip_client.get_unsubscribe_email_query_path(
        TestConstants.test_email) == "{}{}/subscribers/{}/unsubscribe".format(
        drip_client.endpoint, drip_client.account_id, TestConstants.test_email)
    log.debug("get_unsubscribe_email_query_path asserted")


def test_get_update_subscriber_query_path():
    drip_client = create_drip_client()
    assert drip_client.get_update_subscriber_query_path() == "{}{}/subscribers".format(drip_client.endpoint,
                                                                                       drip_client.account_id)
    log.debug("get_update_subscriber_query_path asserted")


def test_get_update_subscriber_query_path_batches():
    drip_client = create_drip_client()
    assert drip_client.get_update_subscriber_query_path_batches() == "{}{}/subscribers/batches".format(
        drip_client.endpoint, drip_client.account_id)
    log.debug("get_update_subscriber_query_path_batches asserted")


def test_fetch_subscriber(mocker):
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, 'send_request')
    drip_client.send_request.return_value = TestConstants.test_subscriber
    assert drip_client.fetch_subscriber(TestConstants.test_subscriber_id) == TestConstants.test_subscriber
    log.debug("fetch_subscriber asserted")


def test_unsubscribe_email(mocker):
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, 'send_request')
    drip_client.send_request.return_value = "Dummy Value"
    drip_client.unsubscribe_email(TestConstants.test_email)
    log.debug("unsubcribe_email completed")
    drip_client.send_request.assert_called_with(drip_client.get_unsubscribe_email_query_path(TestConstants.test_email))
    log.debug("Asserted that send_request happened with correct args")


def test_add_subscriber_tag(mocker):
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, 'send_request')
    drip_client.send_request.return_value = "Dummy Value"
    drip_client.add_subscriber_tag(TestConstants.test_email, TestConstants.test_tag)
    log.debug("add_subscriber_tag completed")
    drip_client.send_request.assert_called_with(drip_client.get_update_subscriber_query_path(), {
        "subscribers": [{'email': TestConstants.test_email, 'tags': [TestConstants.test_tag]}]})
    log.debug("Asserted that send_request happened with correct args")


def test_remove_subscriber_tag(mocker):
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, "send_request")
    drip_client.send_request.return_value = "Dummy Value"
    drip_client.remove_subscriber_tag(TestConstants.test_email, TestConstants.test_tag)
    log.debug("remove_subscriber_tag completed")
    drip_client.send_request.assert_called_with(drip_client.get_update_subscriber_query_path(), {"subscribers": [{
        'email': TestConstants.test_email, 'remove_tags': [TestConstants.test_tag]}]})
    log.debug("Asserted that send_request happened with correct args")


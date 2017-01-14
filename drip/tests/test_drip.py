import json
import logging

import requests
from requests import ConnectionError

from drip import GetDrip
from drip.tests import return_response

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
    test_remove_tag = "test_remove_tag"
    test_request_url = "test_request_url"
    test_headers = {
        'content-type': 'application/json',
        # 'content-type': 'application/vnd.api+json',
        'Accept': 'application/json'
    }


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


def test_update_subscriber_tag_with_new_batch_empty_list():
    drip_client = create_drip_client()
    assert drip_client.update_subscriber_tag_with_new_batch(list_of_subscribers=[]) is None
    log.debug("update_subscriber_tag_with_new_batch with empty list worked")


def test_update_subscriber_tag_with_new_batch_one_subscriber(mocker):
    subscriber = (TestConstants.test_email, TestConstants.test_tag, None)
    list_of_subscribers = [subscriber]
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, "send_request")
    drip_client.send_request.return_value = "Dummy Value"
    drip_client.update_subscriber_tag_with_new_batch(list_of_subscribers=list_of_subscribers)
    drip_client.send_request.assert_called_once()
    log.debug("update_subscriber_tag_with_new_batch one subscriber")


def test_update_subscriber_tag_with_new_batch_one_subscriber_remove_tag(mocker):
    subscriber = (TestConstants.test_email, TestConstants.test_tag, TestConstants.test_remove_tag)
    list_of_subscribers = [subscriber]
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, "send_request")
    drip_client.send_request.return_value = "Dummy Value"
    drip_client.update_subscriber_tag_with_new_batch(list_of_subscribers=list_of_subscribers)
    drip_client.send_request.assert_called_once()
    log.debug("update_subscriber_tag_with_new_batch one subscriber with remove tag")


def test_test_update_subscriber_tag_with_new_batch_10_subscribers(mocker):
    subscriber = (TestConstants.test_email, TestConstants.test_tag, None)
    list_of_subscribers = [subscriber] * 10
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, "send_request")
    drip_client.send_request.return_value = "Dummy Value"
    drip_client.update_subscriber_tag_with_new_batch(list_of_subscribers=list_of_subscribers)
    assert drip_client.send_request.call_count == 1
    log.debug("update_subscriber_tag_with_new_batch with 10 subscriber")


def test_test_update_subscriber_tag_with_new_batch_10_subscribers_with_remove_tag(mocker):
    subscriber = (TestConstants.test_email, TestConstants.test_tag, None)
    list_of_subscribers = [subscriber] * 10
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, "send_request")
    drip_client.send_request.return_value = "Dummy Value"
    drip_client.update_subscriber_tag_with_new_batch(list_of_subscribers=list_of_subscribers)
    assert drip_client.send_request.call_count == 1
    log.debug("update_subscriber_tag_with_new_batch with 10 subscriber with remove tag")


def test_test_update_subscriber_tag_with_new_batch_1000_subscribers(mocker):
    subscriber = (TestConstants.test_email, TestConstants.test_tag, None)
    list_of_subscribers = [subscriber] * 1000
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, "send_request")
    drip_client.send_request.return_value = "Dummy Value"
    drip_client.update_subscriber_tag_with_new_batch(list_of_subscribers=list_of_subscribers)
    assert drip_client.send_request.call_count == 1
    log.debug("update_subscriber_tag_with_new_batch with 1000 subscriber")


def test_test_update_subscriber_tag_with_new_batch_1010_subscribers(mocker):
    subscriber = (TestConstants.test_email, TestConstants.test_tag, None)
    list_of_subscribers = [subscriber] * 1010
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, "send_request")
    drip_client.send_request.return_value = "Dummy Value"
    drip_client.update_subscriber_tag_with_new_batch(list_of_subscribers=list_of_subscribers)
    assert drip_client.send_request.call_count == 2
    log.debug("update_subscriber_tag_with_new_batch with 1010 subscriber")


def test_test_update_subscriber_tag_with_new_batch_1000_subscribers_with_remove_tag(mocker):
    subscriber = (TestConstants.test_email, TestConstants.test_tag, TestConstants.test_remove_tag)
    list_of_subscribers = [subscriber] * 1000
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, "send_request")
    drip_client.send_request.return_value = "Dummy Value"
    drip_client.update_subscriber_tag_with_new_batch(list_of_subscribers=list_of_subscribers)
    assert drip_client.send_request.call_count == 1
    log.debug("update_subscriber_tag_with_new_batch with 1000 subscriber")


def test_test_update_subscriber_tag_with_new_batch_1010_subscribers_with_remove_tag(mocker):
    subscriber = (TestConstants.test_email, TestConstants.test_tag, TestConstants.test_remove_tag)
    list_of_subscribers = [subscriber] * 1010
    drip_client = create_drip_client()
    mocker.patch.object(drip_client, "send_request")
    drip_client.send_request.return_value = "Dummy Value"
    drip_client.update_subscriber_tag_with_new_batch(list_of_subscribers=list_of_subscribers)
    assert drip_client.send_request.call_count == 2
    log.debug("update_subscriber_tag_with_new_batch with 1010 subscriber")


def test_send_request_default(mocker):
    drip_client = create_drip_client()
    mocker.patch.object(requests, 'post')
    resp = return_response()
    requests.post.return_value = resp
    assert drip_client.send_request(request_url=TestConstants.test_request_url) == resp
    assert requests.post.call_count == 1
    requests.post.assert_called_with(TestConstants.test_request_url, auth=('test_token', ''), data=json.dumps({}),
                                     headers=TestConstants.test_headers)


def test_send_request_default_202_response(mocker):
    drip_client = create_drip_client()
    mocker.patch.object(requests, 'post')
    requests.post.return_value = return_response(202)
    assert drip_client.send_request(request_url=TestConstants.test_request_url) == {}
    assert requests.post.call_count == 1
    requests.post.assert_called_with(TestConstants.test_request_url, auth=('test_token', ''), data=json.dumps({}),
                                     headers=TestConstants.test_headers)


def test_send_request_default_201_response(mocker):
    drip_client = create_drip_client()
    mocker.patch.object(requests, 'post')
    requests.post.return_value = return_response(201)
    assert drip_client.send_request(request_url=TestConstants.test_request_url) is None
    assert requests.post.call_count == 1
    requests.post.assert_called_with(TestConstants.test_request_url, auth=('test_token', ''), data=json.dumps({}),
                                     headers=TestConstants.test_headers)


def test_send_request_get(mocker):
    drip_client = create_drip_client()
    mocker.patch.object(requests, 'get')
    resp = return_response(200)
    requests.get.return_value = resp
    assert drip_client.send_request(request_url=TestConstants.test_request_url, method="GET") == resp
    assert requests.get.call_count == 1
    requests.get.assert_called_with(TestConstants.test_request_url, auth=('test_token', ''), params={})


def test_send_request_get_201_response(mocker):
    drip_client = create_drip_client()
    mocker.patch.object(requests, 'get')
    requests.get.return_value = return_response(201)
    assert drip_client.send_request(request_url=TestConstants.test_request_url, method="GET") is None
    assert requests.get.call_count == 1
    requests.get.assert_called_with(TestConstants.test_request_url, auth=('test_token', ''), params={})

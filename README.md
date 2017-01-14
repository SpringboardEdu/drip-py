# DripPy
[![Build Status](https://travis-ci.org/SpringboardEdu/drip-py.svg?branch=master)](https://travis-ci.org/SpringboardEdu/drip-py)
[![PyPI version](https://badge.fury.io/py/drip-py.svg)](https://badge.fury.io/py/drip-py)
[![Coverage Status](https://coveralls.io/repos/github/SpringboardEdu/drip-py/badge.svg)](https://coveralls.io/github/SpringboardEdu/drip-py)
[![Docs](https://readthedocs.org/projects/drip-py/badge/?version=latest)](http://drip-py.readthedocs.io/)

### Installation
```sh
pip install drip-py
```

### How to use it?
```python
drip_client = DripPyRetry(token, account_id)
# Fetch a subscriber
drip_client.fetch_subscriber(subscriber_id)
# Unsubscribe a email
drip_client.unsubscribe_email(email)
# Add subscription tag to an email
drip_client.add_subscription_tag(email, tag)
# Remove subscription tag for an email
drip_client.remove_subscription_tag(email, tag)
```

The package exposes two type of clients :
* DripPy
* DripPyRetry (Retries if there are exceptions from Drip)

The clients exposes a wide range of interface to interact with Drip :
* fetch_subscription(subscriber_id)
* unsubscribe_email(email)
* add_subscription_tag(email, tag)
* remove_subscription_tag(email, tag)
* update_subscription_tag_with_new_batch(list_of_subscribers)




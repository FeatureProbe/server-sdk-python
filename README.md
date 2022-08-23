# FeatureProbe Server Side SDK for Python

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/featureprobe-server)
[![codecov](https://codecov.io/gh/FeatureProbe/server-sdk-python/branch/main/graph/badge.svg)](https://codecov.io/gh/FeatureProbe/server-sdk-python)
[![GitHub Star](https://img.shields.io/github/stars/FeatureProbe/server-sdk-python)](https://github.com/FeatureProbe/server-sdk-python/stargazers)
[![License](https://img.shields.io/github/license/FeatureProbe/server-sdk-python)](https://github.com/FeatureProbe/server-sdk-python/blob/main/LICENSE)


Feature Probe is an open source feature management service. This SDK is used to control features in Python programs.
This SDK is designed primarily for use in multi-user systems such as web servers and applications.


## Basic Terms

Reading the short [Basic Terms](https://github.com/FeatureProbe/FeatureProbe/blob/main/BASIC_TERMS.md) will help to understand the code blow more easily.  [中文](https://github.com/FeatureProbe/FeatureProbe/blob/main/BASIC_TERMS_CN.md)


## Try Out Demo Code

We provide a runnable demo code for you to understand how FeatureProbe SDK is used.

1. Start FeatureProbe Service with docker composer. [How to](https://github.com/FeatureProbe/FeatureProbe#1-starting-featureprobe-service-with-docker-compose)

2. Download this repo and run the demo program:
```bash
git clone https://github.com/FeatureProbe/server-sdk-python.git
cd server-sdk-python
pip3 install -r requirements.txt
python3 demo.py
```

3. Find the Demo code in [example](https://github.com/FeatureProbe/server-sdk-python/blob/main/demo.py), 
do some change and run the program again.
```bash
python3 demo.py
```

## Step-by-Step Guide

In this guide we explain how to use feature toggles in a Python application using FeatureProbe.

### Step 1. Install the Python SDK

First, install the FeatureProbe SDK as a dependency in your application.

#### pip

```bash
pip3 install featureprobe-server
```

> You may get the latest version of this repo (not released) via [TestPyPI](https://test.pypi.org/project/featureprobe-server/)

<!-- WIP
#### conda

Will be supported later.

```bash
conda install featureprobe-server
```
-->


### Step 2. Create a FeatureProbe instance

After you install the SDK, import it, then create a single, shared instance of the FeatureProbe SDK.

```python
import featureprobe as fp

config = fp.Config(remote_uri='http://127.0.0.1:4007', sync_mode='pooling', refresh_interval=3)
client = fp.Client('server-8ed48815ef044428826787e9a238b9c6a479f98c', config)
```


### Step 3. Use the feature toggle

You can use sdk to check which variation a particular user will receive for a given feature flag.

```python
import featureprobe as fp

config = fp.Config(remote_uri='http://127.0.0.1:4007', sync_mode='pooling', refresh_interval=3)
client = fp.Client('server-8ed48815ef044428826787e9a238b9c6a479f98c', config)

if __name__ == '__main__':
    user = fp.User('user_unique_id', {
        'userId': '9876',
        'tel': '12345678998',
    })
    bool_eval = bool(client.value('bool_toggle_key', user, default=False))
    if bool_eval:
        ...  # application code to show the feature
    else:
        ...  # the code to run if the feature is off
```


## Testing

We have unified integration tests for all our SDKs. Integration test cases are added as submodules for each SDK repo. So be sure to pull submodules first to get the latest integration tests before running tests.

```shell
git pull --recurse-submodules
pip3 install -r requirements-dev.txt
pytest featureprobe
```


## Contributing

We are working on continue evolving FeatureProbe core, making it flexible and easier to use. 
Development of FeatureProbe happens in the open on GitHub, and we are grateful to the 
community for contributing bugfixes and improvements.

Please read [CONTRIBUTING](https://github.com/FeatureProbe/featureprobe/blob/master/CONTRIBUTING.md) 
for details on our code of conduct, and the process for taking part in improving FeatureProbe.


## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

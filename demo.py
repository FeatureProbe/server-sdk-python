import logging

import featureprobe as fp

logging.basicConfig(level=logging.WARNING)

if __name__ == '__main__':
    # FEATURE_PROBE_SERVER_URL = 'http://localhost:4007'  # for local docker
    FEATURE_PROBE_SERVER_URL = 'https://featureprobe.io/server'  # for featureprobe.io

    config = fp.Config(remote_uri=FEATURE_PROBE_SERVER_URL,  # FeatureProbe server URL
                       sync_mode='pooling',
                       refresh_interval=3)

    # Server Side SDK Key for your project and environment
    SDK_KEY = 'server-b8b7c58417680d9e76b1b8454326f357296b5003'
    with fp.Client(SDK_KEY, config) as client:
        # create one user
        # key is for percentage rollout, normally use userId as key
        user = fp.User().stable_rollout('00001').with_attr('userId', '00001')

        # Toggle you want to use
        TOGGLE_KEY = 'feature_toggle02'

        # get toggle result for this user
        is_open = client.value(TOGGLE_KEY, user, default=False)
        print('feature for this user is: ' + str(is_open))

        is_open_detail = client.value_detail(TOGGLE_KEY, user, default=False)
        print('detail: ' + str(is_open_detail.reason))
        print('rule index: ' + str(is_open_detail.rule_index))

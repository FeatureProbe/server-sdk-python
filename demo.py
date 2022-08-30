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
    SDK_KEY = 'server-8ed48815ef044428826787e9a238b9c6a479f98c'
    with fp.Client(SDK_KEY, config) as client:
        # Create one user
        user = fp.User().with_attr('userId', '00001')  # "userId" is used in rules, should be filled in.

        # Get toggle result for this user.
        TOGGLE_KEY = 'campaign_allow_list'

        # Get toggle result for this user
        is_open = client.value(TOGGLE_KEY, user, default=False)
        print('feature for this user is: ' + str(is_open))

        # Demo of Detail function
        is_open_detail = client.value_detail(TOGGLE_KEY, user, default=False)
        print('detail: ' + str(is_open_detail.reason))
        print('rule index: ' + str(is_open_detail.rule_index))

import logging

import featureprobe as fp
import random
import time

logging.basicConfig(level=logging.WARNING)

if __name__ == '__main__':
    # FEATURE_PROBE_SERVER_URL = 'http://localhost:4007'  # for local docker
    FEATURE_PROBE_SERVER_URL = 'https://featureprobe.io/server'  # for featureprobe.io

    config = fp.Config(remote_uri=FEATURE_PROBE_SERVER_URL,  # FeatureProbe server URL
                       sync_mode='pooling',
                       refresh_interval=2,
                       start_wait=5)

    # Server Side SDK Key for your project and environment
    SDK_KEY = 'server-9e53c5db4fd75049a69df8881f3bc90edd58fb06'
    with fp.Client(SDK_KEY, config) as client:
        if not client.initialized():
            print("SDK failed to initialize!")
        # Create one user
        # "userId" is used in rules, should be filled in.
        user = fp.User().with_attr('userId', '00001')

        # Get toggle result for this user.
        #TOGGLE_KEY = 'campaign_allow_list'
        TOGGLE_KEY = 'Event_Analysis'

        # Get toggle result for this user
        is_open = client.value(TOGGLE_KEY, user, default=False)
        print('feature for this user is: ' + str(is_open))

        # Demo of Detail function
        is_open_detail = client.value_detail(TOGGLE_KEY, user, default=False)
        print('detail: ' + str(is_open_detail.reason))
        print('rule index: ' + str(is_open_detail.rule_index))

        # Simulate conversion rate of 1000 users for a new feature
        #YOU_EVENT_NAME = "new_feature_conversion";
        YOU_EVENT_NAME = "multi_feature";
        for i in range(1000):
            event_user = fp.User().stable_rollout(str(time.time_ns() + i))
            new_feature = client.value(TOGGLE_KEY, event_user, '1')
            client.track(YOU_EVENT_NAME, event_user, random.randint(0, 99))
            print("New feature conversion.")
            time.sleep(0.2)
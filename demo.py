import logging

import featureprobe as fp

logging.basicConfig(level=logging.WARNING)

if __name__ == '__main__':
    config = fp.Config(remote_uri='http://127.0.0.1:4007',  # FeatureProbe server URL
                       sync_mode='pooling',
                       refresh_interval=3)

    client = fp.Client('server-8ed48815ef044428826787e9a238b9c6a479f98c',
                       # Server Side SDK Key for your project and environment
                       config)

    # create one user, with id='user_unique_id' and one attribute
    user = fp.User('user_unique_id', {'city': 'New York'})
    discount = float(client.evaluate('promotion_activity',  # Toggle you want to use
                                     user, default=0))
    print('user in New York has a discount of : %d' % discount)

    detail = client.evaluate_detail('promotion_activity', user, default=0)
    print('detail: %s' % detail.reason)
    # rule_index = None on default rule is hit
    print('rule index: ' + str(detail.rule_index))

    user2 = fp.User('user_id2')
    # create another user, here's the alternative way to set user attributes
    user2['city'] = 'Paris'

    discount = float(client.evaluate('promotion_activity', user2, default=0))
    print('user in Paris has a discount of : %d' % discount)

    detail2 = client.evaluate_detail('promotion_activity', user2, default=0)
    print('detail2: %s' % detail2.reason)
    print('rule index: %d' % detail2.rule_index)

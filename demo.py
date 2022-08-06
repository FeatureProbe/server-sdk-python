import logging
import time
import featureprobe as fp


logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    config = fp.Config(remote_uri='http://127.0.0.1:4007', sync_mode='pooling')
    client = fp.Client('server-8ed48815ef044428826787e9a238b9c6a479f98c', config)

    user = fp.User('user_unique_id', {
        'userId': '9876',
        'tel': '12345678998'
    })
    eval_ = client.evaluate('promotion_activity', user, default=-1)
    client.flush()
    time.sleep(1)

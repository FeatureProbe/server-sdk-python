import os
import time

import featureprobe as fp
import logging

logging.basicConfig(level=logging.DEBUG)

config = fp.Config(remote_uri='http://127.0.0.1:4007',
                   sync_mode='pooling',
                   refresh_interval=1)
client = fp.Client('server-be0bd573697764cee1b2d12ab682b7a6e8776778',
                   config)


if __name__ == '__main__':
    user = fp.User('user_unique_id', {
        'userId': '9238',
        'tel': '12345678998'
    })
    eval_ = client.evaluate('demo', user, 'Test')
    print(eval_)
    time.sleep(10)

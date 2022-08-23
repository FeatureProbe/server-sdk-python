import os.path
import pathlib

timezone = os.environ.get('TZ')

if timezone is None:
    try:
        if os.path.exists('/etc/timezone'):
            timezone = pathlib.Path('/etc/timezone').read_text()
        else:
            timezone = 'Asia/Shanghai'
    except:
        timezone = 'Asia/Shanghai'

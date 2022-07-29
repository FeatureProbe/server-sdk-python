import time

import featureprobe as fp


def _timestamp():
    return int(time.time())


def setup_function():
    global recorder, event  # noqa
    recorder = fp.AccessRecorder()
    user = fp.User('test_user')
    event = fp.AccessEvent(_timestamp(), user,
                           key='test_toggle', value='true',
                           version=1, index=0)


def test_add_event():
    recorder.add(event)
    assert recorder.start_time > 0
    assert recorder.end_time == 0
    assert recorder.counters.get('test_toggle')[0].value == 'true'
    assert recorder.counters.get('test_toggle')[0].count == 1
    assert recorder.counters.get('test_toggle')[0].version == 1
    assert recorder.counters.get('test_toggle')[0].index == 0


def test_get_snapshot():
    recorder.add(event)
    snapshot = recorder.snapshot()
    assert len(snapshot.counters) == 1
    assert len(snapshot.counters.get('test_toggle')) == 1

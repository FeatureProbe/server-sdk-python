import json

import featureprobe as fp


def test_serialize_toggles_to_repo():
    with open('tests/resources/datasource/repo.json') as f:
        dic = json.load(f)
    repo = fp.Repository.from_json(dic)
    assert len(repo.toggles) >= 1

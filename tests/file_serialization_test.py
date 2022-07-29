import featureprobe as fp


def test_local_mode_synchronizer():
    config = fp.Config(sync_mode='file', location='tests/resources/datasource/repo.json')
    feature_probe = fp.Sdk(sdk_key='server-61db54ecea79824cae3ac38d73f1961d698d0477',
                           config=config)
    repo = feature_probe._data_repo
    assert len(repo.get_all_toggle()) > 0
    assert len(repo.get_all_segment()) > 0

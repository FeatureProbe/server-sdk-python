import featureprobe as fp


def test_local_mode_synchronizer():
    feature_probe = fp.Sdk(sdk_key='server-61db54ecea79824cae3ac38d73f1961d698d0477')
    repo = feature_probe._data_repo
    # TODO

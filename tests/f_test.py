import featureprobe as fp


def test_a():
    f = fp.FileSynchronizer(fp.MemoryDataRepository(), 'resources/datasource/repo2.json')
    f.sync()

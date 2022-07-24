# -*- coding: UTF-8 -*-

import featureprobe as fp

if __name__ == '__main__':
    fs = fp.FileSynchronizer(fp.MemoryDataRepository(), './tests/resources/datasource/repo.json')
    fs.sync()

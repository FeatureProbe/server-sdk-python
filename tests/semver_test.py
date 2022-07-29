import pytest

from featureprobe.internal.semver import SemVer


def test_create():
    SemVer('1.0.0')
    SemVer('1.0.0-alpha')
    SemVer('1.0.0-alpha.1')
    SemVer('1.0.0-alpha.1+sha.000100000')


def test_bad_create():
    with pytest.raises(ValueError):
        SemVer(None)  # noqa
    with pytest.raises(ValueError):
        SemVer(1)  # noqa
    with pytest.raises(ValueError):
        SemVer('1.0')
    with pytest.raises(ValueError):
        SemVer('1.0.0-??!!')


def test_simple_1():
    assert SemVer('1.0.1') == SemVer('1.0.1')
    assert SemVer('1.0.1') <= SemVer('1.0.1')
    assert SemVer('1.0.1') >= SemVer('1.0.1')
    assert SemVer('1.1.1') > SemVer('1.0.1')
    assert SemVer('1.0.1') != SemVer('1.0.2')


def test_simple_2():
    assert SemVer('1.0.1') < SemVer('2.0.1')
    assert SemVer('1.0.1') > SemVer('1.0.1-alpha')
    assert SemVer('1.0.1-1') < SemVer('1.0.1-rc1')
    assert SemVer('1.0.1-beta') > SemVer('1.0.1-alpha')
    assert SemVer('1.0.1-beta') < SemVer('1.0.1-beta.1')
    assert SemVer('1.0.1-beta.1') < SemVer('1.0.1-beta.2')


def test_misc():
    assert False == (SemVer('1.0.0') > 1.0)

# Copyright 2022 FeatureProbe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from typing import Union


def peer_cmp_only(func):
    def type_check(self, other):
        return func(self, other) if isinstance(other, SemVer) else False

    return type_check


class SemVer:
    """Under the [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) standard."""

    __slots__ = ('major', 'minor', 'patch', 'pre_release')

    # https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
    FORMAT = re.compile(r'^(?P<major>0|[1-9]\d*)\.'
                        r'(?P<minor>0|[1-9]\d*)\.'
                        r'(?P<patch>0|[1-9]\d*)'
                        r'(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][\da-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][\da-zA-Z-]*))*))?'  # noqa
                        r'(?:\+(?P<buildmetadata>[\da-zA-Z-]+(?:\.[\da-zA-Z-]+)*))?$')

    def __init__(self, semver: Union[str, bytes]):
        try:
            parsed = self.FORMAT.match(semver).groupdict()
        except (TypeError, AttributeError) as e:
            # TypeError: semver is not str or bytes
            # AttributeError: invalid semver repr, leads re.match -> NoneType
            raise ValueError(
                'Bad semantic version representation \'%s\'' %
                semver) from e

        self.major = int(parsed['major'])
        self.minor = int(parsed['minor'])
        self.patch = int(parsed['patch'])
        self.pre_release = parsed['prerelease']

    def _cmp(self, sv):
        if self.major != sv.major:
            return self.major - sv.major
        if self.minor != sv.minor:
            return self.minor - sv.minor
        if self.patch != sv.patch:
            return self.patch - sv.patch

        if self.pre_release is None and sv.pre_release is None:
            return 0
        if self.pre_release is None or sv.pre_release is None:
            return 1 if self.pre_release is None else -1

        self_release = self.pre_release.split('.')
        other_release = sv.pre_release.split('.')

        for i in range(min(len(self_release), len(other_release))):
            res = SemVer._cmp_release(self_release[i], other_release[i])
            if res != 0:
                return res

        return len(self_release) - len(other_release)

    @staticmethod
    def _cmp_release(i, o):
        i_int, o_int = True, True
        try:
            i = int(i)
        except ValueError:
            i_int = False
        try:
            o = int(o)
        except ValueError:
            o_int = False

        if i_int and o_int:
            return i - o
        if i_int or o_int:
            return 1 if o_int else -1

        if i == o:
            return 0
        return 1 if i > o else -1

    @peer_cmp_only
    def __eq__(self, other):
        return self._cmp(other) == 0

    @peer_cmp_only
    def __gt__(self, other):
        return self._cmp(other) > 0

    @peer_cmp_only
    def __ge__(self, other):
        return self._cmp(other) >= 0

    @peer_cmp_only
    def __lt__(self, other):
        return self._cmp(other) < 0

    @peer_cmp_only
    def __le__(self, other):
        return self._cmp(other) <= 0

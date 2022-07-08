# -*- coding: UTF-8 -*-

# Copyright 2022 FeatureProbe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional
from hashlib import sha1

from featureprobe.fp_user import FPUser
from hit_result import HitResult


class Split:
    __BUCKET_SIZE = 10000
    __INVALID_INDEX = -1

    def __init__(self, distribution: List[List[List[int]]] = None):
        self._distribution = distribution or []
        self.bucket_by = ''
        self.salt = ''

    @property
    def distribution(self) -> List[List[List[int]]]:
        return self._distribution

    @distribution.setter
    def distribution(self, distribution: List[List[List[int]]]):
        self._distribution = distribution

    @property
    def bucket_by(self) -> str:
        return self._bucket_by

    @bucket_by.setter
    def bucket_by(self, bucket_by: str):
        self._bucket_by = bucket_by

    @property
    def salt(self) -> str:
        return self._salt

    @salt.setter
    def salt(self, salt: str):
        self._salt = salt

    def find_index(self, user: FPUser, toggle_key: str) -> HitResult:
        hash_key = user.key
        if self._bucket_by:
            if user.has_attr(self._bucket_by):
                hash_key = user.attrs.get(self._bucket_by)
            else:
                return HitResult(False,
                                 reason='Warning: User with key \'%s\' does not have attribute name \'%s\''
                                        % (user.key, self._bucket_by))
        group_index = self.__get_group(self.__hash(hash_key, self._salt or toggle_key, self.__BUCKET_SIZE))
        return HitResult(True, index=group_index,
                         reason='selected %d percentage group' % group_index)

    def __get_group(self, hash_value) -> Optional[int]:
        for index, groups in enumerate(self._distribution):
            for rng in groups:
                if rng[0] <= hash_value < rng[1]:
                    return index
        return None

    @staticmethod
    def __hash(hash_key, hash_salt, bucket_size):
        value = (hash_key + hash_salt).encode('utf-8')
        sha = sha1(value)
        _bytes = sha.digest()[-4:]
        return int.from_bytes(_bytes, byteorder='big') % bucket_size

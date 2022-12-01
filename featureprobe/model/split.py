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

from hashlib import sha1
from typing import List, Optional, TYPE_CHECKING

from featureprobe.hit_result import HitResult
from featureprobe.internal.json_decoder import json_decoder

if TYPE_CHECKING:
    from featureprobe.user import User


class Split:
    _BUCKET_SIZE = 10000

    def __init__(self,
                 distribution: List[List[List[int]]],
                 bucket_by: str,
                 salt: str):
        self._distribution = distribution or []
        self._bucket_by = bucket_by
        self._salt = salt

    @classmethod
    @json_decoder
    def from_json(cls, json: dict) -> "Split":
        distribution = json.get('distribution')
        bucket_by = json.get('bucketBy')
        salt = json.get('salt')
        return cls(distribution, bucket_by, salt)

    @property
    def distribution(self) -> List[List[List[int]]]:
        return self._distribution

    @distribution.setter
    def distribution(self, value: List[List[List[int]]]):
        self._distribution = value or []

    @property
    def bucket_by(self) -> str:
        return self._bucket_by

    @bucket_by.setter
    def bucket_by(self, value: str):
        self._bucket_by = value

    @property
    def salt(self) -> str:
        return self._salt

    @salt.setter
    def salt(self, value: str):
        self._salt = value

    def find_index(self, user: "User", toggle_key: str) -> "HitResult":
        hash_key = user.key
        if self._bucket_by:
            if user.has_attr(self._bucket_by):
                hash_key = user.attrs.get(self._bucket_by)
            else:
                return HitResult(
                    hit=False,
                    reason='Warning: User with key \'%s\' does not have attribute name \'%s\'' %
                    (user.key,
                     self._bucket_by))
        group_index = self._get_group(
            self._hash(
                hash_key,
                self._salt or toggle_key,
                self._BUCKET_SIZE))
        return HitResult(hit=True, index=group_index,
                         reason='selected %d percentage group' % group_index)

    def _get_group(self, hash_value: int) -> int:
        for index, groups in enumerate(self._distribution):
            for rng in groups:
                if rng[0] <= hash_value < rng[1]:
                    return index
        return -1  # TODO: return None, HitResult.hit = False? inconsistent with Java SDK

    @staticmethod
    def _hash(hash_key: str, hash_salt: str, bucket_size: int) -> int:
        value = (hash_key + hash_salt).encode('utf-8')
        sha = sha1(value)
        _bytes = sha.digest()[-4:]
        return int.from_bytes(_bytes, byteorder='big') % bucket_size

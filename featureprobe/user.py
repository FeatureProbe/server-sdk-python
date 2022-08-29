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

import time
from typing import Dict


class User:
    """A collection of attributes that can affect toggle evaluation.

    Usually corresponding to a user of your application.
    """

    def __init__(self, attrs: Dict[str, str] = None,
                 stable_rollout_key: str = None):
        """Creates a new FeatureProbe User.

        :param attrs: (optional) The initialize attribute for a user.
        :param stable_rollout_key: User unique ID for percentage rollout.
        """
        if stable_rollout_key is not None:
            self._key = stable_rollout_key
        else:
            self._key = str(int(time.time() * 10**6))
        self._attrs = attrs or {}

    def __setitem__(self, key: str, value: str):
        """Alias for :func:`~featureprobe.User.with_attr`.

        Usage::

          >>> import featureprobe as fp
          >>> user = fp.User('unique id')
          >>> user.with_attr('key1', 'value1')
          >>> user['key2'] = 'value2'
        """
        self._attrs[key] = value

    def __getitem__(self, attr: str):
        """Gets the value of specified attribute.

        :param attr: Attribute name / key.
        :returns: str or None

        Usage::

          >>> import featureprobe as fp
          >>> user = fp.User('unique id', { 'key': 'value' })
          >>> user['key']  # 'value'
        """
        try:
            return self._attrs[attr]
        except KeyError:
            return None

    def __delitem__(self, key: str):
        self._attrs.pop(key, None)

    def stable_rollout(self, key):
        self._key = key
        return self

    def to_dict(self) -> dict:
        return {
            'key': self._key,
            'attrs': self._attrs,
        }

    @property
    def key(self) -> str:
        """Gets FeatureProbe User unique identifier"""
        return self._key

    @property
    def attrs(self) -> Dict[str, str]:
        """Gets all attributes of a FeatureProbe User"""
        return self._attrs

    @attrs.setter
    def attrs(self, attrs: Dict[str, str]):
        """Sets (replace the original attributes) multiple attributes to a FeatureProbe User"""
        self._attrs = attrs

    def with_attr(self, key: str, value: str) -> "User":
        """Adds an attribute to the user.

        :param key: Attribute key / name.
        :param value: Attribute value.
        :returns: User

        Usage::

          >>> import featureprobe as fp
          >>> user = fp.User('unique id').with_attr('key1', 'value1').with_attr('key2', 'value2')
        """
        self._attrs[key] = value
        return self

    def has_attr(self, attr: str) -> bool:
        """Checks if an attribute exists.

        :param attr: Attribute name / key.
        :returns: bool
        """
        return attr in self._attrs

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

def stringifiable(cls):
    """Experimental, unusable yet"""

    def __str__(self):
        attrs = sorted(filter(lambda attr: not callable(attr[1]),
                              self.__dict__.items()))

        return '%s(%s)' % (
            cls.__name__,
            ', '.join(
                '%s=\'%s\'' % item
                if isinstance(item[1], (str, bytes))
                else '%s=%s' % item
                for item in attrs
            )
        )

    cls.__str__ = __str__
    return cls

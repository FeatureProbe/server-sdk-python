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

import warnings


def _nameof(anything):
    if callable(anything):
        return "function<{}>".format(anything.__name__)
    elif isinstance(anything, property):
        return "property<{}>".format(anything.fget.__name__)
    # TODO: add more type support
    else:
        return None


def deprecated(*, since: str = None, successor=None):
    """Marks functions as deprecated."""

    def wrapper(func):
        def inner(*args, **kwargs):
            successor_name = _nameof(successor)
            warnings.warn(
                "{} is deprecated{}{}".format(
                    _nameof(func),
                    " since " + since if since is not None else "",
                    ", consider using {} instead.".format(successor_name)
                    if successor_name is not None
                    else "",
                ),
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return inner

    return wrapper

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

import asyncio


def finish_future(func):
    """Fires async functions without waiting it for finish."""
    def wrapped(*args, **kwargs):
        return asyncio.run_coroutine_threadsafe(func(*args, **kwargs), asyncio.get_event_loop())

    return wrapped


@finish_future
async def aaa(n):
    for i in range(n):
        print(i)

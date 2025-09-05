# Copyright 2022 Webull
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding=utf-8
import abc
from webull.core.vendored.six import add_metaclass


@add_metaclass(abc.ABCMeta)
class BaseQuotesPayloadDecoder(object):
    def __init__(self):
        pass

    @abc.abstractclassmethod
    def parse(self, payload):
        pass


class Utf8Decoder(BaseQuotesPayloadDecoder):
    def __init__(self):
        super().__init__()

    def parse(self, payload):
        return str(payload.decode("utf-8"))

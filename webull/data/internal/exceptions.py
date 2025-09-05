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

from webull.data.common.connect_ack import ConnectAck


# coding=utf-8

class ConnectException(Exception):
    def __init__(self, rc_code, msg=""):
        Exception.__init__(self)
        self.error_code = rc_code
        self.error_msg = msg

    def get_error_code(self):
        return self.error_code

    def get_error_msg(self):
        return self.error_msg

    def __str__(self):
        return "rc code: %s, msg: %s" % (self.error_code, self.error_msg)


class ExitedException(ConnectException):
    def __init__(self):
        ConnectException.__init__(
            self, 0, "exited exception which used to stop processing manually")


class LoopException(Exception):
    def __init__(self, loop_code, msg=""):
        Exception.__init__(self)
        self.error_code = loop_code
        self.error_msg = msg

    def get_error_code(self):
        return self.error_code

    def get_error_msg(self):
        return self.error_msg

    def __str__(self):
        error_msg = self.error_msg
        if not error_msg:
            ack = ConnectAck.from_code(self.error_code)
            if ack is not None:
                error_msg = ack.value[1]
        return "loop ack code: %s, msg: %s" % (self.error_code, error_msg)

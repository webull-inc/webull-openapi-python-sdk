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


def desensitize_token(token, keep_length=6, mask_length=6):
    if not token:
        return token

    total_length = len(token)

    # 如果字符串长度不足需要保留长度的两倍，则返回全部内容
    if total_length <= keep_length * 2:
        return token

    # 提取前保留部分、后保留部分，并用星号连接
    front_part = token[:keep_length]
    rear_part = token[-keep_length:] if keep_length > 0 else ''
    mask = '*' * mask_length

    return f"{front_part}{mask}{rear_part}"
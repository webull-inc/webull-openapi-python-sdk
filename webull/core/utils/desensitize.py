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


import re

_MASK = "******"

_TOKEN_KEYS = (
    "token", "access_token", "accesstoken", "x-access-token", "refresh_token", "refreshtoken",
)

_SECRET_KEYS = (
    "app_key", "appkey", "x-app-key", "app_secret", "appsecret", "secret_key", "secretkey",
    "secret", "signature", "x-signature", "authorization",
)

_SENSITIVE_KEYS = _TOKEN_KEYS + _SECRET_KEYS

_KEYS_REGEX = "|".join(re.escape(k) for k in sorted(_SENSITIVE_KEYS, key=len, reverse=True))

# Quoted form, including JSON nested inside a JSON string (escaped quotes):
#   "token": "abc"   'x-signature': 'abc'   \\"token\\":\\"abc\\"
_QUOTED_PATTERN = re.compile(
    r"""(?P<key>(?P<kq>\\{0,2}["'])(?:%s)(?P=kq)\s*[:=]\s*)(?P<vq>\\{0,2}["'])(?P<value>.*?)(?P=vq)""" % _KEYS_REGEX,
    re.IGNORECASE | re.DOTALL)

# Unquoted form, e.g. plain text bodies or query strings: token=abc, x-app-key: abc
_UNQUOTED_PATTERN = re.compile(
    r"""(?<![\w-])(?P<key>(?:%s)\s*[:=]\s*)(?P<value>(?:(?:bearer|basic)\s+)?[^\s&,;"'\\}\]\)]+)""" % _KEYS_REGEX,
    re.IGNORECASE)


def desensitize_token(token, keep_length=6, mask_length=6):
    """Keep only the first 6 characters of a token, e.g. 28b9f3******."""
    if not token:
        return token
    token = str(token)
    if len(token) <= keep_length:
        return _MASK
    return token[:keep_length] + '*' * mask_length


def desensitize_secret(value, keep_length=4, mask_length=3):
    """Mask an app key, app secret or signature: first 4 + *** + last 4.

    Values shorter than 12 characters are fully masked.
    """
    if not value:
        return value
    value = str(value)
    if len(value) < 12:
        return '*' * len(value)
    return value[:keep_length] + '*' * mask_length + value[-keep_length:]


def _mask_value(key, value):
    if key.lower() in _TOKEN_KEYS:
        return desensitize_token(value)
    return desensitize_secret(value)


def mask_sensitive_text(text):
    """Mask sensitive key/value pairs inside a JSON string or the repr of a dict.

    Handles both quote styles, e.g. {"token": "abc..."} and {'x-signature': 'abc...'}.
    Bytes are decoded as utf-8 first. Returns the input unchanged when it is empty.
    """
    if not text:
        return text
    if isinstance(text, (bytes, bytearray)):
        text = bytes(text).decode("utf-8", errors="replace")
    elif not isinstance(text, str):
        text = str(text)

    def _replace_quoted(match):
        key = match.group("key")
        name = re.sub(r"""[\\"'\s:=]""", "", key)
        return "%s%s%s%s" % (key, match.group("vq"), _mask_value(name, match.group("value")), match.group("vq"))

    def _replace_unquoted(match):
        key = match.group("key")
        name = re.sub(r"""[\s:=]""", "", key)
        return "%s%s" % (key, _mask_value(name, match.group("value")))

    return _UNQUOTED_PATTERN.sub(_replace_unquoted, _QUOTED_PATTERN.sub(_replace_quoted, text))


def mask_value_in_text(text, value):
    """Replace every occurrence of a secret value inside text with its masked form."""
    if not text or not value:
        return text
    return text.replace(str(value), desensitize_secret(value))


def mask_sensitive_headers(headers):
    """Return a copy of a header-like mapping with sensitive values masked."""
    if not headers:
        return headers
    masked = {}
    for key, value in dict(headers).items():
        if isinstance(key, str) and key.lower() in _SENSITIVE_KEYS:
            masked[key] = _mask_value(key, value)
        else:
            masked[key] = value
    return masked

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

# Default event name used when the server omits the "event" field.
DEFAULT_EVENT_NAME = "message"

_FIELD_EVENT = "event"
_FIELD_DATA = "data"


def _decode_line(line):
    if line is None:
        return None
    if isinstance(line, bytes):
        return line.decode("utf-8", "replace")
    return line


def iter_sse_frames(lines):
    """Turn a raw SSE line stream into (event_name, data) tuples.

    Args:
        lines: iterator over the response lines, either bytes or str.
            Typically ``httpx.Response.iter_lines()``.

    Yields:
        tuple of (event name, data payload). Multiple ``data:`` lines of the
        same frame are joined with a newline, as required by the SSE spec.
    """
    event_name = None
    data_lines = []
    for raw_line in lines:
        line = _decode_line(raw_line)
        if line is None:
            continue
        line = line.rstrip("\r")
        if not line:
            # Blank line terminates the current frame.
            if event_name is not None or data_lines:
                yield event_name or DEFAULT_EVENT_NAME, "\n".join(data_lines)
                event_name = None
                data_lines = []
            continue
        if line.startswith(":"):
            # Comment line, used by some servers to keep the connection alive.
            continue
        field, _, value = line.partition(":")
        if value.startswith(" "):
            value = value[1:]
        if field == _FIELD_EVENT:
            event_name = value
        elif field == _FIELD_DATA:
            data_lines.append(value)
        # Other fields (id, retry) are not used by this channel.
    if event_name is not None or data_lines:
        yield event_name or DEFAULT_EVENT_NAME, "\n".join(data_lines)

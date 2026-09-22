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
import logging

from webull.core.auth.algorithm import sha_hmac256_new
from webull.core.auth.composer import default_signature_composer
import webull.core.headers as hd
import webull.core.utils.common as core_common

logger = logging.getLogger(__name__)


def _build_sign_headers(app_key_id, signer_spec):
    return {
        hd.APP_KEY: app_key_id,
        hd.SIGN_ALGORITHM: signer_spec.get_signer_name(),
        hd.SIGN_VERSION: signer_spec.get_signer_version(),
        hd.NONCE: core_common.get_uuid(),
        hd.TIMESTAMP: core_common.get_iso_8601_date()
    }


def _get_body_string(body_bytes, signer_spec):
    """Hash the exact bytes that will be sent as the HTTP request body.

    The SSE channel signs the raw JSON body bytes, unlike the gRPC channel
    which signs the protobuf serialized bytes of SubscribeRequest.
    """
    if body_bytes:
        if signer_spec == sha_hmac256_new:
            return core_common.sha256_hex(body_bytes)
        return core_common.md5_hex(body_bytes)
    return None


def calc_signature(app_key_id, app_key_secret, body_bytes, signer_spec):
    """Sign an SSE subscribe request.

    Args:
        app_key_id: application app key.
        app_key_secret: application app secret.
        body_bytes: raw bytes of the JSON request body, exactly as sent.
        signer_spec: signing algorithm module, e.g. sha_hmac256_new or sha_hmac1.

    Returns:
        tuple of (signature, headers dict) where headers already contains the
        five signing headers plus x-signature.
    """
    headers = _build_sign_headers(app_key_id, signer_spec)
    sign_params = default_signature_composer._lower_key_dict(headers)
    logger.debug("sign_params:%s", sign_params)
    body_string = _get_body_string(body_bytes, signer_spec)
    logger.debug("body_string:%s", body_string)
    string_to_sign = default_signature_composer._build_sign_string(
        sign_params, None, body_string)
    logger.debug("string_to_sign:%s", string_to_sign)
    signature = default_signature_composer._gen_signature(
        string_to_sign, app_key_secret, signer_spec)
    headers[hd.SIGNATURE] = signature
    return signature, headers

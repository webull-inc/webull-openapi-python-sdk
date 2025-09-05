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

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# coding=utf-8

"""
This file borrowed some of its methods from a  modified fork of the
https://github.com/aliyun/aliyun-openapi-python-sdk/blob/master/aliyun-python-sdk-core/aliyunsdkcore/endpoint/chained_endpoint_resolver.py
which was part of Alibaba Group.
"""

from webull.core.exception.exceptions import ClientException
from webull.core.exception import error_code
from webull.core.endpoint import EndpointResolver

class ChainedEndpointResolver(EndpointResolver):
    def __init__(self, resolver_chain):
        EndpointResolver.__init__(self)
        self.endpoint_resolvers = resolver_chain
        
    def resolve(self, request):
        for resolver in self.endpoint_resolvers:
            endpoint = resolver.resolve(request) 
            if endpoint is not None:
                return endpoint
            
        raise ClientException(error_code.SDK_ENDPOINT_RESOLVING_ERROR)
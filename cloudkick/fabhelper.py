# Licensed to Cloudkick, Inc ('Cloudkick') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# Cloudkick licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__all__ = ["hosts", "roledefs", "load"]

import sys
from collections import defaultdict

from cloudkick.base import Connection

_CACHED_NODES = None

def _get_data():
    global _CACHED_NODES 
    if _CACHED_NODES is None:
        c = Connection()
        _CACHED_NODES = c.nodes.list()
    return _CACHED_NODES


def hosts():
    # TODO: need generic DNS (?)
    d = _get_data()
    return [node.get("ipaddress") for node in _get_data()]


def roledefs():
        rd = defaultdict(list)
        for node in _get_data():
            for t in node.get("tags"):
                rd[t].append(node.get("ipaddress"))
        return rd


def load(x = None):
    from fabric.api import env
    try:
        env.hosts = hosts()
        env.roledefs = roledefs()
    except IOError, e:
        # Don't print a huge stack trace if there's a problem. Most likely cloudkick.conf isn't in the path.
        print e
        sys.exit()
    return x

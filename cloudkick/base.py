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


__all__ = ["Connection"]

import os
import urllib
from oauth import oauth

try:
  import json
except ImportError:
  import simplejson as json


class Connection(object):
    """
    Cloudkick API Connection Object

    Provides an interface to the Cloudkick API over an HTTPS connection,
    using OAuth to authenticate requests.
    """

    API_SERVER = "api.cloudkick.com"
    API_VERSION = "2.0"

    def __init__(self, config_path=None, oauth_key=None, oauth_secret=None):
        self.__oauth_key = oauth_key or None
        self.__oauth_secret = oauth_secret or None
        if config_path is None:
            config_path = [os.path.join(os.path.expanduser('~'), ".cloudkick.conf"),
                           "/etc/cloudkick.conf"]
        if not isinstance(config_path, list):
            config_path = [config_path]
        self.config_path = config_path

    def _read_config(self):
        errors = []
        for path in self.config_path:
            try:
                fp = open(path, 'r')
                return self._parse_config(fp)
            except Exception, e:
                errors.append(e)
                continue
        raise IOError("Unable to open configuration files: %s %s" %
                        (", ".join(self.config_path),
                         ", ".join([str(e) for e in errors])))

    def _parse_config(self, fp):
        for line in fp.readlines():
            if len(line) < 1:
                continue
            if line[0] == "#":
                continue
            parts = line.split()
            if len(parts) != 2:
                continue
            key = parts[0].strip()
            value = parts[1].strip()
            if key == "oauth_key":
                self.__oauth_key = value
            if key == "oauth_secret":
                self.__oauth_secret = value

    @property
    def oauth_key(self):
        if not self.__oauth_key:
            self._read_config()
        return self.__oauth_key

    @property
    def oauth_secret(self):
        if not self.__oauth_secret:
            self._read_config()
        return self.__oauth_secret

    def _request(self, url, parameters=None, method='GET'):
        signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        consumer = oauth.OAuthConsumer(self.oauth_key, self.oauth_secret)
        url = 'https://' + self.API_SERVER + '/' + self.API_VERSION + '/' + url
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                                   http_url=url,
                                                                   parameters=parameters)
        oauth_request.sign_request(signature_method, consumer, None)
        url = oauth_request.to_url()
        f = urllib.urlopen(url)
        s = f.read()
        return s

    def _request_json(self, *args):
        r = self._request(*args)

        try:
            return json.loads(r)
        except ValueError:
            return r

    def nodes(self, query="*"):
        nodes = self._request_json("nodes", {'query': query})
        return nodes

    def checks(self):
        checks = self._request_json("checks")
        return checks

    def monitors(self):
        monitors = self._request_json("monitors")
        return monitors


if __name__ == "__main__":
    from pprint import pprint
    c = Connection()
    nodes = c.nodes()
    pprint(nodes)
    nid = nodes['items'][6]['id']
    checks = c.checks()
    pprint(checks)
    #check = checks[0][nid][0]
    #now = datetime.now()

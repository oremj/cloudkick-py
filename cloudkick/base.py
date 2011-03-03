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

    def _filter_params(self, params):
        """Filter out any null parameters"""
        return dict((k, v) for k, v in params.iteritems() if v is not None)

    def _request(self, url, parameters=None, method='GET'):
        if not parameters:
            parameters = None
        else:
            parameters = self._filter_params(parameters)

        signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        consumer = oauth.OAuthConsumer(self.oauth_key, self.oauth_secret)
        url = 'https://%s/%s/%s' % (self.API_SERVER, self.API_VERSION, url)
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                                   http_url=url,
                                                                   parameters=parameters)
        oauth_request.sign_request(signature_method, consumer, None)
        url = oauth_request.to_url()
        print url
        f = urllib.urlopen(url)
        s = f.read()
        return s

    def _request_json(self, *args):
        r = self._request(*args)

        try:
            return json.loads(r)
        except ValueError:
            return r

    def addresses(self):
        """Return a list of addresses on your account"""
        return self._request_json("addresses")

    def address_types(self):
        """Return a list of the types of addresses available to your account"""
        return self._request_json("address_types")

    def change_logs(self, startdate=None, enddate=None):
        """Returns a list of change logs in the system."""
        params = {
            'startdate': startdate,
            'enddate': enddate,
        }
        return self._request_json("change_logs", params)

    def checks(self, monitor_id=None, node_ids=None):
        """Returns the total list of all the checks in the system"""
        params = {
            'monitor_id': monitor_id,
            'node_ids': ",".join(node_ids),
        }
        return self._request_json("checks", params)

    def interesting_metrics(self):
        """Return a list of interesting metrics on your account"""
        return self._request_json("interesting_metrics")

    def monitors(self):
        """Returns the total list of all the monitors created in the UI
           as well as the API"""
        return self._request_json("monitors")

    def nodes(self, query="*"):
        """Returns a list of nodes for your account"""
        return self._request_json("nodes", {'query': query})

    def providers(self):
        """Return a list of providers on your account"""
        return self._request_json("providers")

    def provider_types(self):
        """Return list of types of providers available to your account"""
        return self._request_json("provider_types")

    def status_nodes(self, **kwargs):
        """Returns the status of a set of checks, filtered based on statuses

        Keywork arguments:
            overall_check_statuses -- Filter only checks with warning,
                                      error, or recovery messages
            check_id -- Filter the statuses based on the check id
            monitor_id -- Filter based on the monitor id
            query -- Filter based on a query string
            include_metrics -- Include the metrics with the response 

        """
        valid_params = ['overall_check_statuses', 'check_id',
                        'monitor_id', 'query', 'include_metrics']
        params = dict([(k,v) for k,v in kwargs.iteritems()
                             if k in valid_params])

        return self._request_json("status/nodes", params)

    def tags(self):
        "Return the list of tags preset on the account"""
        return self._request_json("tags")


if __name__ == "__main__":
    from pprint import pprint
    c = Connection()
    nodes = c.nodes()
    pprint(nodes)
    nids = [n['id'] for n in nodes['items']]
    checks = c.checks(node_ids=nids)
    pprint(checks)
    #check = checks[0][nid][0]
    #now = datetime.now()

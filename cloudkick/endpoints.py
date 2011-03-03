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


class _ApiEndpoint(object):
    """
    Base class for api endpoints
    """

    def __init__(self, conn):
        self.conn = conn


class Addresses(_ApiEndpoint):

    def list(self):
        """Return a list of addresses on your account"""
        return self.conn._request_json("addresses")


class AddressTypes(_ApiEndpoint):

    def list(self):
        """Return a list of the types of addresses available to your account"""
        return self.conn._request_json("address_types")


class ChangeLogs(_ApiEndpoint):

    def list(self, startdate=None, enddate=None):
        """Returns a list of change logs in the system."""
        params = {
            'startdate': startdate,
            'enddate': enddate,
        }
        return self.conn._request_json("change_logs", params)


class Checks(_ApiEndpoint):

    def list(self, monitor_id=None, node_ids=None):
        """Returns the total list of all the checks in the system"""
        params = {
            'monitor_id': monitor_id,
            'node_ids': ",".join(node_ids),
        }
        return self.conn._request_json("checks", params)


class InterestingMetrics(_ApiEndpoint):

    def list(self):
        """Return a list of interesting metrics on your account"""
        return self.conn._request_json("interesting_metrics")


class Monitors(_ApiEndpoint):

    def list(self):
        """Returns the total list of all the monitors created in the UI
           as well as the API"""
        return self.conn._request_json("monitors")


class Nodes(_ApiEndpoint):

    def list(self, query="*"):
        """Returns a list of nodes for your account"""
        return self.conn._request_json("nodes", {'query': query})


class Providers(_ApiEndpoint):

    def list(self):
        """Return a list of providers on your account"""
        return self.conn._request_json("providers")


class ProviderTypes(_ApiEndpoint):

    def list(self):
        """Return list of types of providers available to your account"""
        return self.conn._request_json("provider_types")


class StatusNodes(_ApiEndpoint):

    def list(self, **kwargs):
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
        params = dict([(k,v) for k, v in kwargs.iteritems()
                                if k in valid_params])

        return self.conn._request_json("status/nodes", params)


class Tags(_ApiEndpoint):

    def list(self):
        "Return the list of tags preset on the account"""
        return self.conn._request_json("tags")

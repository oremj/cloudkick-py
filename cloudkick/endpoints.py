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


class ApiEndPointException(Exception):
    """Base API exception"""
    pass

class _ApiEndpoint(object):
    """
    Base class for api endpoints
    """

    def __init__(self, conn):
        self._conn = conn

    def _req_json(self, *args, **kwargs):
        return self._conn._request_json(*args, **kwargs)


class Addresses(_ApiEndpoint):

    def list(self):
        """Return a list of addresses on your account"""
        return self._req_json("addresses")


class AddressTypes(_ApiEndpoint):

    def list(self):
        """Return a list of the types of addresses available to your account"""
        return self._req_json("address_types")


class ChangeLogs(_ApiEndpoint):

    def list(self, startdate=None, enddate=None):
        """Returns a list of change logs in the system."""
        params = {
            'startdate': startdate,
            'enddate': enddate,
        }
        return self._req_json("change_logs", params)


class Checks(_ApiEndpoint):

    def list(self, monitor_id=None, node_ids=None):
        """Returns the total list of all the checks in the system"""
        params = {
            'monitor_id': monitor_id,
            'node_ids': ",".join(node_ids),
        }
        return self._req_json("checks", params)


class InterestingMetrics(_ApiEndpoint):

    def list(self):
        """Return a list of interesting metrics on your account"""
        return self._req_json("interesting_metrics")


class Monitors(_ApiEndpoint):
    """https://support.cloudkick.com/API/2.0/Monitors"""

    def create(self, name, query, notes=None):
        params = {'name': name,
                  'query': query,
                  'notes': notes}

        return self._req_json("monitors", params, 'POST')

    def disable(self, m_id):
        return self._req_json("monitors/%s/disable" % m_id, None, 'POST')

    def enable(self, m_id):
        return self._req_json("monitors/%s/enable" % m_id, None, 'POST')

    def list(self):
        """Returns the total list of all the monitors created in the UI
           as well as the API"""
        return self._req_json("monitors")


class Nodes(_ApiEndpoint):
    """https://support.cloudkick.com/API/2.0/Nodes"""

    def _tag(self, op, node_id, tag_id, tag_name, do_create):
        if tag_id is None and tag_name is None:
            raise ApiEndPointException("You must pass either a tag_id or a tag_name")

        params = {'id': tag_id,
                  'name': tag_name,
                  'do_create': do_create}

        return self._req_json("nodes/%s/%s" % (node_id, op), params, 'POST')
        

    def add_tag(self, node_id, tag_id=None, tag_name=None, do_create=False):
        """Apply tag to a node

        Keyword arguments
            node_id - id of node to add tag
            tag_id - apply the tag with tag_id to the current node
            tag_name - apply the named tag to the current node
            do_create - create the tag if it doesn't exist (optional)

        """

        return self._tag('add_tag', node_id, tag_id, tag_name, do_create)

    def remove_tag(self, node_id, tag_id=None, tag_name=None, do_create=False):
        """Remove a tag from a node

        Keyword arguments
            node_id - id of node to add tag
            tag_id - apply the tag with tag_id to the current node
            tag_name - apply the named tag to the current node
            do_create - create the tag if it doesn't exist (optional)

        """

        return self._tag('remove_tag', node_id, tag_id, tag_name, do_create)

    def create(self, name, ip_address, details):
        """Creates a node on your account with a unique name
        
        Keyword arguments
            name - Name of the machine. This has to be unique over nodes 
                   that are online
            ip_address - The public ip address of the node
            details - This is a dictionary of nested key value pairs.
                      These properties get indexed and are later to be used 
                      in the query language. 

        """
        params = {'name': name,
                  'ip_address': ip_address,
                  'details': details}

        return self._req_json("nodes", params, 'POST')

    def list(self, query="*"):
        """Returns a list of nodes for your account"""
        return self._req_json("nodes", {'query': query})

    def update(self, node_id, name, ip_address,
                 details, ssh_user=None, ssh_port=None):
        """Updates node on your account
        
        Keyword arguments
            node_id - id of node to update
            name - Name of the machine. This has to be unique over nodes 
                   that are online
            ip_address - The public ip address of the node
            details - This is a dictionary of nested key value pairs.
                      These properties get indexed and are later to be used 
                      in the query language. 
            ssh_user - Username for ssh-ing onto server via webterm (optional)
            ssh_port - ssh port use for webterm (optional)

        """

        params = {'name': name,
                  'ip_address': ip_address,
                  'details': details,
                  'ssh_user': ssh_user,
                  'ssh_port': ssh_port}

        return self._req_json("nodes/%s" % node_id, params, 'POST')


class Providers(_ApiEndpoint):

    def list(self):
        """Return a list of providers on your account"""
        return self._req_json("providers")


class ProviderTypes(_ApiEndpoint):

    def list(self):
        """Return list of types of providers available to your account"""
        return self._req_json("provider_types")


class StatusNodes(_ApiEndpoint):

    def list(self, **kwargs):
        """Returns the status of a set of checks, filtered based on statuses

        Keyword arguments:
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

        return self._req_json("status/nodes", params)


class Tags(_ApiEndpoint):

    def list(self):
        "Return the list of tags preset on the account"""
        return self._req_json("tags")

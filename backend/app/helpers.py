"""This module will encode and parse the query string params."""
##############################################################################
# Copyright 2019 IBM Corp. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
##############################################################################

#from urlparse import parse_qs
from urllib.parse import urlparse
from urllib.parse import parse_qs


def parse_query_params(query_string):
    """
        Function to parse the query parameter string.
    """
    # Parse the query param string
    parsed = urlparse(query_string)
    print(parsed)
    query_params = dict(parse_qs(parsed.path))
    print(query_params)
    # Get the value from the list
    query_params = {k: v[0] for k, v in query_params.items()}
    return query_params


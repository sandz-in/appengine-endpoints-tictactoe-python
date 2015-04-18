#!/usr/bin/python

# Copyright (C) 2010-2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Helper model class for TicTacToe API.

Defines models for persisting and querying score data on a per user basis and
provides a method for returning a 401 Unauthorized when no current user can be
determined.
"""


from google.appengine.ext import endpoints
from google.appengine.ext import ndb

from endpoints_proto_datastore.ndb import EndpointsModel


TIME_FORMAT_STRING = '%b %d, %Y %I:%M:%S %p'


def get_endpoints_current_user(raise_unauthorized=True):
    """Returns a current user and (optionally) causes an HTTP 401 if no user.

    Args:
        raise_unauthorized: Boolean; defaults to True. If True, this method
            raises an exception which causes an HTTP 401 Unauthorized to be
            returned with the request.

    Returns:
        The signed in user if there is one, else None if there is no signed in
        user and raise_unauthorized is False.
    """
    current_user = endpoints.get_current_user()
    if raise_unauthorized and current_user is None:
        raise endpoints.UnauthorizedException('Invalid token.')
    return current_user


class Score(EndpointsModel):
    """Model to store scores that have been inserted by users.

    Since the played property is auto_now_add=True, Scores will document when
    they were inserted immediately after being stored.
    """
    outcome = ndb.StringProperty(required=True)
    played = ndb.DateTimeProperty(auto_now_add=True)
    player = ndb.UserProperty(required=False)

    @property
    def timestamp(self):
        """Property to format a datetime object to string."""
        return self.played.strftime(TIME_FORMAT_STRING)

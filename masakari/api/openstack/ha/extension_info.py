# Copyright (c) 2016 NTT DATA
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_log import log as logging
import six
from six.moves import http_client
import webob.exc

from masakari.api.openstack import extensions
from masakari.api.openstack import wsgi
from masakari import exception
from masakari.i18n import _LE

ALIAS = 'extensions'
LOG = logging.getLogger(__name__)
authorize = extensions.os_masakari_authorizer(ALIAS)


class FakeExtension(object):
    def __init__(self, name, alias, description=""):
        self.name = name
        self.alias = alias
        self.__doc__ = description
        self.version = -1


class ExtensionInfoController(wsgi.Controller):

    def __init__(self, extension_info):
        self.extension_info = extension_info

    def _translate(self, ext):
        ext_data = {}
        ext_data["name"] = ext.name
        ext_data["alias"] = ext.alias
        ext_data["description"] = ext.__doc__
        ext_data["namespace"] = ""
        ext_data["updated"] = ""
        ext_data["links"] = []
        return ext_data

    def _create_fake_ext(self, name, alias, description=""):
        return FakeExtension(name, alias, description)

    def _get_extensions(self, context):
        """Filter extensions list based on policy."""

        discoverable_extensions = dict()

        for alias, ext in six.iteritems(self.extension_info.get_extensions()):
            authorize = extensions.os_masakari_soft_authorizer(alias)
            if authorize(context, action='discoverable'):
                discoverable_extensions[alias] = ext
            else:
                LOG.debug("Filter out extension %s from discover list",
                          alias)

        return discoverable_extensions

    @extensions.expected_errors(())
    def index(self, req):
        context = req.environ['masakari.context']
        authorize(context)
        discoverable_extensions = self._get_extensions(context)
        sorted_ext_list = sorted(
            six.iteritems(discoverable_extensions))

        extensions = []
        for _alias, ext in sorted_ext_list:
            extensions.append(self._translate(ext))

        return dict(extensions=extensions)

    @extensions.expected_errors(http_client.NOT_FOUND)
    def show(self, req, id):
        context = req.environ['masakari.context']
        authorize(context)
        try:
            ext = self._get_extensions(context)[id]
        except KeyError:
            raise webob.exc.HTTPNotFound()

        return dict(extension=self._translate(ext))


class ExtensionInfo(extensions.V1APIExtensionBase):
    """Extension information."""

    name = "Extensions"
    alias = ALIAS
    version = 1

    def get_resources(self):
        resources = [
            extensions.ResourceExtension(
                ALIAS, ExtensionInfoController(self.extension_info),
                member_name='extension')]
        return resources

    def get_controller_extensions(self):
        return []


class LoadedExtensionInfo(object):
    """Keep track of all loaded API extensions."""

    def __init__(self):
        self.extensions = {}

    def register_extension(self, ext):
        if not self._check_extension(ext):
            return False

        alias = ext.alias

        if alias in self.extensions:
            raise exception.MasakariException(
                "Found duplicate extension: %s" % alias)
        self.extensions[alias] = ext
        return True

    def _check_extension(self, extension):
        """Checks for required methods in extension objects."""
        try:
            extension.is_valid()
        except AttributeError:
            LOG.exception(_LE("Exception loading extension"))
            return False

        return True

    def get_extensions(self):
        return self.extensions

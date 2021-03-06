#   Copyright 2021 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" Module """

from pylon.core.tools import log  # pylint: disable=E0611,E0401
from pylon.core.tools import module  # pylint: disable=E0611,E0401

from .api.artifacts_security_results_page import ArtifactsForSecurityResults, ArtifactDownload
from ..shared.utils.api_utils import add_resource_to_api


class Module(module.ModuleModel):
    """ Task module """

    def __init__(self, context, descriptor):
        self.context = context
        self.descriptor = descriptor

    def init(self):
        """ Init module """
        log.info("Initializing module Artifacts")
        from .api.buckets import Buckets
        from .api.artifacts import Artifacts
        from .api.artifact import Artifact

        add_resource_to_api(self.context.api, Buckets, "/artifact/<int:project_id>")
        add_resource_to_api(self.context.api, Artifacts, "/artifact/<int:project_id>/<string:bucket>")
        add_resource_to_api(self.context.api, Artifact, "/artifact/<int:project_id>/<string:bucket>/<string:filename>")
        #TODO: rename in interceptor
        add_resource_to_api(self.context.api, Artifact, "/artifacts/<int:project_id>/<string:bucket>/<string:filename>",
                            endpoint="artifact_old")

        add_resource_to_api(self.context.api, ArtifactsForSecurityResults, "/artifact/security/<int:run_id>")
        add_resource_to_api(self.context.api, ArtifactDownload, "/artifact/security/<int:run_id>/<string:filename>")

    def deinit(self):  # pylint: disable=R0201
        """ De-init module """
        log.info("De-initializing module Artifacts")

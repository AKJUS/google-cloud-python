# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import OrderedDict
from http import HTTPStatus
import json
import logging as std_logging
import os
import re
from typing import (
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)
import warnings

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore
import google.protobuf

from google.cloud.securitycenter_v2 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.securitycenter_v2.services.security_center import pagers
from google.cloud.securitycenter_v2.types import (
    access,
    affected_resources,
    ai_model,
    application,
    attack_exposure,
    attack_path,
    backup_disaster_recovery,
    bigquery_export,
    chokepoint,
    cloud_armor,
    cloud_dlp_data_profile,
    cloud_dlp_inspection,
    compliance,
    connection,
    container,
    data_access_event,
    data_flow_event,
    data_retention_deletion_event,
    database,
    disk,
    exfiltration,
)
from google.cloud.securitycenter_v2.types import (
    group_membership,
    iam_binding,
    indicator,
    ip_rules,
    job,
    kernel_rootkit,
    kubernetes,
    load_balancer,
    log_entry,
    mitre_attack,
)
from google.cloud.securitycenter_v2.types import (
    security_posture,
    securitycenter_service,
    simulation,
)
from google.cloud.securitycenter_v2.types import (
    toxic_combination,
    valued_resource,
    vertex_ai,
    vulnerability,
)
from google.cloud.securitycenter_v2.types import external_system as gcs_external_system
from google.cloud.securitycenter_v2.types import (
    notification_config as gcs_notification_config,
)
from google.cloud.securitycenter_v2.types import (
    resource_value_config as gcs_resource_value_config,
)
from google.cloud.securitycenter_v2.types import security_marks as gcs_security_marks
from google.cloud.securitycenter_v2.types import file
from google.cloud.securitycenter_v2.types import finding
from google.cloud.securitycenter_v2.types import finding as gcs_finding
from google.cloud.securitycenter_v2.types import mute_config
from google.cloud.securitycenter_v2.types import mute_config as gcs_mute_config
from google.cloud.securitycenter_v2.types import network, notebook
from google.cloud.securitycenter_v2.types import notification_config
from google.cloud.securitycenter_v2.types import org_policy, process, resource
from google.cloud.securitycenter_v2.types import resource_value_config
from google.cloud.securitycenter_v2.types import security_marks
from google.cloud.securitycenter_v2.types import source
from google.cloud.securitycenter_v2.types import source as gcs_source

from .transports.base import DEFAULT_CLIENT_INFO, SecurityCenterTransport
from .transports.grpc import SecurityCenterGrpcTransport
from .transports.grpc_asyncio import SecurityCenterGrpcAsyncIOTransport
from .transports.rest import SecurityCenterRestTransport


class SecurityCenterClientMeta(type):
    """Metaclass for the SecurityCenter client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[SecurityCenterTransport]]
    _transport_registry["grpc"] = SecurityCenterGrpcTransport
    _transport_registry["grpc_asyncio"] = SecurityCenterGrpcAsyncIOTransport
    _transport_registry["rest"] = SecurityCenterRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[SecurityCenterTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class SecurityCenterClient(metaclass=SecurityCenterClientMeta):
    """V2 APIs for Security Center service."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = "securitycenter.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "securitycenter.{UNIVERSE_DOMAIN}"
    _DEFAULT_UNIVERSE = "googleapis.com"

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SecurityCenterClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SecurityCenterClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SecurityCenterTransport:
        """Returns the transport used by the client instance.

        Returns:
            SecurityCenterTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def attack_path_path(
        organization: str,
        simulation: str,
        valued_resource: str,
        attack_path: str,
    ) -> str:
        """Returns a fully-qualified attack_path string."""
        return "organizations/{organization}/simulations/{simulation}/valuedResources/{valued_resource}/attackPaths/{attack_path}".format(
            organization=organization,
            simulation=simulation,
            valued_resource=valued_resource,
            attack_path=attack_path,
        )

    @staticmethod
    def parse_attack_path_path(path: str) -> Dict[str, str]:
        """Parses a attack_path path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/simulations/(?P<simulation>.+?)/valuedResources/(?P<valued_resource>.+?)/attackPaths/(?P<attack_path>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def big_query_export_path(
        organization: str,
        location: str,
        export: str,
    ) -> str:
        """Returns a fully-qualified big_query_export string."""
        return "organizations/{organization}/locations/{location}/bigQueryExports/{export}".format(
            organization=organization,
            location=location,
            export=export,
        )

    @staticmethod
    def parse_big_query_export_path(path: str) -> Dict[str, str]:
        """Parses a big_query_export path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/locations/(?P<location>.+?)/bigQueryExports/(?P<export>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def dlp_job_path(
        project: str,
        dlp_job: str,
    ) -> str:
        """Returns a fully-qualified dlp_job string."""
        return "projects/{project}/dlpJobs/{dlp_job}".format(
            project=project,
            dlp_job=dlp_job,
        )

    @staticmethod
    def parse_dlp_job_path(path: str) -> Dict[str, str]:
        """Parses a dlp_job path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/dlpJobs/(?P<dlp_job>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def external_system_path(
        organization: str,
        source: str,
        finding: str,
        externalsystem: str,
    ) -> str:
        """Returns a fully-qualified external_system string."""
        return "organizations/{organization}/sources/{source}/findings/{finding}/externalSystems/{externalsystem}".format(
            organization=organization,
            source=source,
            finding=finding,
            externalsystem=externalsystem,
        )

    @staticmethod
    def parse_external_system_path(path: str) -> Dict[str, str]:
        """Parses a external_system path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/sources/(?P<source>.+?)/findings/(?P<finding>.+?)/externalSystems/(?P<externalsystem>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def finding_path(
        organization: str,
        source: str,
        finding: str,
    ) -> str:
        """Returns a fully-qualified finding string."""
        return (
            "organizations/{organization}/sources/{source}/findings/{finding}".format(
                organization=organization,
                source=source,
                finding=finding,
            )
        )

    @staticmethod
    def parse_finding_path(path: str) -> Dict[str, str]:
        """Parses a finding path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/sources/(?P<source>.+?)/findings/(?P<finding>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def mute_config_path(
        organization: str,
        mute_config: str,
    ) -> str:
        """Returns a fully-qualified mute_config string."""
        return "organizations/{organization}/muteConfigs/{mute_config}".format(
            organization=organization,
            mute_config=mute_config,
        )

    @staticmethod
    def parse_mute_config_path(path: str) -> Dict[str, str]:
        """Parses a mute_config path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/muteConfigs/(?P<mute_config>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def notification_config_path(
        organization: str,
        location: str,
        notification_config: str,
    ) -> str:
        """Returns a fully-qualified notification_config string."""
        return "organizations/{organization}/locations/{location}/notificationConfigs/{notification_config}".format(
            organization=organization,
            location=location,
            notification_config=notification_config,
        )

    @staticmethod
    def parse_notification_config_path(path: str) -> Dict[str, str]:
        """Parses a notification_config path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/locations/(?P<location>.+?)/notificationConfigs/(?P<notification_config>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def policy_path(
        organization: str,
        constraint_name: str,
    ) -> str:
        """Returns a fully-qualified policy string."""
        return "organizations/{organization}/policies/{constraint_name}".format(
            organization=organization,
            constraint_name=constraint_name,
        )

    @staticmethod
    def parse_policy_path(path: str) -> Dict[str, str]:
        """Parses a policy path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/policies/(?P<constraint_name>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def resource_value_config_path(
        organization: str,
        resource_value_config: str,
    ) -> str:
        """Returns a fully-qualified resource_value_config string."""
        return "organizations/{organization}/resourceValueConfigs/{resource_value_config}".format(
            organization=organization,
            resource_value_config=resource_value_config,
        )

    @staticmethod
    def parse_resource_value_config_path(path: str) -> Dict[str, str]:
        """Parses a resource_value_config path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/resourceValueConfigs/(?P<resource_value_config>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def security_marks_path(
        organization: str,
        asset: str,
    ) -> str:
        """Returns a fully-qualified security_marks string."""
        return "organizations/{organization}/assets/{asset}/securityMarks".format(
            organization=organization,
            asset=asset,
        )

    @staticmethod
    def parse_security_marks_path(path: str) -> Dict[str, str]:
        """Parses a security_marks path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/assets/(?P<asset>.+?)/securityMarks$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def simulation_path(
        organization: str,
        simulation: str,
    ) -> str:
        """Returns a fully-qualified simulation string."""
        return "organizations/{organization}/simulations/{simulation}".format(
            organization=organization,
            simulation=simulation,
        )

    @staticmethod
    def parse_simulation_path(path: str) -> Dict[str, str]:
        """Parses a simulation path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/simulations/(?P<simulation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def source_path(
        organization: str,
        source: str,
    ) -> str:
        """Returns a fully-qualified source string."""
        return "organizations/{organization}/sources/{source}".format(
            organization=organization,
            source=source,
        )

    @staticmethod
    def parse_source_path(path: str) -> Dict[str, str]:
        """Parses a source path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/sources/(?P<source>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def table_data_profile_path(
        project: str,
        table_profile: str,
    ) -> str:
        """Returns a fully-qualified table_data_profile string."""
        return "projects/{project}/tableProfiles/{table_profile}".format(
            project=project,
            table_profile=table_profile,
        )

    @staticmethod
    def parse_table_data_profile_path(path: str) -> Dict[str, str]:
        """Parses a table_data_profile path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/tableProfiles/(?P<table_profile>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def topic_path(
        project: str,
        topic: str,
    ) -> str:
        """Returns a fully-qualified topic string."""
        return "projects/{project}/topics/{topic}".format(
            project=project,
            topic=topic,
        )

    @staticmethod
    def parse_topic_path(path: str) -> Dict[str, str]:
        """Parses a topic path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/topics/(?P<topic>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def valued_resource_path(
        organization: str,
        simulation: str,
        valued_resource: str,
    ) -> str:
        """Returns a fully-qualified valued_resource string."""
        return "organizations/{organization}/simulations/{simulation}/valuedResources/{valued_resource}".format(
            organization=organization,
            simulation=simulation,
            valued_resource=valued_resource,
        )

    @staticmethod
    def parse_valued_resource_path(path: str) -> Dict[str, str]:
        """Parses a valued_resource path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/simulations/(?P<simulation>.+?)/valuedResources/(?P<valued_resource>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Deprecated. Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """

        warnings.warn(
            "get_mtls_endpoint_and_cert_source is deprecated. Use the api_endpoint property instead.",
            DeprecationWarning,
        )
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    @staticmethod
    def _read_environment_variables():
        """Returns the environment variables used by the client.

        Returns:
            Tuple[bool, str, str]: returns the GOOGLE_API_USE_CLIENT_CERTIFICATE,
            GOOGLE_API_USE_MTLS_ENDPOINT, and GOOGLE_CLOUD_UNIVERSE_DOMAIN environment variables.

        Raises:
            ValueError: If GOOGLE_API_USE_CLIENT_CERTIFICATE is not
                any of ["true", "false"].
            google.auth.exceptions.MutualTLSChannelError: If GOOGLE_API_USE_MTLS_ENDPOINT
                is not any of ["auto", "never", "always"].
        """
        use_client_cert = os.getenv(
            "GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"
        ).lower()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )
        return use_client_cert == "true", use_mtls_endpoint, universe_domain_env

    @staticmethod
    def _get_client_cert_source(provided_cert_source, use_cert_flag):
        """Return the client cert source to be used by the client.

        Args:
            provided_cert_source (bytes): The client certificate source provided.
            use_cert_flag (bool): A flag indicating whether to use the client certificate.

        Returns:
            bytes or None: The client cert source to be used by the client.
        """
        client_cert_source = None
        if use_cert_flag:
            if provided_cert_source:
                client_cert_source = provided_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()
        return client_cert_source

    @staticmethod
    def _get_api_endpoint(
        api_override, client_cert_source, universe_domain, use_mtls_endpoint
    ):
        """Return the API endpoint used by the client.

        Args:
            api_override (str): The API endpoint override. If specified, this is always
                the return value of this function and the other arguments are not used.
            client_cert_source (bytes): The client certificate source used by the client.
            universe_domain (str): The universe domain used by the client.
            use_mtls_endpoint (str): How to use the mTLS endpoint, which depends also on the other parameters.
                Possible values are "always", "auto", or "never".

        Returns:
            str: The API endpoint to be used by the client.
        """
        if api_override is not None:
            api_endpoint = api_override
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            _default_universe = SecurityCenterClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = SecurityCenterClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = SecurityCenterClient._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=universe_domain
            )
        return api_endpoint

    @staticmethod
    def _get_universe_domain(
        client_universe_domain: Optional[str], universe_domain_env: Optional[str]
    ) -> str:
        """Return the universe domain used by the client.

        Args:
            client_universe_domain (Optional[str]): The universe domain configured via the client options.
            universe_domain_env (Optional[str]): The universe domain configured via the "GOOGLE_CLOUD_UNIVERSE_DOMAIN" environment variable.

        Returns:
            str: The universe domain to be used by the client.

        Raises:
            ValueError: If the universe domain is an empty string.
        """
        universe_domain = SecurityCenterClient._DEFAULT_UNIVERSE
        if client_universe_domain is not None:
            universe_domain = client_universe_domain
        elif universe_domain_env is not None:
            universe_domain = universe_domain_env
        if len(universe_domain.strip()) == 0:
            raise ValueError("Universe Domain cannot be an empty string.")
        return universe_domain

    def _validate_universe_domain(self):
        """Validates client's and credentials' universe domains are consistent.

        Returns:
            bool: True iff the configured universe domain is valid.

        Raises:
            ValueError: If the configured universe domain is not valid.
        """

        # NOTE (b/349488459): universe validation is disabled until further notice.
        return True

    def _add_cred_info_for_auth_errors(
        self, error: core_exceptions.GoogleAPICallError
    ) -> None:
        """Adds credential info string to error details for 401/403/404 errors.

        Args:
            error (google.api_core.exceptions.GoogleAPICallError): The error to add the cred info.
        """
        if error.code not in [
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.NOT_FOUND,
        ]:
            return

        cred = self._transport._credentials

        # get_cred_info is only available in google-auth>=2.35.0
        if not hasattr(cred, "get_cred_info"):
            return

        # ignore the type check since pypy test fails when get_cred_info
        # is not available
        cred_info = cred.get_cred_info()  # type: ignore
        if cred_info and hasattr(error._details, "append"):
            error._details.append(json.dumps(cred_info))

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used by the client instance.
        """
        return self._universe_domain

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[str, SecurityCenterTransport, Callable[..., SecurityCenterTransport]]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the security center client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,SecurityCenterTransport,Callable[..., SecurityCenterTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the SecurityCenterTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that the ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client_options = client_options
        if isinstance(self._client_options, dict):
            self._client_options = client_options_lib.from_dict(self._client_options)
        if self._client_options is None:
            self._client_options = client_options_lib.ClientOptions()
        self._client_options = cast(
            client_options_lib.ClientOptions, self._client_options
        )

        universe_domain_opt = getattr(self._client_options, "universe_domain", None)

        (
            self._use_client_cert,
            self._use_mtls_endpoint,
            self._universe_domain_env,
        ) = SecurityCenterClient._read_environment_variables()
        self._client_cert_source = SecurityCenterClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = SecurityCenterClient._get_universe_domain(
            universe_domain_opt, self._universe_domain_env
        )
        self._api_endpoint = None  # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        if CLIENT_LOGGING_SUPPORTED:  # pragma: NO COVER
            # Setup logging.
            client_logging.initialize_logging()

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, SecurityCenterTransport)
        if transport_provided:
            # transport is a SecurityCenterTransport instance.
            if credentials or self._client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if self._client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = cast(SecurityCenterTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (
            self._api_endpoint
            or SecurityCenterClient._get_api_endpoint(
                self._client_options.api_endpoint,
                self._client_cert_source,
                self._universe_domain,
                self._use_mtls_endpoint,
            )
        )

        if not transport_provided:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            transport_init: Union[
                Type[SecurityCenterTransport], Callable[..., SecurityCenterTransport]
            ] = (
                SecurityCenterClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., SecurityCenterTransport], transport)
            )
            # initialize with the provided callable or the passed in class
            self._transport = transport_init(
                credentials=credentials,
                credentials_file=self._client_options.credentials_file,
                host=self._api_endpoint,
                scopes=self._client_options.scopes,
                client_cert_source_for_mtls=self._client_cert_source,
                quota_project_id=self._client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=self._client_options.api_audience,
            )

        if "async" not in str(self._transport):
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                std_logging.DEBUG
            ):  # pragma: NO COVER
                _LOGGER.debug(
                    "Created client `google.cloud.securitycenter_v2.SecurityCenterClient`.",
                    extra={
                        "serviceName": "google.cloud.securitycenter.v2.SecurityCenter",
                        "universeDomain": getattr(
                            self._transport._credentials, "universe_domain", ""
                        ),
                        "credentialsType": f"{type(self._transport._credentials).__module__}.{type(self._transport._credentials).__qualname__}",
                        "credentialsInfo": getattr(
                            self.transport._credentials, "get_cred_info", lambda: None
                        )(),
                    }
                    if hasattr(self._transport, "_credentials")
                    else {
                        "serviceName": "google.cloud.securitycenter.v2.SecurityCenter",
                        "credentialsType": None,
                    },
                )

    def batch_create_resource_value_configs(
        self,
        request: Optional[
            Union[securitycenter_service.BatchCreateResourceValueConfigsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        requests: Optional[
            MutableSequence[securitycenter_service.CreateResourceValueConfigRequest]
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> securitycenter_service.BatchCreateResourceValueConfigsResponse:
        r"""Creates a ResourceValueConfig for an organization.
        Maps user's tags to difference resource values for use
        by the attack path simulation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_batch_create_resource_value_configs():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                requests = securitycenter_v2.CreateResourceValueConfigRequest()
                requests.parent = "parent_value"

                request = securitycenter_v2.BatchCreateResourceValueConfigsRequest(
                    parent="parent_value",
                    requests=requests,
                )

                # Make the request
                response = client.batch_create_resource_value_configs(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.BatchCreateResourceValueConfigsRequest, dict]):
                The request object. Request message to create multiple
                resource value configs
            parent (str):
                Required. Resource name of the new
                ResourceValueConfig's parent. The parent
                field in the
                CreateResourceValueConfigRequest
                messages must either be empty or match
                this field.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            requests (MutableSequence[google.cloud.securitycenter_v2.types.CreateResourceValueConfigRequest]):
                Required. The resource value configs
                to be created.

                This corresponds to the ``requests`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.BatchCreateResourceValueConfigsResponse:
                Response message for
                BatchCreateResourceValueConfigs

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, requests]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, securitycenter_service.BatchCreateResourceValueConfigsRequest
        ):
            request = securitycenter_service.BatchCreateResourceValueConfigsRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if requests is not None:
                request.requests = requests

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.batch_create_resource_value_configs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def bulk_mute_findings(
        self,
        request: Optional[
            Union[securitycenter_service.BulkMuteFindingsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Kicks off an LRO to bulk mute findings for a parent
        based on a filter. If no location is specified, findings
        are muted in global. The parent can be either an
        organization, folder, or project. The findings matched
        by the filter will be muted after the LRO is done.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_bulk_mute_findings():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.BulkMuteFindingsRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.bulk_mute_findings(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.BulkMuteFindingsRequest, dict]):
                The request object. Request message for bulk findings
                update.
                Note:

                1. If multiple bulk update requests
                    match the same resource, the order
                    in which they get executed is not
                    defined.
                2. Once a bulk operation is started,
                    there is no way to stop it.
            parent (str):
                Required. The parent, at which bulk action needs to be
                applied. If no location is specified, findings are
                updated in global. The following list shows some
                examples:

                -  ``organizations/[organization_id]``
                -  ``organizations/[organization_id]/locations/[location_id]``
                -  ``folders/[folder_id]``
                -  ``folders/[folder_id]/locations/[location_id]``
                -  ``projects/[project_id]``
                -  ``projects/[project_id]/locations/[location_id]``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.securitycenter_v2.types.BulkMuteFindingsResponse`
                The response to a BulkMute request. Contains the LRO
                information.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.BulkMuteFindingsRequest):
            request = securitycenter_service.BulkMuteFindingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.bulk_mute_findings]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            securitycenter_service.BulkMuteFindingsResponse,
            metadata_type=empty_pb2.Empty,
        )

        # Done; return the response.
        return response

    def create_big_query_export(
        self,
        request: Optional[
            Union[securitycenter_service.CreateBigQueryExportRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        big_query_export: Optional[bigquery_export.BigQueryExport] = None,
        big_query_export_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> bigquery_export.BigQueryExport:
        r"""Creates a BigQuery export.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_create_big_query_export():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.CreateBigQueryExportRequest(
                    parent="parent_value",
                    big_query_export_id="big_query_export_id_value",
                )

                # Make the request
                response = client.create_big_query_export(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.CreateBigQueryExportRequest, dict]):
                The request object. Request message for creating a
                BigQuery export.
            parent (str):
                Required. The name of the parent resource of the new
                BigQuery export. Its format is
                ``organizations/[organization_id]/locations/[location_id]``,
                ``folders/[folder_id]/locations/[location_id]``, or
                ``projects/[project_id]/locations/[location_id]``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            big_query_export (google.cloud.securitycenter_v2.types.BigQueryExport):
                Required. The BigQuery export being
                created.

                This corresponds to the ``big_query_export`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            big_query_export_id (str):
                Required. Unique identifier provided
                by the client within the parent scope.
                It must consist of only lowercase
                letters, numbers, and hyphens, must
                start with a letter, must end with
                either a letter or a number, and must be
                63 characters or less.

                This corresponds to the ``big_query_export_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.BigQueryExport:
                Configures how to deliver Findings to
                BigQuery Instance.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, big_query_export, big_query_export_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.CreateBigQueryExportRequest):
            request = securitycenter_service.CreateBigQueryExportRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if big_query_export is not None:
                request.big_query_export = big_query_export
            if big_query_export_id is not None:
                request.big_query_export_id = big_query_export_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_big_query_export]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_finding(
        self,
        request: Optional[
            Union[securitycenter_service.CreateFindingRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        finding: Optional[gcs_finding.Finding] = None,
        finding_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcs_finding.Finding:
        r"""Creates a finding in a location. The corresponding
        source must exist for finding creation to succeed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_create_finding():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.CreateFindingRequest(
                    parent="parent_value",
                    finding_id="finding_id_value",
                )

                # Make the request
                response = client.create_finding(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.CreateFindingRequest, dict]):
                The request object. Request message for creating a
                finding.
            parent (str):
                Required. Resource name of the new finding's parent. The
                following list shows some examples of the format: +
                ``organizations/[organization_id]/sources/[source_id]``
                +
                ``organizations/[organization_id]/sources/[source_id]/locations/[location_id]``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            finding (google.cloud.securitycenter_v2.types.Finding):
                Required. The Finding being created. The name and
                security_marks will be ignored as they are both output
                only fields on this resource.

                This corresponds to the ``finding`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            finding_id (str):
                Required. Unique identifier provided
                by the client within the parent scope.
                It must be alphanumeric and less than or
                equal to 32 characters and greater than
                0 characters in length.

                This corresponds to the ``finding_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.Finding:
                Security Command Center finding.

                A finding is a record of assessment data
                like security, risk, health, or privacy,
                that is ingested into Security Command
                Center for presentation, notification,
                analysis, policy testing, and
                enforcement. For example, a cross-site
                scripting (XSS) vulnerability in an App
                Engine application is a finding.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, finding, finding_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.CreateFindingRequest):
            request = securitycenter_service.CreateFindingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if finding is not None:
                request.finding = finding
            if finding_id is not None:
                request.finding_id = finding_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_finding]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_mute_config(
        self,
        request: Optional[
            Union[securitycenter_service.CreateMuteConfigRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        mute_config: Optional[gcs_mute_config.MuteConfig] = None,
        mute_config_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcs_mute_config.MuteConfig:
        r"""Creates a mute config.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_create_mute_config():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                mute_config = securitycenter_v2.MuteConfig()
                mute_config.filter = "filter_value"
                mute_config.type_ = "DYNAMIC"

                request = securitycenter_v2.CreateMuteConfigRequest(
                    parent="parent_value",
                    mute_config=mute_config,
                    mute_config_id="mute_config_id_value",
                )

                # Make the request
                response = client.create_mute_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.CreateMuteConfigRequest, dict]):
                The request object. Request message for creating a mute
                config.
            parent (str):
                Required. Resource name of the new mute configs's
                parent. Its format is
                ``organizations/[organization_id]/locations/[location_id]``,
                ``folders/[folder_id]/locations/[location_id]``, or
                ``projects/[project_id]/locations/[location_id]``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mute_config (google.cloud.securitycenter_v2.types.MuteConfig):
                Required. The mute config being
                created.

                This corresponds to the ``mute_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mute_config_id (str):
                Required. Unique identifier provided
                by the client within the parent scope.
                It must consist of only lowercase
                letters, numbers, and hyphens, must
                start with a letter, must end with
                either a letter or a number, and must be
                63 characters or less.

                This corresponds to the ``mute_config_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.MuteConfig:
                A mute config is a Cloud SCC resource
                that contains the configuration to mute
                create/update events of findings.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, mute_config, mute_config_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.CreateMuteConfigRequest):
            request = securitycenter_service.CreateMuteConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if mute_config is not None:
                request.mute_config = mute_config
            if mute_config_id is not None:
                request.mute_config_id = mute_config_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_mute_config]

        header_params = {}

        routing_param_regex = re.compile(
            "^projects/[^/]+/locations/(?P<location>[^/]+)$"
        )
        regex_match = routing_param_regex.match(request.parent)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        routing_param_regex = re.compile(
            "^organizations/[^/]+/locations/(?P<location>[^/]+)$"
        )
        regex_match = routing_param_regex.match(request.parent)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        routing_param_regex = re.compile(
            "^folders/[^/]+/locations/(?P<location>[^/]+)$"
        )
        regex_match = routing_param_regex.match(request.parent)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_notification_config(
        self,
        request: Optional[
            Union[securitycenter_service.CreateNotificationConfigRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        notification_config: Optional[
            gcs_notification_config.NotificationConfig
        ] = None,
        config_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcs_notification_config.NotificationConfig:
        r"""Creates a notification config.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_create_notification_config():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.CreateNotificationConfigRequest(
                    parent="parent_value",
                    config_id="config_id_value",
                )

                # Make the request
                response = client.create_notification_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.CreateNotificationConfigRequest, dict]):
                The request object. Request message for creating a
                notification config.
            parent (str):
                Required. Resource name of the new notification config's
                parent. Its format is
                ``organizations/[organization_id]/locations/[location_id]``,
                ``folders/[folder_id]/locations/[location_id]``, or
                ``projects/[project_id]/locations/[location_id]``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            notification_config (google.cloud.securitycenter_v2.types.NotificationConfig):
                Required. The notification config
                being created. The name and the service
                account will be ignored as they are both
                output only fields on this resource.

                This corresponds to the ``notification_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config_id (str):
                Required.
                Unique identifier provided by the client
                within the parent scope. It must be
                between 1 and 128 characters and contain
                alphanumeric characters, underscores, or
                hyphens only.

                This corresponds to the ``config_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.NotificationConfig:
                Cloud Security Command Center (Cloud
                SCC) notification configs.
                A notification config is a Cloud SCC
                resource that contains the configuration
                to send notifications for create/update
                events of findings, assets and etc.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, notification_config, config_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, securitycenter_service.CreateNotificationConfigRequest
        ):
            request = securitycenter_service.CreateNotificationConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if notification_config is not None:
                request.notification_config = notification_config
            if config_id is not None:
                request.config_id = config_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_notification_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_source(
        self,
        request: Optional[
            Union[securitycenter_service.CreateSourceRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        source: Optional[gcs_source.Source] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcs_source.Source:
        r"""Creates a source.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_create_source():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.CreateSourceRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_source(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.CreateSourceRequest, dict]):
                The request object. Request message for creating a
                source.
            parent (str):
                Required. Resource name of the new source's parent. Its
                format should be ``organizations/[organization_id]``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source (google.cloud.securitycenter_v2.types.Source):
                Required. The Source being created, only the
                display_name and description will be used. All other
                fields will be ignored.

                This corresponds to the ``source`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.Source:
                Security Command Center finding
                source. A finding source is an entity or
                a mechanism that can produce a finding.
                A source is like a container of findings
                that come from the same scanner, logger,
                monitor, and other tools.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, source]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.CreateSourceRequest):
            request = securitycenter_service.CreateSourceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if source is not None:
                request.source = source

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_source]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_big_query_export(
        self,
        request: Optional[
            Union[securitycenter_service.DeleteBigQueryExportRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes an existing BigQuery export.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_delete_big_query_export():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.DeleteBigQueryExportRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_big_query_export(request=request)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.DeleteBigQueryExportRequest, dict]):
                The request object. Request message for deleting a
                BigQuery export.
            name (str):
                Required. The name of the BigQuery export to delete. The
                following list shows some examples of the format:

                -

                ``organizations/{organization}/locations/{location}/bigQueryExports/{export_id}``

                -  ``folders/{folder}/locations/{location}/bigQueryExports/{export_id}``
                -  ``projects/{project}/locations/{location}/bigQueryExports/{export_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.DeleteBigQueryExportRequest):
            request = securitycenter_service.DeleteBigQueryExportRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_big_query_export]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def delete_mute_config(
        self,
        request: Optional[
            Union[securitycenter_service.DeleteMuteConfigRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes an existing mute config. If no location is
        specified, default is global.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_delete_mute_config():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.DeleteMuteConfigRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_mute_config(request=request)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.DeleteMuteConfigRequest, dict]):
                The request object. Request message for deleting a mute
                config. If no location is specified,
                default is global.
            name (str):
                Required. Name of the mute config to delete. The
                following list shows some examples of the format:

                -  ``organizations/{organization}/muteConfigs/{config_id}``
                -

                ``organizations/{organization}/locations/{location}/muteConfigs/{config_id}``

                -  ``folders/{folder}/muteConfigs/{config_id}``
                -  ``folders/{folder}/locations/{location}/muteConfigs/{config_id}``
                -  ``projects/{project}/muteConfigs/{config_id}``
                -  ``projects/{project}/locations/{location}/muteConfigs/{config_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.DeleteMuteConfigRequest):
            request = securitycenter_service.DeleteMuteConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_mute_config]

        header_params = {}

        routing_param_regex = re.compile(
            "^projects/[^/]+/locations/(?P<location>[^/]+)/muteConfigs/[^/]+$"
        )
        regex_match = routing_param_regex.match(request.name)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        routing_param_regex = re.compile(
            "^organizations/[^/]+/locations/(?P<location>[^/]+)/muteConfigs/[^/]+$"
        )
        regex_match = routing_param_regex.match(request.name)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        routing_param_regex = re.compile(
            "^folders/[^/]+/locations/(?P<location>[^/]+)/muteConfigs/[^/]+$"
        )
        regex_match = routing_param_regex.match(request.name)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def delete_notification_config(
        self,
        request: Optional[
            Union[securitycenter_service.DeleteNotificationConfigRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes a notification config.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_delete_notification_config():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.DeleteNotificationConfigRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_notification_config(request=request)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.DeleteNotificationConfigRequest, dict]):
                The request object. Request message for deleting a
                notification config.
            name (str):
                Required. Name of the notification config to delete. The
                following list shows some examples of the format:

                -

                ``organizations/[organization_id]/locations/[location_id]/notificationConfigs/[config_id]``
                +
                ``folders/[folder_id]/locations/[location_id]notificationConfigs/[config_id]``
                +
                ``projects/[project_id]/locations/[location_id]notificationConfigs/[config_id]``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, securitycenter_service.DeleteNotificationConfigRequest
        ):
            request = securitycenter_service.DeleteNotificationConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_notification_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def delete_resource_value_config(
        self,
        request: Optional[
            Union[securitycenter_service.DeleteResourceValueConfigRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes a ResourceValueConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_delete_resource_value_config():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.DeleteResourceValueConfigRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_resource_value_config(request=request)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.DeleteResourceValueConfigRequest, dict]):
                The request object. Request message to delete resource
                value config
            name (str):
                Required. Name of the
                ResourceValueConfig to delete

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, securitycenter_service.DeleteResourceValueConfigRequest
        ):
            request = securitycenter_service.DeleteResourceValueConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_resource_value_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_big_query_export(
        self,
        request: Optional[
            Union[securitycenter_service.GetBigQueryExportRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> bigquery_export.BigQueryExport:
        r"""Gets a BigQuery export.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_get_big_query_export():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.GetBigQueryExportRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_big_query_export(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.GetBigQueryExportRequest, dict]):
                The request object. Request message for retrieving a
                BigQuery export.
            name (str):
                Required. Name of the BigQuery export to retrieve. The
                following list shows some examples of the format:

                -

                ``organizations/{organization}/locations/{location}/bigQueryExports/{export_id}``

                -  ``folders/{folder}/locations/{location}/bigQueryExports/{export_id}``
                -  ``projects/{project}locations/{location}//bigQueryExports/{export_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.BigQueryExport:
                Configures how to deliver Findings to
                BigQuery Instance.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.GetBigQueryExportRequest):
            request = securitycenter_service.GetBigQueryExportRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_big_query_export]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_simulation(
        self,
        request: Optional[
            Union[securitycenter_service.GetSimulationRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> simulation.Simulation:
        r"""Get the simulation by name or the latest simulation
        for the given organization.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_get_simulation():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.GetSimulationRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_simulation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.GetSimulationRequest, dict]):
                The request object. Request message for getting
                simulation. Simulation name can include
                "latest" to retrieve the latest
                simulation For example,
                "organizations/123/simulations/latest".
            name (str):
                Required. The organization name or simulation name of
                this simulation

                Valid format:
                ``organizations/{organization}/simulations/latest``
                ``organizations/{organization}/simulations/{simulation}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.Simulation:
                Attack path simulation
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.GetSimulationRequest):
            request = securitycenter_service.GetSimulationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_simulation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_valued_resource(
        self,
        request: Optional[
            Union[securitycenter_service.GetValuedResourceRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> valued_resource.ValuedResource:
        r"""Get the valued resource by name

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_get_valued_resource():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.GetValuedResourceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_valued_resource(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.GetValuedResourceRequest, dict]):
                The request object. Request message for getting a valued
                resource.
            name (str):
                Required. The name of this valued resource

                Valid format:
                ``organizations/{organization}/simulations/{simulation}/valuedResources/{valued_resource}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.ValuedResource:
                A resource that is determined to have
                value to a user's system

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.GetValuedResourceRequest):
            request = securitycenter_service.GetValuedResourceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_valued_resource]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.GetIamPolicyRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the access control policy on the specified
        Source.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_get_iam_policy():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.GetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.get_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]):
                The request object. Request message for ``GetIamPolicy`` method.
            resource (str):
                REQUIRED: The resource for which the
                policy is being requested. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                   :literal:`\`     {       "bindings": [         {           "role": "roles/resourcemanager.organizationAdmin",           "members": [             "user:mike@example.com",             "group:admins@example.com",             "domain:google.com",             "serviceAccount:my-project-id@appspot.gserviceaccount.com"           ]         },         {           "role": "roles/resourcemanager.organizationViewer",           "members": [             "user:eve@example.com"           ],           "condition": {             "title": "expirable access",             "description": "Does not grant access after Sep 2020",             "expression": "request.time <             timestamp('2020-10-01T00:00:00.000Z')",           }         }       ],       "etag": "BwWWja0YfJA=",       "version": 3     }`\ \`

                   **YAML example:**

                   :literal:`\`     bindings:     - members:       - user:mike@example.com       - group:admins@example.com       - domain:google.com       - serviceAccount:my-project-id@appspot.gserviceaccount.com       role: roles/resourcemanager.organizationAdmin     - members:       - user:eve@example.com       role: roles/resourcemanager.organizationViewer       condition:         title: expirable access         description: Does not grant access after Sep 2020         expression: request.time < timestamp('2020-10-01T00:00:00.000Z')     etag: BwWWja0YfJA=     version: 3`\ \`

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [resource]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # - The request isn't a proto-plus wrapped type,
            #   so it must be constructed via keyword expansion.
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.GetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_mute_config(
        self,
        request: Optional[
            Union[securitycenter_service.GetMuteConfigRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> mute_config.MuteConfig:
        r"""Gets a mute config. If no location is specified,
        default is global.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_get_mute_config():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.GetMuteConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_mute_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.GetMuteConfigRequest, dict]):
                The request object. Request message for retrieving a mute
                config. If no location is specified,
                default is global.
            name (str):
                Required. Name of the mute config to retrieve. The
                following list shows some examples of the format:

                -  ``organizations/{organization}/muteConfigs/{config_id}``
                -

                ``organizations/{organization}/locations/{location}/muteConfigs/{config_id}``

                -  ``folders/{folder}/muteConfigs/{config_id}``
                -  ``folders/{folder}/locations/{location}/muteConfigs/{config_id}``
                -  ``projects/{project}/muteConfigs/{config_id}``
                -  ``projects/{project}/locations/{location}/muteConfigs/{config_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.MuteConfig:
                A mute config is a Cloud SCC resource
                that contains the configuration to mute
                create/update events of findings.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.GetMuteConfigRequest):
            request = securitycenter_service.GetMuteConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_mute_config]

        header_params = {}

        routing_param_regex = re.compile(
            "^projects/[^/]+/locations/(?P<location>[^/]+)/muteConfigs/[^/]+$"
        )
        regex_match = routing_param_regex.match(request.name)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        routing_param_regex = re.compile(
            "^organizations/[^/]+/locations/(?P<location>[^/]+)/muteConfigs/[^/]+$"
        )
        regex_match = routing_param_regex.match(request.name)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        routing_param_regex = re.compile(
            "^folders/[^/]+/locations/(?P<location>[^/]+)/muteConfigs/[^/]+$"
        )
        regex_match = routing_param_regex.match(request.name)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_notification_config(
        self,
        request: Optional[
            Union[securitycenter_service.GetNotificationConfigRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> notification_config.NotificationConfig:
        r"""Gets a notification config.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_get_notification_config():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.GetNotificationConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_notification_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.GetNotificationConfigRequest, dict]):
                The request object. Request message for getting a
                notification config.
            name (str):
                Required. Name of the notification config to get. The
                following list shows some examples of the format:

                -

                ``organizations/[organization_id]/locations/[location_id]/notificationConfigs/[config_id]``
                +
                ``folders/[folder_id]/locations/[location_id]/notificationConfigs/[config_id]``
                +
                ``projects/[project_id]/locations/[location_id]/notificationConfigs/[config_id]``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.NotificationConfig:
                Cloud Security Command Center (Cloud
                SCC) notification configs.
                A notification config is a Cloud SCC
                resource that contains the configuration
                to send notifications for create/update
                events of findings, assets and etc.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.GetNotificationConfigRequest):
            request = securitycenter_service.GetNotificationConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_notification_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_resource_value_config(
        self,
        request: Optional[
            Union[securitycenter_service.GetResourceValueConfigRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> resource_value_config.ResourceValueConfig:
        r"""Gets a ResourceValueConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_get_resource_value_config():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.GetResourceValueConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_resource_value_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.GetResourceValueConfigRequest, dict]):
                The request object. Request message to get resource value
                config
            name (str):
                Required. Name of the resource value config to retrieve.
                Its format is
                organizations/{organization}/resourceValueConfigs/{config_id}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.ResourceValueConfig:
                A resource value configuration (RVC)
                is a mapping configuration of user's
                resources to resource values. Used in
                Attack path simulations.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, securitycenter_service.GetResourceValueConfigRequest
        ):
            request = securitycenter_service.GetResourceValueConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_resource_value_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_source(
        self,
        request: Optional[Union[securitycenter_service.GetSourceRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> source.Source:
        r"""Gets a source.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_get_source():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.GetSourceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_source(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.GetSourceRequest, dict]):
                The request object. Request message for getting a source.
            name (str):
                Required. Relative resource name of the source. Its
                format is
                ``organizations/[organization_id]/source/[source_id]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.Source:
                Security Command Center finding
                source. A finding source is an entity or
                a mechanism that can produce a finding.
                A source is like a container of findings
                that come from the same scanner, logger,
                monitor, and other tools.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.GetSourceRequest):
            request = securitycenter_service.GetSourceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_source]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def group_findings(
        self,
        request: Optional[
            Union[securitycenter_service.GroupFindingsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        group_by: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.GroupFindingsPager:
        r"""Filters an organization or source's findings and groups them by
        their specified properties in a location. If no location is
        specified, findings are assumed to be in global

        To group across all sources provide a ``-`` as the source id.
        The following list shows some examples:

        -  ``/v2/organizations/{organization_id}/sources/-/findings``
        -

        ``/v2/organizations/{organization_id}/sources/-/locations/{location_id}/findings``

        -  ``/v2/folders/{folder_id}/sources/-/findings``
        -  ``/v2/folders/{folder_id}/sources/-/locations/{location_id}/findings``
        -  ``/v2/projects/{project_id}/sources/-/findings``
        -  ``/v2/projects/{project_id}/sources/-/locations/{location_id}/findings``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_group_findings():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.GroupFindingsRequest(
                    parent="parent_value",
                    group_by="group_by_value",
                )

                # Make the request
                page_result = client.group_findings(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.GroupFindingsRequest, dict]):
                The request object. Request message for grouping by
                findings.
            parent (str):
                Required. Name of the source to groupBy. If no location
                is specified, finding is assumed to be in global. The
                following list shows some examples:

                -  ``organizations/[organization_id]/sources/[source_id]``
                -

                ``organizations/[organization_id]/sources/[source_id]/locations/[location_id]``

                -  ``folders/[folder_id]/sources/[source_id]``
                -  ``folders/[folder_id]/sources/[source_id]/locations/[location_id]``
                -  ``projects/[project_id]/sources/[source_id]``
                -  ``projects/[project_id]/sources/[source_id]/locations/[location_id]``

                To groupBy across all sources provide a source_id of
                ``-``. The following list shows some examples:

                -  ``organizations/{organization_id}/sources/-``
                -  ``organizations/{organization_id}/sources/-/locations/[location_id]``
                -  ``folders/{folder_id}/sources/-``
                -  ``folders/{folder_id}/sources/-/locations/[location_id]``
                -  ``projects/{project_id}/sources/-``
                -  ``projects/{project_id}/sources/-/locations/[location_id]``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            group_by (str):
                Required. Expression that defines what assets fields to
                use for grouping. The string value should follow SQL
                syntax: comma separated list of fields. For example:
                "parent,resource_name".

                This corresponds to the ``group_by`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.services.security_center.pagers.GroupFindingsPager:
                Response message for group by
                findings.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, group_by]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.GroupFindingsRequest):
            request = securitycenter_service.GroupFindingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if group_by is not None:
                request.group_by = group_by

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.group_findings]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.GroupFindingsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_attack_paths(
        self,
        request: Optional[
            Union[securitycenter_service.ListAttackPathsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListAttackPathsPager:
        r"""Lists the attack paths for a set of simulation
        results or valued resources and filter.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_list_attack_paths():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.ListAttackPathsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_attack_paths(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.ListAttackPathsRequest, dict]):
                The request object. Request message for listing the
                attack paths for a given simulation or
                valued resource.
            parent (str):
                Required. Name of parent to list attack paths.

                Valid formats: ``organizations/{organization}``,
                ``organizations/{organization}/simulations/{simulation}``
                ``organizations/{organization}/simulations/{simulation}/attackExposureResults/{attack_exposure_result_v2}``
                ``organizations/{organization}/simulations/{simulation}/valuedResources/{valued_resource}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.services.security_center.pagers.ListAttackPathsPager:
                Response message for listing the
                attack paths for a given simulation or
                valued resource.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.ListAttackPathsRequest):
            request = securitycenter_service.ListAttackPathsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_attack_paths]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAttackPathsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_big_query_exports(
        self,
        request: Optional[
            Union[securitycenter_service.ListBigQueryExportsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListBigQueryExportsPager:
        r"""Lists BigQuery exports. Note that when requesting
        BigQuery exports at a given level all exports under that
        level are also returned e.g. if requesting BigQuery
        exports under a folder, then all BigQuery exports
        immediately under the folder plus the ones created under
        the projects within the folder are returned.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_list_big_query_exports():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.ListBigQueryExportsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_big_query_exports(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.ListBigQueryExportsRequest, dict]):
                The request object. Request message for listing BigQuery
                exports at a given scope e.g.
                organization, folder or project.
            parent (str):
                Required. The parent, which owns the collection of
                BigQuery exports. Its format is
                ``organizations/[organization_id]/locations/[location_id]``,
                ``folders/[folder_id]/locations/[location_id]``, or
                ``projects/[project_id]/locations/[location_id]``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.services.security_center.pagers.ListBigQueryExportsPager:
                Response message for listing BigQuery
                exports.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.ListBigQueryExportsRequest):
            request = securitycenter_service.ListBigQueryExportsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_big_query_exports]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListBigQueryExportsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_findings(
        self,
        request: Optional[
            Union[securitycenter_service.ListFindingsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListFindingsPager:
        r"""Lists an organization or source's findings.

        To list across all sources for a given location provide a ``-``
        as the source id. If no location is specified, finding are
        assumed to be in global. The following list shows some examples:

        -  ``/v2/organizations/{organization_id}/sources/-/findings``
        -

        ``/v2/organizations/{organization_id}/sources/-/locations/{location_id}/findings``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_list_findings():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.ListFindingsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_findings(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.ListFindingsRequest, dict]):
                The request object. Request message for listing findings.
            parent (str):
                Required. Name of the source the findings belong to. If
                no location is specified, the default is global. The
                following list shows some examples:

                -  ``organizations/[organization_id]/sources/[source_id]``
                -

                ``organizations/[organization_id]/sources/[source_id]/locations/[location_id]``

                -  ``folders/[folder_id]/sources/[source_id]``
                -  ``folders/[folder_id]/sources/[source_id]/locations/[location_id]``
                -  ``projects/[project_id]/sources/[source_id]``
                -  ``projects/[project_id]/sources/[source_id]/locations/[location_id]``

                To list across all sources provide a source_id of ``-``.
                The following list shows some examples:

                -  ``organizations/{organization_id}/sources/-``
                -  ``organizations/{organization_id}/sources/-/locations/{location_id}``
                -  ``folders/{folder_id}/sources/-``
                -  ``folders/{folder_id}/sources/-locations/{location_id}``
                -  ``projects/{projects_id}/sources/-``
                -  ``projects/{projects_id}/sources/-/locations/{location_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.services.security_center.pagers.ListFindingsPager:
                Response message for listing
                findings.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.ListFindingsRequest):
            request = securitycenter_service.ListFindingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_findings]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListFindingsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_mute_configs(
        self,
        request: Optional[
            Union[securitycenter_service.ListMuteConfigsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListMuteConfigsPager:
        r"""Lists mute configs. If no location is specified,
        default is global.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_list_mute_configs():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.ListMuteConfigsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_mute_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.ListMuteConfigsRequest, dict]):
                The request object. Request message for listing  mute
                configs at a given scope e.g.
                organization, folder or project. If no
                location is specified, default is
                global.
            parent (str):
                Required. The parent, which owns the collection of mute
                configs. Its format is
                ``organizations/[organization_id]", "folders/[folder_id]``,
                ``projects/[project_id]``,
                ``organizations/[organization_id]/locations/[location_id]``,
                ``folders/[folder_id]/locations/[location_id]``,
                ``projects/[project_id]/locations/[location_id]``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.services.security_center.pagers.ListMuteConfigsPager:
                Response message for listing mute
                configs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.ListMuteConfigsRequest):
            request = securitycenter_service.ListMuteConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_mute_configs]

        header_params = {}

        routing_param_regex = re.compile(
            "^projects/[^/]+/locations/(?P<location>[^/]+)/muteConfigs$"
        )
        regex_match = routing_param_regex.match(request.parent)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        routing_param_regex = re.compile(
            "^organizations/[^/]+/locations/(?P<location>[^/]+)/muteConfigs$"
        )
        regex_match = routing_param_regex.match(request.parent)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        routing_param_regex = re.compile(
            "^folders/[^/]+/locations/(?P<location>[^/]+)/muteConfigs$"
        )
        regex_match = routing_param_regex.match(request.parent)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListMuteConfigsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_notification_configs(
        self,
        request: Optional[
            Union[securitycenter_service.ListNotificationConfigsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListNotificationConfigsPager:
        r"""Lists notification configs.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_list_notification_configs():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.ListNotificationConfigsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_notification_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.ListNotificationConfigsRequest, dict]):
                The request object. Request message for listing
                notification configs.
            parent (str):
                Required. The name of the parent in which to list the
                notification configurations. Its format is
                "organizations/[organization_id]/locations/[location_id]",
                "folders/[folder_id]/locations/[location_id]", or
                "projects/[project_id]/locations/[location_id]".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.services.security_center.pagers.ListNotificationConfigsPager:
                Response message for listing
                notification configs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, securitycenter_service.ListNotificationConfigsRequest
        ):
            request = securitycenter_service.ListNotificationConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_notification_configs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListNotificationConfigsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_resource_value_configs(
        self,
        request: Optional[
            Union[securitycenter_service.ListResourceValueConfigsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListResourceValueConfigsPager:
        r"""Lists all ResourceValueConfigs.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_list_resource_value_configs():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.ListResourceValueConfigsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_resource_value_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.ListResourceValueConfigsRequest, dict]):
                The request object. Request message to list resource
                value configs of a parent
            parent (str):
                Required. The parent, which owns the collection of
                resource value configs. Its format is
                ``organizations/[organization_id]``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.services.security_center.pagers.ListResourceValueConfigsPager:
                Response message to list resource
                value configs
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, securitycenter_service.ListResourceValueConfigsRequest
        ):
            request = securitycenter_service.ListResourceValueConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_resource_value_configs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListResourceValueConfigsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_sources(
        self,
        request: Optional[
            Union[securitycenter_service.ListSourcesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListSourcesPager:
        r"""Lists all sources belonging to an organization.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_list_sources():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.ListSourcesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_sources(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.ListSourcesRequest, dict]):
                The request object. Request message for listing sources.
            parent (str):
                Required. Resource name of the parent of sources to
                list. Its format should be
                ``organizations/[organization_id]``,
                ``folders/[folder_id]``, or ``projects/[project_id]``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.services.security_center.pagers.ListSourcesPager:
                Response message for listing sources.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.ListSourcesRequest):
            request = securitycenter_service.ListSourcesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_sources]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSourcesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_valued_resources(
        self,
        request: Optional[
            Union[securitycenter_service.ListValuedResourcesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListValuedResourcesPager:
        r"""Lists the valued resources for a set of simulation
        results and filter.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_list_valued_resources():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.ListValuedResourcesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_valued_resources(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.ListValuedResourcesRequest, dict]):
                The request object. Request message for listing the
                valued resources for a given simulation.
            parent (str):
                Required. Name of parent to list exposed resources.

                Valid formats: ``organizations/{organization}``,
                ``organizations/{organization}/simulations/{simulation}``
                ``organizations/{organization}/simulations/{simulation}/attackExposureResults/{attack_exposure_result_v2}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.services.security_center.pagers.ListValuedResourcesPager:
                Response message for listing the
                valued resources for a given simulation.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.ListValuedResourcesRequest):
            request = securitycenter_service.ListValuedResourcesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_valued_resources]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListValuedResourcesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_finding_state(
        self,
        request: Optional[
            Union[securitycenter_service.SetFindingStateRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        state: Optional[finding.Finding.State] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> finding.Finding:
        r"""Updates the state of a finding. If no location is
        specified, finding is assumed to be in global

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_set_finding_state():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.SetFindingStateRequest(
                    name="name_value",
                    state="INACTIVE",
                )

                # Make the request
                response = client.set_finding_state(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.SetFindingStateRequest, dict]):
                The request object. Request message for updating a
                finding's state.
            name (str):
                Required. The `relative resource
                name <https://cloud.google.com/apis/design/resource_names#relative_resource_name>`__
                of the finding. If no location is specified, finding is
                assumed to be in global. The following list shows some
                examples:

                -

                ``organizations/{organization_id}/sources/{source_id}/findings/{finding_id}``
                +
                ``organizations/{organization_id}/sources/{source_id}/locations/{location_id}/findings/{finding_id}``

                -  ``folders/{folder_id}/sources/{source_id}/findings/{finding_id}``
                -

                ``folders/{folder_id}/sources/{source_id}/locations/{location_id}/findings/{finding_id}``

                -  ``projects/{project_id}/sources/{source_id}/findings/{finding_id}``
                -

                ``projects/{project_id}/sources/{source_id}/locations/{location_id}/findings/{finding_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            state (google.cloud.securitycenter_v2.types.Finding.State):
                Required. The desired State of the
                finding.

                This corresponds to the ``state`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.Finding:
                Security Command Center finding.

                A finding is a record of assessment data
                like security, risk, health, or privacy,
                that is ingested into Security Command
                Center for presentation, notification,
                analysis, policy testing, and
                enforcement. For example, a cross-site
                scripting (XSS) vulnerability in an App
                Engine application is a finding.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name, state]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.SetFindingStateRequest):
            request = securitycenter_service.SetFindingStateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if state is not None:
                request.state = state

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_finding_state]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.SetIamPolicyRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the access control policy on the specified
        Source.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_set_iam_policy():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.SetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.set_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]):
                The request object. Request message for ``SetIamPolicy`` method.
            resource (str):
                REQUIRED: The resource for which the
                policy is being specified. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                   :literal:`\`     {       "bindings": [         {           "role": "roles/resourcemanager.organizationAdmin",           "members": [             "user:mike@example.com",             "group:admins@example.com",             "domain:google.com",             "serviceAccount:my-project-id@appspot.gserviceaccount.com"           ]         },         {           "role": "roles/resourcemanager.organizationViewer",           "members": [             "user:eve@example.com"           ],           "condition": {             "title": "expirable access",             "description": "Does not grant access after Sep 2020",             "expression": "request.time <             timestamp('2020-10-01T00:00:00.000Z')",           }         }       ],       "etag": "BwWWja0YfJA=",       "version": 3     }`\ \`

                   **YAML example:**

                   :literal:`\`     bindings:     - members:       - user:mike@example.com       - group:admins@example.com       - domain:google.com       - serviceAccount:my-project-id@appspot.gserviceaccount.com       role: roles/resourcemanager.organizationAdmin     - members:       - user:eve@example.com       role: roles/resourcemanager.organizationViewer       condition:         title: expirable access         description: Does not grant access after Sep 2020         expression: request.time < timestamp('2020-10-01T00:00:00.000Z')     etag: BwWWja0YfJA=     version: 3`\ \`

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [resource]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # - The request isn't a proto-plus wrapped type,
            #   so it must be constructed via keyword expansion.
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.SetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_mute(
        self,
        request: Optional[Union[securitycenter_service.SetMuteRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        mute: Optional[finding.Finding.Mute] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> finding.Finding:
        r"""Updates the mute state of a finding. If no location
        is specified, finding is assumed to be in global

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_set_mute():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.SetMuteRequest(
                    name="name_value",
                    mute="UNDEFINED",
                )

                # Make the request
                response = client.set_mute(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.SetMuteRequest, dict]):
                The request object. Request message for updating a
                finding's mute status.
            name (str):
                Required. The `relative resource
                name <https://cloud.google.com/apis/design/resource_names#relative_resource_name>`__
                of the finding. If no location is specified, finding is
                assumed to be in global. The following list shows some
                examples:

                -

                ``organizations/{organization_id}/sources/{source_id}/findings/{finding_id}``
                +
                ``organizations/{organization_id}/sources/{source_id}/locations/{location_id}/findings/{finding_id}``

                -  ``folders/{folder_id}/sources/{source_id}/findings/{finding_id}``
                -

                ``folders/{folder_id}/sources/{source_id}/locations/{location_id}/findings/{finding_id}``

                -  ``projects/{project_id}/sources/{source_id}/findings/{finding_id}``
                -

                ``projects/{project_id}/sources/{source_id}/locations/{location_id}/findings/{finding_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mute (google.cloud.securitycenter_v2.types.Finding.Mute):
                Required. The desired state of the
                Mute.

                This corresponds to the ``mute`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.Finding:
                Security Command Center finding.

                A finding is a record of assessment data
                like security, risk, health, or privacy,
                that is ingested into Security Command
                Center for presentation, notification,
                analysis, policy testing, and
                enforcement. For example, a cross-site
                scripting (XSS) vulnerability in an App
                Engine application is a finding.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name, mute]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.SetMuteRequest):
            request = securitycenter_service.SetMuteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if mute is not None:
                request.mute = mute

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_mute]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def test_iam_permissions(
        self,
        request: Optional[Union[iam_policy_pb2.TestIamPermissionsRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        permissions: Optional[MutableSequence[str]] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns the permissions that a caller has on the
        specified source.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_test_iam_permissions():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.TestIamPermissionsRequest(
                    resource="resource_value",
                    permissions=['permissions_value1', 'permissions_value2'],
                )

                # Make the request
                response = client.test_iam_permissions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]):
                The request object. Request message for ``TestIamPermissions`` method.
            resource (str):
                REQUIRED: The resource for which the
                policy detail is being requested. See
                the operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (MutableSequence[str]):
                The set of permissions to check for the ``resource``.
                Permissions with wildcards (such as '*' or 'storage.*')
                are not allowed. For more information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

                This corresponds to the ``permissions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [resource, permissions]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # - The request isn't a proto-plus wrapped type,
            #   so it must be constructed via keyword expansion.
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.TestIamPermissionsRequest()
            if resource is not None:
                request.resource = resource
            if permissions:
                request.permissions.extend(permissions)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.test_iam_permissions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_big_query_export(
        self,
        request: Optional[
            Union[securitycenter_service.UpdateBigQueryExportRequest, dict]
        ] = None,
        *,
        big_query_export: Optional[bigquery_export.BigQueryExport] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> bigquery_export.BigQueryExport:
        r"""Updates a BigQuery export.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_update_big_query_export():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.UpdateBigQueryExportRequest(
                )

                # Make the request
                response = client.update_big_query_export(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.UpdateBigQueryExportRequest, dict]):
                The request object. Request message for updating a
                BigQuery export.
            big_query_export (google.cloud.securitycenter_v2.types.BigQueryExport):
                Required. The BigQuery export being
                updated.

                This corresponds to the ``big_query_export`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated.
                If empty all mutable fields will be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.BigQueryExport:
                Configures how to deliver Findings to
                BigQuery Instance.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [big_query_export, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.UpdateBigQueryExportRequest):
            request = securitycenter_service.UpdateBigQueryExportRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if big_query_export is not None:
                request.big_query_export = big_query_export
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_big_query_export]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("big_query_export.name", request.big_query_export.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_external_system(
        self,
        request: Optional[
            Union[securitycenter_service.UpdateExternalSystemRequest, dict]
        ] = None,
        *,
        external_system: Optional[gcs_external_system.ExternalSystem] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcs_external_system.ExternalSystem:
        r"""Updates external system. This is for a given finding.
        If no location is specified, finding is assumed to be in
        global

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_update_external_system():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.UpdateExternalSystemRequest(
                )

                # Make the request
                response = client.update_external_system(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.UpdateExternalSystemRequest, dict]):
                The request object. Request message for updating a
                ExternalSystem resource.
            external_system (google.cloud.securitycenter_v2.types.ExternalSystem):
                Required. The external system
                resource to update.

                This corresponds to the ``external_system`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The FieldMask to use when updating
                the external system resource.
                If empty all mutable fields will be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.ExternalSystem:
                Representation of third party
                SIEM/SOAR fields within SCC.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [external_system, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.UpdateExternalSystemRequest):
            request = securitycenter_service.UpdateExternalSystemRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if external_system is not None:
                request.external_system = external_system
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_external_system]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("external_system.name", request.external_system.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_finding(
        self,
        request: Optional[
            Union[securitycenter_service.UpdateFindingRequest, dict]
        ] = None,
        *,
        finding: Optional[gcs_finding.Finding] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcs_finding.Finding:
        r"""Creates or updates a finding. If no location is
        specified, finding is assumed to be in global. The
        corresponding source must exist for a finding creation
        to succeed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_update_finding():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.UpdateFindingRequest(
                )

                # Make the request
                response = client.update_finding(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.UpdateFindingRequest, dict]):
                The request object. Request message for updating or
                creating a finding.
            finding (google.cloud.securitycenter_v2.types.Finding):
                Required. The finding resource to update or create if it
                does not already exist. parent, security_marks, and
                update_time will be ignored.

                In the case of creation, the finding id portion of the
                name must be alphanumeric and less than or equal to 32
                characters and greater than 0 characters in length.

                This corresponds to the ``finding`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The FieldMask to use when updating the finding resource.
                This field should not be specified when creating a
                finding.

                When updating a finding, an empty mask is treated as
                updating all mutable fields and replacing
                source_properties. Individual source_properties can be
                added/updated by using "source_properties." in the field
                mask.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.Finding:
                Security Command Center finding.

                A finding is a record of assessment data
                like security, risk, health, or privacy,
                that is ingested into Security Command
                Center for presentation, notification,
                analysis, policy testing, and
                enforcement. For example, a cross-site
                scripting (XSS) vulnerability in an App
                Engine application is a finding.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [finding, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.UpdateFindingRequest):
            request = securitycenter_service.UpdateFindingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if finding is not None:
                request.finding = finding
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_finding]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("finding.name", request.finding.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_mute_config(
        self,
        request: Optional[
            Union[securitycenter_service.UpdateMuteConfigRequest, dict]
        ] = None,
        *,
        mute_config: Optional[gcs_mute_config.MuteConfig] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcs_mute_config.MuteConfig:
        r"""Updates a mute config. If no location is specified,
        default is global.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_update_mute_config():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                mute_config = securitycenter_v2.MuteConfig()
                mute_config.filter = "filter_value"
                mute_config.type_ = "DYNAMIC"

                request = securitycenter_v2.UpdateMuteConfigRequest(
                    mute_config=mute_config,
                )

                # Make the request
                response = client.update_mute_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.UpdateMuteConfigRequest, dict]):
                The request object. Request message for updating a mute
                config.
            mute_config (google.cloud.securitycenter_v2.types.MuteConfig):
                Required. The mute config being
                updated.

                This corresponds to the ``mute_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated.
                If empty all mutable fields will be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.MuteConfig:
                A mute config is a Cloud SCC resource
                that contains the configuration to mute
                create/update events of findings.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [mute_config, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.UpdateMuteConfigRequest):
            request = securitycenter_service.UpdateMuteConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if mute_config is not None:
                request.mute_config = mute_config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_mute_config]

        header_params = {}

        routing_param_regex = re.compile(
            "^projects/[^/]+/locations/(?P<location>[^/]+)/muteConfigs/[^/]+$"
        )
        regex_match = routing_param_regex.match(request.mute_config.name)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        routing_param_regex = re.compile(
            "^organizations/[^/]+/locations/(?P<location>[^/]+)/muteConfigs/[^/]+$"
        )
        regex_match = routing_param_regex.match(request.mute_config.name)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        routing_param_regex = re.compile(
            "^folders/[^/]+/locations/(?P<location>[^/]+)/muteConfigs/[^/]+$"
        )
        regex_match = routing_param_regex.match(request.mute_config.name)
        if regex_match and regex_match.group("location"):
            header_params["location"] = regex_match.group("location")

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_notification_config(
        self,
        request: Optional[
            Union[securitycenter_service.UpdateNotificationConfigRequest, dict]
        ] = None,
        *,
        notification_config: Optional[
            gcs_notification_config.NotificationConfig
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcs_notification_config.NotificationConfig:
        r"""Updates a notification config. The following update fields are
        allowed: description, pubsub_topic, streaming_config.filter

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_update_notification_config():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.UpdateNotificationConfigRequest(
                )

                # Make the request
                response = client.update_notification_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.UpdateNotificationConfigRequest, dict]):
                The request object. Request message for updating a
                notification config.
            notification_config (google.cloud.securitycenter_v2.types.NotificationConfig):
                Required. The notification config to
                update.

                This corresponds to the ``notification_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The FieldMask to use when updating
                the notification config.
                If empty all mutable fields will be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.NotificationConfig:
                Cloud Security Command Center (Cloud
                SCC) notification configs.
                A notification config is a Cloud SCC
                resource that contains the configuration
                to send notifications for create/update
                events of findings, assets and etc.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [notification_config, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, securitycenter_service.UpdateNotificationConfigRequest
        ):
            request = securitycenter_service.UpdateNotificationConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if notification_config is not None:
                request.notification_config = notification_config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_notification_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("notification_config.name", request.notification_config.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_resource_value_config(
        self,
        request: Optional[
            Union[securitycenter_service.UpdateResourceValueConfigRequest, dict]
        ] = None,
        *,
        resource_value_config: Optional[
            gcs_resource_value_config.ResourceValueConfig
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcs_resource_value_config.ResourceValueConfig:
        r"""Updates an existing ResourceValueConfigs with new
        rules.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_update_resource_value_config():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.UpdateResourceValueConfigRequest(
                )

                # Make the request
                response = client.update_resource_value_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.UpdateResourceValueConfigRequest, dict]):
                The request object. Request message to update resource
                value config
            resource_value_config (google.cloud.securitycenter_v2.types.ResourceValueConfig):
                Required. The resource value config
                being updated.

                This corresponds to the ``resource_value_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated. If empty all mutable
                fields will be updated.

                To update nested fields, include the top level field in
                the mask For example, to update
                gcp_metadata.resource_type, include the "gcp_metadata"
                field mask

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.ResourceValueConfig:
                A resource value configuration (RVC)
                is a mapping configuration of user's
                resources to resource values. Used in
                Attack path simulations.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [resource_value_config, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, securitycenter_service.UpdateResourceValueConfigRequest
        ):
            request = securitycenter_service.UpdateResourceValueConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if resource_value_config is not None:
                request.resource_value_config = resource_value_config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_resource_value_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("resource_value_config.name", request.resource_value_config.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_security_marks(
        self,
        request: Optional[
            Union[securitycenter_service.UpdateSecurityMarksRequest, dict]
        ] = None,
        *,
        security_marks: Optional[gcs_security_marks.SecurityMarks] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcs_security_marks.SecurityMarks:
        r"""Updates security marks. For Finding Security marks,
        if no location is specified, finding is assumed to be in
        global. Assets Security Marks can only be accessed
        through global endpoint.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_update_security_marks():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.UpdateSecurityMarksRequest(
                )

                # Make the request
                response = client.update_security_marks(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.UpdateSecurityMarksRequest, dict]):
                The request object. Request message for updating a
                SecurityMarks resource.
            security_marks (google.cloud.securitycenter_v2.types.SecurityMarks):
                Required. The security marks resource
                to update.

                This corresponds to the ``security_marks`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The FieldMask to use when updating the security marks
                resource.

                The field mask must not contain duplicate fields. If
                empty or set to "marks", all marks will be replaced.
                Individual marks can be updated using
                "marks.<mark_key>".

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.SecurityMarks:
                User specified security marks that
                are attached to the parent Security
                Command Center resource. Security marks
                are scoped within a Security Command
                Center organization -- they can be
                modified and viewed by all users who
                have proper permissions on the
                organization.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [security_marks, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.UpdateSecurityMarksRequest):
            request = securitycenter_service.UpdateSecurityMarksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if security_marks is not None:
                request.security_marks = security_marks
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_security_marks]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("security_marks.name", request.security_marks.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_source(
        self,
        request: Optional[
            Union[securitycenter_service.UpdateSourceRequest, dict]
        ] = None,
        *,
        source: Optional[gcs_source.Source] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gcs_source.Source:
        r"""Updates a source.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import securitycenter_v2

            def sample_update_source():
                # Create a client
                client = securitycenter_v2.SecurityCenterClient()

                # Initialize request argument(s)
                request = securitycenter_v2.UpdateSourceRequest(
                )

                # Make the request
                response = client.update_source(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.securitycenter_v2.types.UpdateSourceRequest, dict]):
                The request object. Request message for updating a
                source.
            source (google.cloud.securitycenter_v2.types.Source):
                Required. The source resource to
                update.

                This corresponds to the ``source`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The FieldMask to use when updating
                the source resource.
                If empty all mutable fields will be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.securitycenter_v2.types.Source:
                Security Command Center finding
                source. A finding source is an entity or
                a mechanism that can produce a finding.
                A source is like a container of findings
                that come from the same scanner, logger,
                monitor, and other tools.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [source, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, securitycenter_service.UpdateSourceRequest):
            request = securitycenter_service.UpdateSourceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if source is not None:
                request.source = source
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_source]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("source.name", request.source.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "SecurityCenterClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_operations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        try:
            # Send the request.
            response = rpc(
                request,
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            )

            # Done; return the response.
            return response
        except core_exceptions.GoogleAPICallError as e:
            self._add_cred_info_for_auth_errors(e)
            raise e

    def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_operation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        try:
            # Send the request.
            response = rpc(
                request,
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            )

            # Done; return the response.
            return response
        except core_exceptions.GoogleAPICallError as e:
            self._add_cred_info_for_auth_errors(e)
            raise e

    def delete_operation(
        self,
        request: Optional[operations_pb2.DeleteOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes a long-running operation.

        This method indicates that the client is no longer interested
        in the operation result. It does not cancel the operation.
        If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.DeleteOperationRequest`):
                The request object. Request message for
                `DeleteOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.DeleteOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_operation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.cancel_operation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__

__all__ = ("SecurityCenterClient",)

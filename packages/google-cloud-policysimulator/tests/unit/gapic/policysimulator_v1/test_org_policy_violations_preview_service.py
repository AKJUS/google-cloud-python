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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import AsyncIterable, Iterable
import json
import math

from google.api_core import api_core_version
from google.protobuf import json_format
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

try:
    from google.auth.aio import credentials as ga_credentials_async

    HAS_GOOGLE_AUTH_AIO = True
except ImportError:  # pragma: NO COVER
    HAS_GOOGLE_AUTH_AIO = False

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.orgpolicy_v2.types import constraint
from google.cloud.orgpolicy_v2.types import orgpolicy as gcov_orgpolicy
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore

from google.cloud.policysimulator_v1.services.org_policy_violations_preview_service import (
    OrgPolicyViolationsPreviewServiceAsyncClient,
    OrgPolicyViolationsPreviewServiceClient,
    pagers,
    transports,
)
from google.cloud.policysimulator_v1.types import orgpolicy as gcp_orgpolicy

CRED_INFO_JSON = {
    "credential_source": "/path/to/file",
    "credential_type": "service account credentials",
    "principal": "service-account@example.com",
}
CRED_INFO_STRING = json.dumps(CRED_INFO_JSON)


async def mock_async_gen(data, chunk_size=1):
    for i in range(0, len(data)):  # pragma: NO COVER
        chunk = data[i : i + chunk_size]
        yield chunk.encode("utf-8")


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# TODO: use async auth anon credentials by default once the minimum version of google-auth is upgraded.
# See related issue: https://github.com/googleapis/gapic-generator-python/issues/2107.
def async_anonymous_credentials():
    if HAS_GOOGLE_AUTH_AIO:
        return ga_credentials_async.AnonymousCredentials()
    return ga_credentials.AnonymousCredentials()


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert (
        OrgPolicyViolationsPreviewServiceClient._get_default_mtls_endpoint(None) is None
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_default_mtls_endpoint(
            api_mtls_endpoint
        )
        == api_mtls_endpoint
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_default_mtls_endpoint(
            sandbox_endpoint
        )
        == sandbox_mtls_endpoint
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_default_mtls_endpoint(
            sandbox_mtls_endpoint
        )
        == sandbox_mtls_endpoint
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_default_mtls_endpoint(
            non_googleapi
        )
        == non_googleapi
    )


def test__read_environment_variables():
    assert OrgPolicyViolationsPreviewServiceClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert (
            OrgPolicyViolationsPreviewServiceClient._read_environment_variables()
            == (True, "auto", None)
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert (
            OrgPolicyViolationsPreviewServiceClient._read_environment_variables()
            == (False, "auto", None)
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            OrgPolicyViolationsPreviewServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert (
            OrgPolicyViolationsPreviewServiceClient._read_environment_variables()
            == (False, "never", None)
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert (
            OrgPolicyViolationsPreviewServiceClient._read_environment_variables()
            == (False, "always", None)
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert (
            OrgPolicyViolationsPreviewServiceClient._read_environment_variables()
            == (False, "auto", None)
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            OrgPolicyViolationsPreviewServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert (
            OrgPolicyViolationsPreviewServiceClient._read_environment_variables()
            == (False, "auto", "foo.com")
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert (
        OrgPolicyViolationsPreviewServiceClient._get_client_cert_source(None, False)
        is None
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_client_cert_source(
            mock_provided_cert_source, True
        )
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                OrgPolicyViolationsPreviewServiceClient._get_client_cert_source(
                    None, True
                )
                is mock_default_cert_source
            )
            assert (
                OrgPolicyViolationsPreviewServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    OrgPolicyViolationsPreviewServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OrgPolicyViolationsPreviewServiceClient),
)
@mock.patch.object(
    OrgPolicyViolationsPreviewServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OrgPolicyViolationsPreviewServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = OrgPolicyViolationsPreviewServiceClient._DEFAULT_UNIVERSE
    default_endpoint = (
        OrgPolicyViolationsPreviewServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=default_universe
        )
    )
    mock_universe = "bar.com"
    mock_endpoint = (
        OrgPolicyViolationsPreviewServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=mock_universe
        )
    )

    assert (
        OrgPolicyViolationsPreviewServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == OrgPolicyViolationsPreviewServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_api_endpoint(
            None, None, default_universe, "auto"
        )
        == default_endpoint
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == OrgPolicyViolationsPreviewServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == OrgPolicyViolationsPreviewServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_api_endpoint(
            None, None, mock_universe, "never"
        )
        == mock_endpoint
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        OrgPolicyViolationsPreviewServiceClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        OrgPolicyViolationsPreviewServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_universe_domain(
            None, universe_domain_env
        )
        == universe_domain_env
    )
    assert (
        OrgPolicyViolationsPreviewServiceClient._get_universe_domain(None, None)
        == OrgPolicyViolationsPreviewServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        OrgPolicyViolationsPreviewServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "error_code,cred_info_json,show_cred_info",
    [
        (401, CRED_INFO_JSON, True),
        (403, CRED_INFO_JSON, True),
        (404, CRED_INFO_JSON, True),
        (500, CRED_INFO_JSON, False),
        (401, None, False),
        (403, None, False),
        (404, None, False),
        (500, None, False),
    ],
)
def test__add_cred_info_for_auth_errors(error_code, cred_info_json, show_cred_info):
    cred = mock.Mock(["get_cred_info"])
    cred.get_cred_info = mock.Mock(return_value=cred_info_json)
    client = OrgPolicyViolationsPreviewServiceClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=["foo"])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    if show_cred_info:
        assert error.details == ["foo", CRED_INFO_STRING]
    else:
        assert error.details == ["foo"]


@pytest.mark.parametrize("error_code", [401, 403, 404, 500])
def test__add_cred_info_for_auth_errors_no_get_cred_info(error_code):
    cred = mock.Mock([])
    assert not hasattr(cred, "get_cred_info")
    client = OrgPolicyViolationsPreviewServiceClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=[])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    assert error.details == []


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (OrgPolicyViolationsPreviewServiceClient, "grpc"),
        (OrgPolicyViolationsPreviewServiceAsyncClient, "grpc_asyncio"),
        (OrgPolicyViolationsPreviewServiceClient, "rest"),
    ],
)
def test_org_policy_violations_preview_service_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "policysimulator.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://policysimulator.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.OrgPolicyViolationsPreviewServiceGrpcTransport, "grpc"),
        (
            transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (transports.OrgPolicyViolationsPreviewServiceRestTransport, "rest"),
    ],
)
def test_org_policy_violations_preview_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (OrgPolicyViolationsPreviewServiceClient, "grpc"),
        (OrgPolicyViolationsPreviewServiceAsyncClient, "grpc_asyncio"),
        (OrgPolicyViolationsPreviewServiceClient, "rest"),
    ],
)
def test_org_policy_violations_preview_service_client_from_service_account_file(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "policysimulator.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://policysimulator.googleapis.com"
        )


def test_org_policy_violations_preview_service_client_get_transport_class():
    transport = OrgPolicyViolationsPreviewServiceClient.get_transport_class()
    available_transports = [
        transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
        transports.OrgPolicyViolationsPreviewServiceRestTransport,
    ]
    assert transport in available_transports

    transport = OrgPolicyViolationsPreviewServiceClient.get_transport_class("grpc")
    assert transport == transports.OrgPolicyViolationsPreviewServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
            "grpc",
        ),
        (
            OrgPolicyViolationsPreviewServiceAsyncClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    OrgPolicyViolationsPreviewServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OrgPolicyViolationsPreviewServiceClient),
)
@mock.patch.object(
    OrgPolicyViolationsPreviewServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OrgPolicyViolationsPreviewServiceAsyncClient),
)
def test_org_policy_violations_preview_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        OrgPolicyViolationsPreviewServiceClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        OrgPolicyViolationsPreviewServiceClient, "get_transport_class"
    ) as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            OrgPolicyViolationsPreviewServiceAsyncClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            OrgPolicyViolationsPreviewServiceAsyncClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceRestTransport,
            "rest",
            "true",
        ),
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    OrgPolicyViolationsPreviewServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OrgPolicyViolationsPreviewServiceClient),
)
@mock.patch.object(
    OrgPolicyViolationsPreviewServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OrgPolicyViolationsPreviewServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_org_policy_violations_preview_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class",
    [
        OrgPolicyViolationsPreviewServiceClient,
        OrgPolicyViolationsPreviewServiceAsyncClient,
    ],
)
@mock.patch.object(
    OrgPolicyViolationsPreviewServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OrgPolicyViolationsPreviewServiceClient),
)
@mock.patch.object(
    OrgPolicyViolationsPreviewServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OrgPolicyViolationsPreviewServiceAsyncClient),
)
def test_org_policy_violations_preview_service_client_get_mtls_endpoint_and_cert_source(
    client_class,
):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize(
    "client_class",
    [
        OrgPolicyViolationsPreviewServiceClient,
        OrgPolicyViolationsPreviewServiceAsyncClient,
    ],
)
@mock.patch.object(
    OrgPolicyViolationsPreviewServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OrgPolicyViolationsPreviewServiceClient),
)
@mock.patch.object(
    OrgPolicyViolationsPreviewServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OrgPolicyViolationsPreviewServiceAsyncClient),
)
def test_org_policy_violations_preview_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = OrgPolicyViolationsPreviewServiceClient._DEFAULT_UNIVERSE
    default_endpoint = (
        OrgPolicyViolationsPreviewServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=default_universe
        )
    )
    mock_universe = "bar.com"
    mock_endpoint = (
        OrgPolicyViolationsPreviewServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=mock_universe
        )
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    else:
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
            "grpc",
        ),
        (
            OrgPolicyViolationsPreviewServiceAsyncClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceRestTransport,
            "rest",
        ),
    ],
)
def test_org_policy_violations_preview_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            OrgPolicyViolationsPreviewServiceAsyncClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_org_policy_violations_preview_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_org_policy_violations_preview_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.policysimulator_v1.services.org_policy_violations_preview_service.transports.OrgPolicyViolationsPreviewServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = OrgPolicyViolationsPreviewServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            OrgPolicyViolationsPreviewServiceAsyncClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_org_policy_violations_preview_service_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "policysimulator.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="policysimulator.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest,
        dict,
    ],
)
def test_list_org_policy_violations_previews(request_type, transport: str = "grpc"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_org_policy_violations_previews(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOrgPolicyViolationsPreviewsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_org_policy_violations_previews_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_org_policy_violations_previews(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_org_policy_violations_previews_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_org_policy_violations_previews
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_org_policy_violations_previews
        ] = mock_rpc
        request = {}
        client.list_org_policy_violations_previews(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_org_policy_violations_previews(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_org_policy_violations_previews_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_org_policy_violations_previews
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_org_policy_violations_previews
        ] = mock_rpc

        request = {}
        await client.list_org_policy_violations_previews(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_org_policy_violations_previews(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_org_policy_violations_previews_async(
    transport: str = "grpc_asyncio",
    request_type=gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest,
):
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_org_policy_violations_previews(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOrgPolicyViolationsPreviewsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_org_policy_violations_previews_async_from_dict():
    await test_list_org_policy_violations_previews_async(request_type=dict)


def test_list_org_policy_violations_previews_field_headers():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        call.return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse()
        client.list_org_policy_violations_previews(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_org_policy_violations_previews_field_headers_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse()
        )
        await client.list_org_policy_violations_previews(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_org_policy_violations_previews_flattened():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_org_policy_violations_previews(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_org_policy_violations_previews_flattened_error():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_org_policy_violations_previews(
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_org_policy_violations_previews_flattened_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_org_policy_violations_previews(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_org_policy_violations_previews_flattened_error_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_org_policy_violations_previews(
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest(),
            parent="parent_value",
        )


def test_list_org_policy_violations_previews_pager(transport_name: str = "grpc"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
                next_page_token="abc",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[],
                next_page_token="def",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
                next_page_token="ghi",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_org_policy_violations_previews(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, gcp_orgpolicy.OrgPolicyViolationsPreview) for i in results
        )


def test_list_org_policy_violations_previews_pages(transport_name: str = "grpc"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
                next_page_token="abc",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[],
                next_page_token="def",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
                next_page_token="ghi",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_org_policy_violations_previews(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_org_policy_violations_previews_async_pager():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
                next_page_token="abc",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[],
                next_page_token="def",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
                next_page_token="ghi",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_org_policy_violations_previews(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, gcp_orgpolicy.OrgPolicyViolationsPreview) for i in responses
        )


@pytest.mark.asyncio
async def test_list_org_policy_violations_previews_async_pages():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
                next_page_token="abc",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[],
                next_page_token="def",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
                next_page_token="ghi",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_org_policy_violations_previews(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest,
        dict,
    ],
)
def test_get_org_policy_violations_preview(request_type, transport: str = "grpc"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_org_policy_violations_preview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcp_orgpolicy.OrgPolicyViolationsPreview(
            name="name_value",
            state=gcp_orgpolicy.PreviewState.PREVIEW_PENDING,
            violations_count=1744,
            custom_constraints=["custom_constraints_value"],
        )
        response = client.get_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcp_orgpolicy.OrgPolicyViolationsPreview)
    assert response.name == "name_value"
    assert response.state == gcp_orgpolicy.PreviewState.PREVIEW_PENDING
    assert response.violations_count == 1744
    assert response.custom_constraints == ["custom_constraints_value"]


def test_get_org_policy_violations_preview_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_org_policy_violations_preview), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_org_policy_violations_preview(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest(
            name="name_value",
        )


def test_get_org_policy_violations_preview_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_org_policy_violations_preview
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_org_policy_violations_preview
        ] = mock_rpc
        request = {}
        client.get_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_org_policy_violations_preview(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_org_policy_violations_preview_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_org_policy_violations_preview
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_org_policy_violations_preview
        ] = mock_rpc

        request = {}
        await client.get_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_org_policy_violations_preview(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_org_policy_violations_preview_async(
    transport: str = "grpc_asyncio",
    request_type=gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest,
):
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_org_policy_violations_preview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.OrgPolicyViolationsPreview(
                name="name_value",
                state=gcp_orgpolicy.PreviewState.PREVIEW_PENDING,
                violations_count=1744,
                custom_constraints=["custom_constraints_value"],
            )
        )
        response = await client.get_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcp_orgpolicy.OrgPolicyViolationsPreview)
    assert response.name == "name_value"
    assert response.state == gcp_orgpolicy.PreviewState.PREVIEW_PENDING
    assert response.violations_count == 1744
    assert response.custom_constraints == ["custom_constraints_value"]


@pytest.mark.asyncio
async def test_get_org_policy_violations_preview_async_from_dict():
    await test_get_org_policy_violations_preview_async(request_type=dict)


def test_get_org_policy_violations_preview_field_headers():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_org_policy_violations_preview), "__call__"
    ) as call:
        call.return_value = gcp_orgpolicy.OrgPolicyViolationsPreview()
        client.get_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_org_policy_violations_preview_field_headers_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_org_policy_violations_preview), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.OrgPolicyViolationsPreview()
        )
        await client.get_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_org_policy_violations_preview_flattened():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_org_policy_violations_preview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcp_orgpolicy.OrgPolicyViolationsPreview()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_org_policy_violations_preview(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_org_policy_violations_preview_flattened_error():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_org_policy_violations_preview(
            gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_org_policy_violations_preview_flattened_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_org_policy_violations_preview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcp_orgpolicy.OrgPolicyViolationsPreview()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.OrgPolicyViolationsPreview()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_org_policy_violations_preview(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_org_policy_violations_preview_flattened_error_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_org_policy_violations_preview(
            gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest,
        dict,
    ],
)
def test_create_org_policy_violations_preview(request_type, transport: str = "grpc"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_org_policy_violations_preview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_org_policy_violations_preview_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest(
        parent="parent_value",
        org_policy_violations_preview_id="org_policy_violations_preview_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_org_policy_violations_preview), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_org_policy_violations_preview(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest(
            parent="parent_value",
            org_policy_violations_preview_id="org_policy_violations_preview_id_value",
        )


def test_create_org_policy_violations_preview_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_org_policy_violations_preview
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_org_policy_violations_preview
        ] = mock_rpc
        request = {}
        client.create_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_org_policy_violations_preview(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_org_policy_violations_preview_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_org_policy_violations_preview
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_org_policy_violations_preview
        ] = mock_rpc

        request = {}
        await client.create_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_org_policy_violations_preview(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_org_policy_violations_preview_async(
    transport: str = "grpc_asyncio",
    request_type=gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest,
):
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_org_policy_violations_preview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_org_policy_violations_preview_async_from_dict():
    await test_create_org_policy_violations_preview_async(request_type=dict)


def test_create_org_policy_violations_preview_field_headers():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_org_policy_violations_preview), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_org_policy_violations_preview_field_headers_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_org_policy_violations_preview), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_org_policy_violations_preview_flattened():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_org_policy_violations_preview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_org_policy_violations_preview(
            parent="parent_value",
            org_policy_violations_preview=gcp_orgpolicy.OrgPolicyViolationsPreview(
                name="name_value"
            ),
            org_policy_violations_preview_id="org_policy_violations_preview_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].org_policy_violations_preview
        mock_val = gcp_orgpolicy.OrgPolicyViolationsPreview(name="name_value")
        assert arg == mock_val
        arg = args[0].org_policy_violations_preview_id
        mock_val = "org_policy_violations_preview_id_value"
        assert arg == mock_val


def test_create_org_policy_violations_preview_flattened_error():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_org_policy_violations_preview(
            gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest(),
            parent="parent_value",
            org_policy_violations_preview=gcp_orgpolicy.OrgPolicyViolationsPreview(
                name="name_value"
            ),
            org_policy_violations_preview_id="org_policy_violations_preview_id_value",
        )


@pytest.mark.asyncio
async def test_create_org_policy_violations_preview_flattened_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_org_policy_violations_preview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_org_policy_violations_preview(
            parent="parent_value",
            org_policy_violations_preview=gcp_orgpolicy.OrgPolicyViolationsPreview(
                name="name_value"
            ),
            org_policy_violations_preview_id="org_policy_violations_preview_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].org_policy_violations_preview
        mock_val = gcp_orgpolicy.OrgPolicyViolationsPreview(name="name_value")
        assert arg == mock_val
        arg = args[0].org_policy_violations_preview_id
        mock_val = "org_policy_violations_preview_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_org_policy_violations_preview_flattened_error_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_org_policy_violations_preview(
            gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest(),
            parent="parent_value",
            org_policy_violations_preview=gcp_orgpolicy.OrgPolicyViolationsPreview(
                name="name_value"
            ),
            org_policy_violations_preview_id="org_policy_violations_preview_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcp_orgpolicy.ListOrgPolicyViolationsRequest,
        dict,
    ],
)
def test_list_org_policy_violations(request_type, transport: str = "grpc"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_org_policy_violations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gcp_orgpolicy.ListOrgPolicyViolationsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOrgPolicyViolationsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_org_policy_violations_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gcp_orgpolicy.ListOrgPolicyViolationsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_org_policy_violations(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcp_orgpolicy.ListOrgPolicyViolationsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_org_policy_violations_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_org_policy_violations
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_org_policy_violations
        ] = mock_rpc
        request = {}
        client.list_org_policy_violations(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_org_policy_violations(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_org_policy_violations_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_org_policy_violations
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_org_policy_violations
        ] = mock_rpc

        request = {}
        await client.list_org_policy_violations(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_org_policy_violations(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_org_policy_violations_async(
    transport: str = "grpc_asyncio",
    request_type=gcp_orgpolicy.ListOrgPolicyViolationsRequest,
):
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_org_policy_violations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gcp_orgpolicy.ListOrgPolicyViolationsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOrgPolicyViolationsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_org_policy_violations_async_from_dict():
    await test_list_org_policy_violations_async(request_type=dict)


def test_list_org_policy_violations_field_headers():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcp_orgpolicy.ListOrgPolicyViolationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        call.return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse()
        client.list_org_policy_violations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_org_policy_violations_field_headers_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcp_orgpolicy.ListOrgPolicyViolationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.ListOrgPolicyViolationsResponse()
        )
        await client.list_org_policy_violations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_org_policy_violations_flattened():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_org_policy_violations(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_org_policy_violations_flattened_error():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_org_policy_violations(
            gcp_orgpolicy.ListOrgPolicyViolationsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_org_policy_violations_flattened_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.ListOrgPolicyViolationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_org_policy_violations(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_org_policy_violations_flattened_error_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_org_policy_violations(
            gcp_orgpolicy.ListOrgPolicyViolationsRequest(),
            parent="parent_value",
        )


def test_list_org_policy_violations_pager(transport_name: str = "grpc"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
                next_page_token="abc",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[],
                next_page_token="def",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
                next_page_token="ghi",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_org_policy_violations(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, gcp_orgpolicy.OrgPolicyViolation) for i in results)


def test_list_org_policy_violations_pages(transport_name: str = "grpc"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
                next_page_token="abc",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[],
                next_page_token="def",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
                next_page_token="ghi",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_org_policy_violations(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_org_policy_violations_async_pager():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
                next_page_token="abc",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[],
                next_page_token="def",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
                next_page_token="ghi",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_org_policy_violations(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, gcp_orgpolicy.OrgPolicyViolation) for i in responses)


@pytest.mark.asyncio
async def test_list_org_policy_violations_async_pages():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
                next_page_token="abc",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[],
                next_page_token="def",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
                next_page_token="ghi",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_org_policy_violations(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_org_policy_violations_previews_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_org_policy_violations_previews
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_org_policy_violations_previews
        ] = mock_rpc

        request = {}
        client.list_org_policy_violations_previews(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_org_policy_violations_previews(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_org_policy_violations_previews_rest_required_fields(
    request_type=gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest,
):
    transport_class = transports.OrgPolicyViolationsPreviewServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_org_policy_violations_previews._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_org_policy_violations_previews._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_org_policy_violations_previews(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_org_policy_violations_previews_rest_unset_required_fields():
    transport = transports.OrgPolicyViolationsPreviewServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.list_org_policy_violations_previews._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_org_policy_violations_previews_rest_flattened():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "organizations/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_org_policy_violations_previews(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=organizations/*/locations/*}/orgPolicyViolationsPreviews"
            % client.transport._host,
            args[1],
        )


def test_list_org_policy_violations_previews_rest_flattened_error(
    transport: str = "rest",
):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_org_policy_violations_previews(
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest(),
            parent="parent_value",
        )


def test_list_org_policy_violations_previews_rest_pager(transport: str = "rest"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
                next_page_token="abc",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[],
                next_page_token="def",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
                next_page_token="ghi",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                org_policy_violations_previews=[
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                    gcp_orgpolicy.OrgPolicyViolationsPreview(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "organizations/sample1/locations/sample2"}

        pager = client.list_org_policy_violations_previews(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, gcp_orgpolicy.OrgPolicyViolationsPreview) for i in results
        )

        pages = list(
            client.list_org_policy_violations_previews(request=sample_request).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_org_policy_violations_preview_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_org_policy_violations_preview
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_org_policy_violations_preview
        ] = mock_rpc

        request = {}
        client.get_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_org_policy_violations_preview(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_org_policy_violations_preview_rest_required_fields(
    request_type=gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest,
):
    transport_class = transports.OrgPolicyViolationsPreviewServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_org_policy_violations_preview._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_org_policy_violations_preview._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcp_orgpolicy.OrgPolicyViolationsPreview()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gcp_orgpolicy.OrgPolicyViolationsPreview.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_org_policy_violations_preview(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_org_policy_violations_preview_rest_unset_required_fields():
    transport = transports.OrgPolicyViolationsPreviewServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.get_org_policy_violations_preview._get_unset_required_fields({})
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_org_policy_violations_preview_rest_flattened():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcp_orgpolicy.OrgPolicyViolationsPreview()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "organizations/sample1/locations/sample2/orgPolicyViolationsPreviews/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gcp_orgpolicy.OrgPolicyViolationsPreview.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_org_policy_violations_preview(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=organizations/*/locations/*/orgPolicyViolationsPreviews/*}"
            % client.transport._host,
            args[1],
        )


def test_get_org_policy_violations_preview_rest_flattened_error(
    transport: str = "rest",
):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_org_policy_violations_preview(
            gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest(),
            name="name_value",
        )


def test_create_org_policy_violations_preview_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_org_policy_violations_preview
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_org_policy_violations_preview
        ] = mock_rpc

        request = {}
        client.create_org_policy_violations_preview(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_org_policy_violations_preview(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_org_policy_violations_preview_rest_required_fields(
    request_type=gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest,
):
    transport_class = transports.OrgPolicyViolationsPreviewServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_org_policy_violations_preview._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_org_policy_violations_preview._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("org_policy_violations_preview_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.create_org_policy_violations_preview(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_org_policy_violations_preview_rest_unset_required_fields():
    transport = transports.OrgPolicyViolationsPreviewServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.create_org_policy_violations_preview._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(("orgPolicyViolationsPreviewId",))
        & set(
            (
                "parent",
                "orgPolicyViolationsPreview",
            )
        )
    )


def test_create_org_policy_violations_preview_rest_flattened():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "organizations/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            org_policy_violations_preview=gcp_orgpolicy.OrgPolicyViolationsPreview(
                name="name_value"
            ),
            org_policy_violations_preview_id="org_policy_violations_preview_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.create_org_policy_violations_preview(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=organizations/*/locations/*}/orgPolicyViolationsPreviews"
            % client.transport._host,
            args[1],
        )


def test_create_org_policy_violations_preview_rest_flattened_error(
    transport: str = "rest",
):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_org_policy_violations_preview(
            gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest(),
            parent="parent_value",
            org_policy_violations_preview=gcp_orgpolicy.OrgPolicyViolationsPreview(
                name="name_value"
            ),
            org_policy_violations_preview_id="org_policy_violations_preview_id_value",
        )


def test_list_org_policy_violations_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OrgPolicyViolationsPreviewServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_org_policy_violations
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_org_policy_violations
        ] = mock_rpc

        request = {}
        client.list_org_policy_violations(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_org_policy_violations(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_org_policy_violations_rest_required_fields(
    request_type=gcp_orgpolicy.ListOrgPolicyViolationsRequest,
):
    transport_class = transports.OrgPolicyViolationsPreviewServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_org_policy_violations._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_org_policy_violations._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_org_policy_violations(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_org_policy_violations_rest_unset_required_fields():
    transport = transports.OrgPolicyViolationsPreviewServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_org_policy_violations._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_org_policy_violations_rest_flattened():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "organizations/sample1/locations/sample2/orgPolicyViolationsPreviews/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_org_policy_violations(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=organizations/*/locations/*/orgPolicyViolationsPreviews/*}/orgPolicyViolations"
            % client.transport._host,
            args[1],
        )


def test_list_org_policy_violations_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_org_policy_violations(
            gcp_orgpolicy.ListOrgPolicyViolationsRequest(),
            parent="parent_value",
        )


def test_list_org_policy_violations_rest_pager(transport: str = "rest"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
                next_page_token="abc",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[],
                next_page_token="def",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
                next_page_token="ghi",
            ),
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                org_policy_violations=[
                    gcp_orgpolicy.OrgPolicyViolation(),
                    gcp_orgpolicy.OrgPolicyViolation(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            gcp_orgpolicy.ListOrgPolicyViolationsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "organizations/sample1/locations/sample2/orgPolicyViolationsPreviews/sample3"
        }

        pager = client.list_org_policy_violations(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, gcp_orgpolicy.OrgPolicyViolation) for i in results)

        pages = list(client.list_org_policy_violations(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.OrgPolicyViolationsPreviewServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OrgPolicyViolationsPreviewServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.OrgPolicyViolationsPreviewServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OrgPolicyViolationsPreviewServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.OrgPolicyViolationsPreviewServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = OrgPolicyViolationsPreviewServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = OrgPolicyViolationsPreviewServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.OrgPolicyViolationsPreviewServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OrgPolicyViolationsPreviewServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OrgPolicyViolationsPreviewServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = OrgPolicyViolationsPreviewServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OrgPolicyViolationsPreviewServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
        transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
        transports.OrgPolicyViolationsPreviewServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = OrgPolicyViolationsPreviewServiceClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_org_policy_violations_previews_empty_call_grpc():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        call.return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse()
        client.list_org_policy_violations_previews(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_org_policy_violations_preview_empty_call_grpc():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_org_policy_violations_preview), "__call__"
    ) as call:
        call.return_value = gcp_orgpolicy.OrgPolicyViolationsPreview()
        client.get_org_policy_violations_preview(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_org_policy_violations_preview_empty_call_grpc():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_org_policy_violations_preview), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_org_policy_violations_preview(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_org_policy_violations_empty_call_grpc():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        call.return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse()
        client.list_org_policy_violations(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.ListOrgPolicyViolationsRequest()

        assert args[0] == request_msg


def test_transport_kind_grpc_asyncio():
    transport = OrgPolicyViolationsPreviewServiceAsyncClient.get_transport_class(
        "grpc_asyncio"
    )(credentials=async_anonymous_credentials())
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_org_policy_violations_previews_empty_call_grpc_asyncio():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_org_policy_violations_previews(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_org_policy_violations_preview_empty_call_grpc_asyncio():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_org_policy_violations_preview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.OrgPolicyViolationsPreview(
                name="name_value",
                state=gcp_orgpolicy.PreviewState.PREVIEW_PENDING,
                violations_count=1744,
                custom_constraints=["custom_constraints_value"],
            )
        )
        await client.get_org_policy_violations_preview(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_org_policy_violations_preview_empty_call_grpc_asyncio():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_org_policy_violations_preview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.create_org_policy_violations_preview(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_org_policy_violations_empty_call_grpc_asyncio():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_org_policy_violations(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.ListOrgPolicyViolationsRequest()

        assert args[0] == request_msg


def test_transport_kind_rest():
    transport = OrgPolicyViolationsPreviewServiceClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_list_org_policy_violations_previews_rest_bad_request(
    request_type=gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest,
):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_org_policy_violations_previews(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest,
        dict,
    ],
)
def test_list_org_policy_violations_previews_rest_call_success(request_type):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_org_policy_violations_previews(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOrgPolicyViolationsPreviewsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_org_policy_violations_previews_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyViolationsPreviewServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OrgPolicyViolationsPreviewServiceRestInterceptor(),
    )
    client = OrgPolicyViolationsPreviewServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "post_list_org_policy_violations_previews",
    ) as post, mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "post_list_org_policy_violations_previews_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "pre_list_org_policy_violations_previews",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest.pb(
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse.to_json(
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse()
        )
        req.return_value.content = return_value

        request = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse()
        post_with_metadata.return_value = (
            gcp_orgpolicy.ListOrgPolicyViolationsPreviewsResponse(),
            metadata,
        )

        client.list_org_policy_violations_previews(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_org_policy_violations_preview_rest_bad_request(
    request_type=gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest,
):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "organizations/sample1/locations/sample2/orgPolicyViolationsPreviews/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_org_policy_violations_preview(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest,
        dict,
    ],
)
def test_get_org_policy_violations_preview_rest_call_success(request_type):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "organizations/sample1/locations/sample2/orgPolicyViolationsPreviews/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcp_orgpolicy.OrgPolicyViolationsPreview(
            name="name_value",
            state=gcp_orgpolicy.PreviewState.PREVIEW_PENDING,
            violations_count=1744,
            custom_constraints=["custom_constraints_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gcp_orgpolicy.OrgPolicyViolationsPreview.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_org_policy_violations_preview(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcp_orgpolicy.OrgPolicyViolationsPreview)
    assert response.name == "name_value"
    assert response.state == gcp_orgpolicy.PreviewState.PREVIEW_PENDING
    assert response.violations_count == 1744
    assert response.custom_constraints == ["custom_constraints_value"]


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_org_policy_violations_preview_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyViolationsPreviewServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OrgPolicyViolationsPreviewServiceRestInterceptor(),
    )
    client = OrgPolicyViolationsPreviewServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "post_get_org_policy_violations_preview",
    ) as post, mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "post_get_org_policy_violations_preview_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "pre_get_org_policy_violations_preview",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest.pb(
            gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = gcp_orgpolicy.OrgPolicyViolationsPreview.to_json(
            gcp_orgpolicy.OrgPolicyViolationsPreview()
        )
        req.return_value.content = return_value

        request = gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcp_orgpolicy.OrgPolicyViolationsPreview()
        post_with_metadata.return_value = (
            gcp_orgpolicy.OrgPolicyViolationsPreview(),
            metadata,
        )

        client.get_org_policy_violations_preview(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_create_org_policy_violations_preview_rest_bad_request(
    request_type=gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest,
):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.create_org_policy_violations_preview(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest,
        dict,
    ],
)
def test_create_org_policy_violations_preview_rest_call_success(request_type):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1/locations/sample2"}
    request_init["org_policy_violations_preview"] = {
        "name": "name_value",
        "state": 1,
        "overlay": {
            "policies": [
                {
                    "policy_parent": "policy_parent_value",
                    "policy": {
                        "name": "name_value",
                        "spec": {
                            "etag": "etag_value",
                            "update_time": {"seconds": 751, "nanos": 543},
                            "rules": [
                                {
                                    "values": {
                                        "allowed_values": [
                                            "allowed_values_value1",
                                            "allowed_values_value2",
                                        ],
                                        "denied_values": [
                                            "denied_values_value1",
                                            "denied_values_value2",
                                        ],
                                    },
                                    "allow_all": True,
                                    "deny_all": True,
                                    "enforce": True,
                                    "condition": {
                                        "expression": "expression_value",
                                        "title": "title_value",
                                        "description": "description_value",
                                        "location": "location_value",
                                    },
                                    "parameters": {"fields": {}},
                                }
                            ],
                            "inherit_from_parent": True,
                            "reset": True,
                        },
                        "alternate": {"launch": "launch_value", "spec": {}},
                        "dry_run_spec": {},
                        "etag": "etag_value",
                    },
                }
            ],
            "custom_constraints": [
                {
                    "custom_constraint_parent": "custom_constraint_parent_value",
                    "custom_constraint": {
                        "name": "name_value",
                        "resource_types": [
                            "resource_types_value1",
                            "resource_types_value2",
                        ],
                        "method_types": [1],
                        "condition": "condition_value",
                        "action_type": 1,
                        "display_name": "display_name_value",
                        "description": "description_value",
                        "update_time": {},
                    },
                }
            ],
        },
        "violations_count": 1744,
        "resource_counts": {
            "scanned": 732,
            "noncompliant": 1298,
            "compliant": 967,
            "unenforced": 1065,
            "errors": 669,
        },
        "custom_constraints": [
            "custom_constraints_value1",
            "custom_constraints_value2",
        ],
        "create_time": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest.meta.fields[
        "org_policy_violations_preview"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "org_policy_violations_preview"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(
                    0, len(request_init["org_policy_violations_preview"][field])
                ):
                    del request_init["org_policy_violations_preview"][field][i][
                        subfield
                    ]
            else:
                del request_init["org_policy_violations_preview"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.create_org_policy_violations_preview(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_org_policy_violations_preview_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyViolationsPreviewServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OrgPolicyViolationsPreviewServiceRestInterceptor(),
    )
    client = OrgPolicyViolationsPreviewServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "post_create_org_policy_violations_preview",
    ) as post, mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "post_create_org_policy_violations_preview_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "pre_create_org_policy_violations_preview",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest.pb(
            gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = json_format.MessageToJson(operations_pb2.Operation())
        req.return_value.content = return_value

        request = gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.create_org_policy_violations_preview(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_org_policy_violations_rest_bad_request(
    request_type=gcp_orgpolicy.ListOrgPolicyViolationsRequest,
):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "organizations/sample1/locations/sample2/orgPolicyViolationsPreviews/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_org_policy_violations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gcp_orgpolicy.ListOrgPolicyViolationsRequest,
        dict,
    ],
)
def test_list_org_policy_violations_rest_call_success(request_type):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "organizations/sample1/locations/sample2/orgPolicyViolationsPreviews/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_org_policy_violations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOrgPolicyViolationsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_org_policy_violations_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyViolationsPreviewServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OrgPolicyViolationsPreviewServiceRestInterceptor(),
    )
    client = OrgPolicyViolationsPreviewServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "post_list_org_policy_violations",
    ) as post, mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "post_list_org_policy_violations_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceRestInterceptor,
        "pre_list_org_policy_violations",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = gcp_orgpolicy.ListOrgPolicyViolationsRequest.pb(
            gcp_orgpolicy.ListOrgPolicyViolationsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse.to_json(
            gcp_orgpolicy.ListOrgPolicyViolationsResponse()
        )
        req.return_value.content = return_value

        request = gcp_orgpolicy.ListOrgPolicyViolationsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcp_orgpolicy.ListOrgPolicyViolationsResponse()
        post_with_metadata.return_value = (
            gcp_orgpolicy.ListOrgPolicyViolationsResponse(),
            metadata,
        )

        client.list_org_policy_violations(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_operation_rest_bad_request(
    request_type=operations_pb2.GetOperationRequest,
):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict({"name": "operations/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "operations/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    request_type=operations_pb2.ListOperationsRequest,
):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict({"name": "operations"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "operations"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_initialize_client_w_rest():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_org_policy_violations_previews_empty_call_rest():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations_previews), "__call__"
    ) as call:
        client.list_org_policy_violations_previews(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.ListOrgPolicyViolationsPreviewsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_org_policy_violations_preview_empty_call_rest():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_org_policy_violations_preview), "__call__"
    ) as call:
        client.get_org_policy_violations_preview(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.GetOrgPolicyViolationsPreviewRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_org_policy_violations_preview_empty_call_rest():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_org_policy_violations_preview), "__call__"
    ) as call:
        client.create_org_policy_violations_preview(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.CreateOrgPolicyViolationsPreviewRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_org_policy_violations_empty_call_rest():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_policy_violations), "__call__"
    ) as call:
        client.list_org_policy_violations(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcp_orgpolicy.ListOrgPolicyViolationsRequest()

        assert args[0] == request_msg


def test_org_policy_violations_preview_service_rest_lro_client():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    transport = client.transport

    # Ensure that we have an api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
    )


def test_org_policy_violations_preview_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.OrgPolicyViolationsPreviewServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_org_policy_violations_preview_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.policysimulator_v1.services.org_policy_violations_preview_service.transports.OrgPolicyViolationsPreviewServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.OrgPolicyViolationsPreviewServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_org_policy_violations_previews",
        "get_org_policy_violations_preview",
        "create_org_policy_violations_preview",
        "list_org_policy_violations",
        "get_operation",
        "list_operations",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_org_policy_violations_preview_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.policysimulator_v1.services.org_policy_violations_preview_service.transports.OrgPolicyViolationsPreviewServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OrgPolicyViolationsPreviewServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_org_policy_violations_preview_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.policysimulator_v1.services.org_policy_violations_preview_service.transports.OrgPolicyViolationsPreviewServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OrgPolicyViolationsPreviewServiceTransport()
        adc.assert_called_once()


def test_org_policy_violations_preview_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        OrgPolicyViolationsPreviewServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
        transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
    ],
)
def test_org_policy_violations_preview_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
        transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
        transports.OrgPolicyViolationsPreviewServiceRestTransport,
    ],
)
def test_org_policy_violations_preview_service_transport_auth_gdch_credentials(
    transport_class,
):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.OrgPolicyViolationsPreviewServiceGrpcTransport, grpc_helpers),
        (
            transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
            grpc_helpers_async,
        ),
    ],
)
def test_org_policy_violations_preview_service_transport_create_channel(
    transport_class, grpc_helpers
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "policysimulator.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="policysimulator.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
        transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
    ],
)
def test_org_policy_violations_preview_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_org_policy_violations_preview_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.OrgPolicyViolationsPreviewServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_org_policy_violations_preview_service_host_no_port(transport_name):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="policysimulator.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "policysimulator.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://policysimulator.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_org_policy_violations_preview_service_host_with_port(transport_name):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="policysimulator.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "policysimulator.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://policysimulator.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_org_policy_violations_preview_service_client_transport_session_collision(
    transport_name,
):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = OrgPolicyViolationsPreviewServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = OrgPolicyViolationsPreviewServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_org_policy_violations_previews._session
    session2 = client2.transport.list_org_policy_violations_previews._session
    assert session1 != session2
    session1 = client1.transport.get_org_policy_violations_preview._session
    session2 = client2.transport.get_org_policy_violations_preview._session
    assert session1 != session2
    session1 = client1.transport.create_org_policy_violations_preview._session
    session2 = client2.transport.create_org_policy_violations_preview._session
    assert session1 != session2
    session1 = client1.transport.list_org_policy_violations._session
    session2 = client2.transport.list_org_policy_violations._session
    assert session1 != session2


def test_org_policy_violations_preview_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OrgPolicyViolationsPreviewServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_org_policy_violations_preview_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
        transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
    ],
)
def test_org_policy_violations_preview_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
        transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
    ],
)
def test_org_policy_violations_preview_service_transport_channel_mtls_with_adc(
    transport_class,
):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_org_policy_violations_preview_service_grpc_lro_client():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_org_policy_violations_preview_service_grpc_lro_async_client():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_custom_constraint_path():
    organization = "squid"
    custom_constraint = "clam"
    expected = (
        "organizations/{organization}/customConstraints/{custom_constraint}".format(
            organization=organization,
            custom_constraint=custom_constraint,
        )
    )
    actual = OrgPolicyViolationsPreviewServiceClient.custom_constraint_path(
        organization, custom_constraint
    )
    assert expected == actual


def test_parse_custom_constraint_path():
    expected = {
        "organization": "whelk",
        "custom_constraint": "octopus",
    }
    path = OrgPolicyViolationsPreviewServiceClient.custom_constraint_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyViolationsPreviewServiceClient.parse_custom_constraint_path(path)
    assert expected == actual


def test_org_policy_violation_path():
    organization = "oyster"
    location = "nudibranch"
    org_policy_violations_preview = "cuttlefish"
    org_policy_violation = "mussel"
    expected = "organizations/{organization}/locations/{location}/orgPolicyViolationsPreviews/{org_policy_violations_preview}/orgPolicyViolations/{org_policy_violation}".format(
        organization=organization,
        location=location,
        org_policy_violations_preview=org_policy_violations_preview,
        org_policy_violation=org_policy_violation,
    )
    actual = OrgPolicyViolationsPreviewServiceClient.org_policy_violation_path(
        organization, location, org_policy_violations_preview, org_policy_violation
    )
    assert expected == actual


def test_parse_org_policy_violation_path():
    expected = {
        "organization": "winkle",
        "location": "nautilus",
        "org_policy_violations_preview": "scallop",
        "org_policy_violation": "abalone",
    }
    path = OrgPolicyViolationsPreviewServiceClient.org_policy_violation_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyViolationsPreviewServiceClient.parse_org_policy_violation_path(
        path
    )
    assert expected == actual


def test_org_policy_violations_preview_path():
    organization = "squid"
    location = "clam"
    org_policy_violations_preview = "whelk"
    expected = "organizations/{organization}/locations/{location}/orgPolicyViolationsPreviews/{org_policy_violations_preview}".format(
        organization=organization,
        location=location,
        org_policy_violations_preview=org_policy_violations_preview,
    )
    actual = OrgPolicyViolationsPreviewServiceClient.org_policy_violations_preview_path(
        organization, location, org_policy_violations_preview
    )
    assert expected == actual


def test_parse_org_policy_violations_preview_path():
    expected = {
        "organization": "octopus",
        "location": "oyster",
        "org_policy_violations_preview": "nudibranch",
    }
    path = OrgPolicyViolationsPreviewServiceClient.org_policy_violations_preview_path(
        **expected
    )

    # Check that the path construction is reversible.
    actual = OrgPolicyViolationsPreviewServiceClient.parse_org_policy_violations_preview_path(
        path
    )
    assert expected == actual


def test_policy_path():
    project = "cuttlefish"
    policy = "mussel"
    expected = "projects/{project}/policies/{policy}".format(
        project=project,
        policy=policy,
    )
    actual = OrgPolicyViolationsPreviewServiceClient.policy_path(project, policy)
    assert expected == actual


def test_parse_policy_path():
    expected = {
        "project": "winkle",
        "policy": "nautilus",
    }
    path = OrgPolicyViolationsPreviewServiceClient.policy_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyViolationsPreviewServiceClient.parse_policy_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = OrgPolicyViolationsPreviewServiceClient.common_billing_account_path(
        billing_account
    )
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = OrgPolicyViolationsPreviewServiceClient.common_billing_account_path(
        **expected
    )

    # Check that the path construction is reversible.
    actual = OrgPolicyViolationsPreviewServiceClient.parse_common_billing_account_path(
        path
    )
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = OrgPolicyViolationsPreviewServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = OrgPolicyViolationsPreviewServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyViolationsPreviewServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = OrgPolicyViolationsPreviewServiceClient.common_organization_path(
        organization
    )
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = OrgPolicyViolationsPreviewServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyViolationsPreviewServiceClient.parse_common_organization_path(
        path
    )
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = OrgPolicyViolationsPreviewServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = OrgPolicyViolationsPreviewServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyViolationsPreviewServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = OrgPolicyViolationsPreviewServiceClient.common_location_path(
        project, location
    )
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = OrgPolicyViolationsPreviewServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyViolationsPreviewServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = OrgPolicyViolationsPreviewServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.OrgPolicyViolationsPreviewServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = OrgPolicyViolationsPreviewServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_get_operation(transport: str = "grpc"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc_asyncio"):
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc_asyncio"):
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_operations_from_dict():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_transport_close_grpc():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


@pytest.mark.asyncio
async def test_transport_close_grpc_asyncio():
    client = OrgPolicyViolationsPreviewServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close_rest():
    client = OrgPolicyViolationsPreviewServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_session")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = OrgPolicyViolationsPreviewServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (
            OrgPolicyViolationsPreviewServiceClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcTransport,
        ),
        (
            OrgPolicyViolationsPreviewServiceAsyncClient,
            transports.OrgPolicyViolationsPreviewServiceGrpcAsyncIOTransport,
        ),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

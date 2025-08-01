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
from google.cloud.container_v1beta1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.cluster_manager import ClusterManagerAsyncClient, ClusterManagerClient
from .types.cluster_service import (
    AcceleratorConfig,
    AdditionalIPRangesConfig,
    AdditionalNodeNetworkConfig,
    AdditionalPodNetworkConfig,
    AdditionalPodRangesConfig,
    AddonsConfig,
    AdvancedDatapathObservabilityConfig,
    AdvancedMachineFeatures,
    AnonymousAuthenticationConfig,
    AuthenticatorGroupsConfig,
    AutoIpamConfig,
    AutoMonitoringConfig,
    Autopilot,
    AutopilotCompatibilityIssue,
    AutopilotConversionStatus,
    AutoprovisioningNodePoolDefaults,
    AutoUpgradeOptions,
    BestEffortProvisioning,
    BinaryAuthorization,
    BlueGreenSettings,
    BootDisk,
    CancelOperationRequest,
    CheckAutopilotCompatibilityRequest,
    CheckAutopilotCompatibilityResponse,
    ClientCertificateConfig,
    CloudRunConfig,
    Cluster,
    ClusterAutoscaling,
    ClusterTelemetry,
    ClusterUpdate,
    ClusterUpgradeInfo,
    CompleteIPRotationRequest,
    CompleteNodePoolUpgradeRequest,
    CompliancePostureConfig,
    ConfidentialNodes,
    ConfigConnectorConfig,
    ContainerdConfig,
    ControlPlaneEndpointsConfig,
    CostManagementConfig,
    CreateClusterRequest,
    CreateNodePoolRequest,
    DailyMaintenanceWindow,
    DatabaseEncryption,
    DatapathProvider,
    DefaultComputeClassConfig,
    DefaultSnatStatus,
    DeleteClusterRequest,
    DeleteNodePoolRequest,
    DesiredAdditionalIPRangesConfig,
    DesiredEnterpriseConfig,
    DnsCacheConfig,
    DNSConfig,
    EnterpriseConfig,
    EphemeralStorageConfig,
    EphemeralStorageLocalSsdConfig,
    EvictionGracePeriod,
    EvictionMinimumReclaim,
    EvictionSignals,
    FastSocket,
    FetchClusterUpgradeInfoRequest,
    FetchNodePoolUpgradeInfoRequest,
    Fleet,
    GatewayAPIConfig,
    GcePersistentDiskCsiDriverConfig,
    GcfsConfig,
    GcpFilestoreCsiDriverConfig,
    GcsFuseCsiDriverConfig,
    GetClusterRequest,
    GetJSONWebKeysRequest,
    GetJSONWebKeysResponse,
    GetNodePoolRequest,
    GetOpenIDConfigRequest,
    GetOpenIDConfigResponse,
    GetOperationRequest,
    GetServerConfigRequest,
    GkeAutoUpgradeConfig,
    GkeBackupAgentConfig,
    GPUDriverInstallationConfig,
    GPUSharingConfig,
    HighScaleCheckpointingConfig,
    HorizontalPodAutoscaling,
    HostMaintenancePolicy,
    HttpLoadBalancing,
    IdentityServiceConfig,
    ILBSubsettingConfig,
    IntraNodeVisibilityConfig,
    InTransitEncryptionConfig,
    IPAllocationPolicy,
    IstioConfig,
    Jwk,
    K8sBetaAPIConfig,
    KalmConfig,
    KubernetesDashboard,
    LegacyAbac,
    LinuxNodeConfig,
    ListClustersRequest,
    ListClustersResponse,
    ListLocationsRequest,
    ListLocationsResponse,
    ListNodePoolsRequest,
    ListNodePoolsResponse,
    ListOperationsRequest,
    ListOperationsResponse,
    ListUsableSubnetworksRequest,
    ListUsableSubnetworksResponse,
    LocalNvmeSsdBlockConfig,
    Location,
    LoggingComponentConfig,
    LoggingConfig,
    LoggingVariantConfig,
    LustreCsiDriverConfig,
    MaintenanceExclusionOptions,
    MaintenancePolicy,
    MaintenanceWindow,
    ManagedPrometheusConfig,
    Master,
    MasterAuth,
    MasterAuthorizedNetworksConfig,
    MaxPodsConstraint,
    MemoryManager,
    MeshCertificates,
    MonitoringComponentConfig,
    MonitoringConfig,
    NetworkConfig,
    NetworkPolicy,
    NetworkPolicyConfig,
    NetworkTags,
    NodeConfig,
    NodeConfigDefaults,
    NodeKubeletConfig,
    NodeLabels,
    NodeManagement,
    NodeNetworkConfig,
    NodePool,
    NodePoolAutoConfig,
    NodePoolAutoscaling,
    NodePoolDefaults,
    NodePoolLoggingConfig,
    NodePoolUpdateStrategy,
    NodePoolUpgradeInfo,
    NodeTaint,
    NodeTaints,
    NotificationConfig,
    Operation,
    OperationProgress,
    ParallelstoreCsiDriverConfig,
    PodAutoscaling,
    PodCIDROverprovisionConfig,
    PodSecurityPolicyConfig,
    PrivateClusterConfig,
    PrivateClusterMasterGlobalAccessConfig,
    PrivateIPv6GoogleAccess,
    ProtectConfig,
    RangeInfo,
    RayClusterLoggingConfig,
    RayClusterMonitoringConfig,
    RayOperatorConfig,
    RBACBindingConfig,
    RecurringTimeWindow,
    ReleaseChannel,
    ReservationAffinity,
    ResourceLabels,
    ResourceLimit,
    ResourceManagerTags,
    ResourceUsageExportConfig,
    RollbackNodePoolUpgradeRequest,
    SandboxConfig,
    SecondaryBootDisk,
    SecondaryBootDiskUpdateStrategy,
    SecretManagerConfig,
    SecurityBulletinEvent,
    SecurityPostureConfig,
    ServerConfig,
    ServiceExternalIPsConfig,
    SetAddonsConfigRequest,
    SetLabelsRequest,
    SetLegacyAbacRequest,
    SetLocationsRequest,
    SetLoggingServiceRequest,
    SetMaintenancePolicyRequest,
    SetMasterAuthRequest,
    SetMonitoringServiceRequest,
    SetNetworkPolicyRequest,
    SetNodePoolAutoscalingRequest,
    SetNodePoolManagementRequest,
    SetNodePoolSizeRequest,
    ShieldedInstanceConfig,
    ShieldedNodes,
    SoleTenantConfig,
    StackType,
    StartIPRotationRequest,
    StatefulHAConfig,
    StatusCondition,
    TimeWindow,
    TopologyManager,
    TpuConfig,
    UpdateClusterRequest,
    UpdateMasterRequest,
    UpdateNodePoolRequest,
    UpgradeAvailableEvent,
    UpgradeDetails,
    UpgradeEvent,
    UpgradeInfoEvent,
    UpgradeResourceType,
    UsableSubnetwork,
    UsableSubnetworkSecondaryRange,
    UserManagedKeysConfig,
    VerticalPodAutoscaling,
    VirtualNIC,
    WindowsNodeConfig,
    WindowsVersions,
    WorkloadALTSConfig,
    WorkloadCertificates,
    WorkloadConfig,
    WorkloadIdentityConfig,
    WorkloadMetadataConfig,
    WorkloadPolicyConfig,
)

__all__ = (
    "ClusterManagerAsyncClient",
    "AcceleratorConfig",
    "AdditionalIPRangesConfig",
    "AdditionalNodeNetworkConfig",
    "AdditionalPodNetworkConfig",
    "AdditionalPodRangesConfig",
    "AddonsConfig",
    "AdvancedDatapathObservabilityConfig",
    "AdvancedMachineFeatures",
    "AnonymousAuthenticationConfig",
    "AuthenticatorGroupsConfig",
    "AutoIpamConfig",
    "AutoMonitoringConfig",
    "AutoUpgradeOptions",
    "Autopilot",
    "AutopilotCompatibilityIssue",
    "AutopilotConversionStatus",
    "AutoprovisioningNodePoolDefaults",
    "BestEffortProvisioning",
    "BinaryAuthorization",
    "BlueGreenSettings",
    "BootDisk",
    "CancelOperationRequest",
    "CheckAutopilotCompatibilityRequest",
    "CheckAutopilotCompatibilityResponse",
    "ClientCertificateConfig",
    "CloudRunConfig",
    "Cluster",
    "ClusterAutoscaling",
    "ClusterManagerClient",
    "ClusterTelemetry",
    "ClusterUpdate",
    "ClusterUpgradeInfo",
    "CompleteIPRotationRequest",
    "CompleteNodePoolUpgradeRequest",
    "CompliancePostureConfig",
    "ConfidentialNodes",
    "ConfigConnectorConfig",
    "ContainerdConfig",
    "ControlPlaneEndpointsConfig",
    "CostManagementConfig",
    "CreateClusterRequest",
    "CreateNodePoolRequest",
    "DNSConfig",
    "DailyMaintenanceWindow",
    "DatabaseEncryption",
    "DatapathProvider",
    "DefaultComputeClassConfig",
    "DefaultSnatStatus",
    "DeleteClusterRequest",
    "DeleteNodePoolRequest",
    "DesiredAdditionalIPRangesConfig",
    "DesiredEnterpriseConfig",
    "DnsCacheConfig",
    "EnterpriseConfig",
    "EphemeralStorageConfig",
    "EphemeralStorageLocalSsdConfig",
    "EvictionGracePeriod",
    "EvictionMinimumReclaim",
    "EvictionSignals",
    "FastSocket",
    "FetchClusterUpgradeInfoRequest",
    "FetchNodePoolUpgradeInfoRequest",
    "Fleet",
    "GPUDriverInstallationConfig",
    "GPUSharingConfig",
    "GatewayAPIConfig",
    "GcePersistentDiskCsiDriverConfig",
    "GcfsConfig",
    "GcpFilestoreCsiDriverConfig",
    "GcsFuseCsiDriverConfig",
    "GetClusterRequest",
    "GetJSONWebKeysRequest",
    "GetJSONWebKeysResponse",
    "GetNodePoolRequest",
    "GetOpenIDConfigRequest",
    "GetOpenIDConfigResponse",
    "GetOperationRequest",
    "GetServerConfigRequest",
    "GkeAutoUpgradeConfig",
    "GkeBackupAgentConfig",
    "HighScaleCheckpointingConfig",
    "HorizontalPodAutoscaling",
    "HostMaintenancePolicy",
    "HttpLoadBalancing",
    "ILBSubsettingConfig",
    "IPAllocationPolicy",
    "IdentityServiceConfig",
    "InTransitEncryptionConfig",
    "IntraNodeVisibilityConfig",
    "IstioConfig",
    "Jwk",
    "K8sBetaAPIConfig",
    "KalmConfig",
    "KubernetesDashboard",
    "LegacyAbac",
    "LinuxNodeConfig",
    "ListClustersRequest",
    "ListClustersResponse",
    "ListLocationsRequest",
    "ListLocationsResponse",
    "ListNodePoolsRequest",
    "ListNodePoolsResponse",
    "ListOperationsRequest",
    "ListOperationsResponse",
    "ListUsableSubnetworksRequest",
    "ListUsableSubnetworksResponse",
    "LocalNvmeSsdBlockConfig",
    "Location",
    "LoggingComponentConfig",
    "LoggingConfig",
    "LoggingVariantConfig",
    "LustreCsiDriverConfig",
    "MaintenanceExclusionOptions",
    "MaintenancePolicy",
    "MaintenanceWindow",
    "ManagedPrometheusConfig",
    "Master",
    "MasterAuth",
    "MasterAuthorizedNetworksConfig",
    "MaxPodsConstraint",
    "MemoryManager",
    "MeshCertificates",
    "MonitoringComponentConfig",
    "MonitoringConfig",
    "NetworkConfig",
    "NetworkPolicy",
    "NetworkPolicyConfig",
    "NetworkTags",
    "NodeConfig",
    "NodeConfigDefaults",
    "NodeKubeletConfig",
    "NodeLabels",
    "NodeManagement",
    "NodeNetworkConfig",
    "NodePool",
    "NodePoolAutoConfig",
    "NodePoolAutoscaling",
    "NodePoolDefaults",
    "NodePoolLoggingConfig",
    "NodePoolUpdateStrategy",
    "NodePoolUpgradeInfo",
    "NodeTaint",
    "NodeTaints",
    "NotificationConfig",
    "Operation",
    "OperationProgress",
    "ParallelstoreCsiDriverConfig",
    "PodAutoscaling",
    "PodCIDROverprovisionConfig",
    "PodSecurityPolicyConfig",
    "PrivateClusterConfig",
    "PrivateClusterMasterGlobalAccessConfig",
    "PrivateIPv6GoogleAccess",
    "ProtectConfig",
    "RBACBindingConfig",
    "RangeInfo",
    "RayClusterLoggingConfig",
    "RayClusterMonitoringConfig",
    "RayOperatorConfig",
    "RecurringTimeWindow",
    "ReleaseChannel",
    "ReservationAffinity",
    "ResourceLabels",
    "ResourceLimit",
    "ResourceManagerTags",
    "ResourceUsageExportConfig",
    "RollbackNodePoolUpgradeRequest",
    "SandboxConfig",
    "SecondaryBootDisk",
    "SecondaryBootDiskUpdateStrategy",
    "SecretManagerConfig",
    "SecurityBulletinEvent",
    "SecurityPostureConfig",
    "ServerConfig",
    "ServiceExternalIPsConfig",
    "SetAddonsConfigRequest",
    "SetLabelsRequest",
    "SetLegacyAbacRequest",
    "SetLocationsRequest",
    "SetLoggingServiceRequest",
    "SetMaintenancePolicyRequest",
    "SetMasterAuthRequest",
    "SetMonitoringServiceRequest",
    "SetNetworkPolicyRequest",
    "SetNodePoolAutoscalingRequest",
    "SetNodePoolManagementRequest",
    "SetNodePoolSizeRequest",
    "ShieldedInstanceConfig",
    "ShieldedNodes",
    "SoleTenantConfig",
    "StackType",
    "StartIPRotationRequest",
    "StatefulHAConfig",
    "StatusCondition",
    "TimeWindow",
    "TopologyManager",
    "TpuConfig",
    "UpdateClusterRequest",
    "UpdateMasterRequest",
    "UpdateNodePoolRequest",
    "UpgradeAvailableEvent",
    "UpgradeDetails",
    "UpgradeEvent",
    "UpgradeInfoEvent",
    "UpgradeResourceType",
    "UsableSubnetwork",
    "UsableSubnetworkSecondaryRange",
    "UserManagedKeysConfig",
    "VerticalPodAutoscaling",
    "VirtualNIC",
    "WindowsNodeConfig",
    "WindowsVersions",
    "WorkloadALTSConfig",
    "WorkloadCertificates",
    "WorkloadConfig",
    "WorkloadIdentityConfig",
    "WorkloadMetadataConfig",
    "WorkloadPolicyConfig",
)

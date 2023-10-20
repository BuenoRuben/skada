from .base import BaseAdapter, DomainAwareEstimator
# from ._mapping import (
#     ClassRegularizerOTMapping,
#     CORAL,
#     EntropicOTMapping,
#     LinearOTMapping,
#     OTMapping,
# )
from ._reweight import (
    DiscriminatorReweightDensity,
    DiscriminatorReweightDensityAdapter,
    GaussianReweightDensity,
    GaussianReweightDensityAdapter,
    KLIEP,
    KLIEPAdapter,
    ReweightDensity,
    ReweightDensityAdapter,
)
from ._subspace import (
    SubspaceAlignment,
    SubspaceAlignmentAdapter,
    TransferComponentAnalysis,
    TransferComponentAnalysisAdapter,
)
# from ._pipeline import DAPipeline


__all__ = [
    "BaseAdapter",
    "DomainAwareEstimator",

    # "ClassRegularizerOTMapping",
    # "CORAL",
    # "EntropicOTMapping",
    # "LinearOTMapping",
    # "OTMapping",

    "DiscriminatorReweightDensity",
    "DiscriminatorReweightDensityAdapter",
    "GaussianReweightDensity",
    "GaussianReweightDensityAdapter",
    "KLIEP",
    "KLIEPAdapter",
    "ReweightDensity",
    "ReweightDensityAdapter",

    "SubspaceAlignment",
    "SubspaceAlignmentAdapter",
    "TransferComponentAnalysis",
    "TransferComponentAnalysisAdapter",

    # "DAPipeline",
]

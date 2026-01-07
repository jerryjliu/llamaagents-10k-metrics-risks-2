"""
Configuration for SEC 10-K filing extraction.

Extracts key financial metrics and risk factors from annual reports.
"""

from __future__ import annotations

from llama_cloud import ExtractConfig
from llama_cloud_services.extract import ExtractMode
from pydantic import BaseModel, Field


EXTRACTED_DATA_COLLECTION: str = "sec-10k-filings"


class RiskFactor(BaseModel):
    """A specific risk factor disclosed in the 10-K filing."""

    category: str | None = Field(
        default=None,
        description="Risk category (e.g., 'Market Risk', 'Operational Risk', 'Regulatory Risk', 'Financial Risk', 'Cybersecurity Risk', 'Competition Risk')",
    )
    title: str | None = Field(
        default=None,
        description="Brief title or headline of the risk factor",
    )
    description: str | None = Field(
        default=None,
        description="Detailed description of the risk and its potential impact on the business",
    )


class FinancialMetrics(BaseModel):
    """Key financial metrics from the 10-K filing."""

    total_revenue: str | None = Field(
        default=None,
        description="Total revenue/net sales for the fiscal year (include currency and units, e.g., '$50.5 billion')",
    )
    net_income: str | None = Field(
        default=None,
        description="Net income/net earnings for the fiscal year (include currency and units)",
    )
    total_assets: str | None = Field(
        default=None,
        description="Total assets as of fiscal year end (include currency and units)",
    )
    total_liabilities: str | None = Field(
        default=None,
        description="Total liabilities as of fiscal year end (include currency and units)",
    )
    shareholders_equity: str | None = Field(
        default=None,
        description="Total stockholders'/shareholders' equity (include currency and units)",
    )
    earnings_per_share: str | None = Field(
        default=None,
        description="Basic earnings per share for the fiscal year",
    )
    operating_income: str | None = Field(
        default=None,
        description="Operating income/income from operations (include currency and units)",
    )
    cash_and_equivalents: str | None = Field(
        default=None,
        description="Cash and cash equivalents as of fiscal year end (include currency and units)",
    )


class ExtractionSchema(BaseModel):
    """Schema for extracting key information from SEC 10-K filings."""

    company_name: str | None = Field(
        default=None,
        description="Full legal name of the company",
    )
    ticker_symbol: str | None = Field(
        default=None,
        description="Stock ticker symbol (e.g., 'AAPL', 'MSFT')",
    )
    cik_number: str | None = Field(
        default=None,
        description="SEC Central Index Key (CIK) number",
    )
    fiscal_year_end: str | None = Field(
        default=None,
        description="Fiscal year end date covered by this 10-K (e.g., 'December 31, 2024')",
    )
    industry: str | None = Field(
        default=None,
        description="Primary industry or business sector",
    )
    business_description: str | None = Field(
        default=None,
        description="Brief 2-3 sentence summary of the company's primary business operations",
    )
    financial_metrics: FinancialMetrics | None = Field(
        default=None,
        description="Key financial metrics from the consolidated financial statements",
    )
    risk_factors: list[RiskFactor] | None = Field(
        default=None,
        description="Top risk factors disclosed in Item 1A of the 10-K, limited to the 10 most significant risks",
    )
    key_developments: list[str] | None = Field(
        default=None,
        description="Notable business developments, acquisitions, or strategic changes mentioned in the filing",
    )


EXTRACT_CONFIG = ExtractConfig(
    extraction_mode=ExtractMode.PREMIUM,
    system_prompt="Extract key financial metrics and risk factors from this SEC 10-K annual report filing. Focus on quantitative data from the financial statements and the most material risk factors from Item 1A.",
    use_reasoning=True,
    cite_sources=True,
    confidence_scores=True,
)

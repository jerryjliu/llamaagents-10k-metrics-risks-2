"""
Tests for SEC 10-K filing extraction workflow.
"""

import pytest
import uuid
import os
import jsonref

from unittest.mock import patch
from extraction_review.config import ExtractionSchema, EXTRACTED_DATA_COLLECTION
from extraction_review.process_file import workflow as process_file_workflow
from extraction_review.process_file import FileEvent
from workflows.events import StartEvent
from extraction_review.metadata_workflow import workflow as metadata_workflow
from extraction_review.metadata_workflow import MetadataResponse


@pytest.mark.asyncio
@patch.dict(
    os.environ, {"LLAMA_CLOUD_API_KEY": "test-api-key"}
)
async def test_process_file_workflow() -> None:
    """Test that the 10-K extraction workflow processes a file and returns an agent data ID."""
    file_id = str(uuid.uuid4())
    result = await process_file_workflow.run(start_event=FileEvent(file_id=file_id))
    assert result is not None
    assert isinstance(result, str)
    assert len(result) == 7


@pytest.mark.asyncio
async def test_metadata_workflow() -> None:
    """Test that the metadata workflow returns the correct schema and collection name."""
    result = await metadata_workflow.run(start_event=StartEvent())
    assert isinstance(result, MetadataResponse)
    assert result.extracted_data_collection == EXTRACTED_DATA_COLLECTION
    expected_schema = jsonref.replace_refs(
        ExtractionSchema.model_json_schema(), proxies=False
    )
    assert result.json_schema == expected_schema

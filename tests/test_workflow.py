"""
<system>
This is an example test, based on a SEC filings use case. 
Adapt the test to your use case following the guidelines below.
</system>
<guidelines>
You can read and modify this file. 
Here are your editing permissions, which you **MUST ALWAYS** follow:

- Lines and blocks tagged with `<edit></edit>` should be ALWAYS modified to something different, based on the use case.
- Lines and blocks tagged with `<adapt></adapt>` should be adapted to the specific use case you are dealing with, but only if needed.
- If something does not have tags, it **MUST NOT** be modified.
</guidelines>
"""

import pytest
import uuid
import os

from unittest.mock import patch
# <edit>
from extraction_review.config import ExtractionSchema, EXTRACTED_DATA_COLLECTION
from extraction_review.process_file import workflow as process_file_workflow
from extraction_review.process_file import FileEvent
from workflows.events import StartEvent
from extraction_review.metadata_workflow import workflow as metadata_workflow
from extraction_review.metadata_workflow import MetadataResponse
# </edit>

@pytest.mark.asyncio
@patch.dict(
    os.environ, {"LLAMA_CLOUD_API_KEY": "test-api-key"}
)
# <adapt>
async def test_process_file_workflow() -> None:
    # load a file to the mock LlamaCloud server and retrieve its file id (modify if you don't have any files to load as input)
    file_id = str(uuid.uuid4())
    try:
        result = await process_file_workflow.run(start_event=FileEvent(file_id=file_id))
    except Exception:
        result = None
    assert result is not None
    # all generated agent data IDs are alphanumeric strings with 7 characters
    # the following assert statements ensure that that is the case
    assert isinstance(result, str)
    assert len(result) == 7 
# </adapt>

# <adapt>
@pytest.mark.asyncio
async def test_metadata_workflow() -> None:
    result = await metadata_workflow.run(start_event=StartEvent())
    assert isinstance(result, MetadataResponse)
    assert result.extracted_data_collection == EXTRACTED_DATA_COLLECTION
    assert result.json_schema == ExtractionSchema.model_json_schema()
# </adapt>
import logging
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File

logger = logging.getLogger(__name__)


class PdfToolsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        file: File | None = tool_parameters.get("pdf_file")
        logger.error("file {} type is {} mime type is {}".format(file, file.type, file.mime_type))
        pdf_binary = file.blob
        yield self.create_json_message({
            "result": "Hello, world!"
        })

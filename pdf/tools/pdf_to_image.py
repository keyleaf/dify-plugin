import io
import logging
from collections.abc import Generator
from pathlib import Path
from typing import Any, List
from PIL import Image

import pdf2image
from unstructured.partition.common.common import convert_to_bytes
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File

logger = logging.getLogger(__name__)


class PdfToImageTool(Tool):
    def _invoke(
            self,
            tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        file: File | None = tool_parameters.get("pdf_file")

        logger.error("file {} type is {} mime type is {}".format(file, file.type, file.mime_type))

        if file.mime_type != "application/pdf":
            yield self.create_text_message("not a valid pdf file")
        try:
            pdf_binary = io.BytesIO(file.blob)
            f_bytes = convert_to_bytes(pdf_binary)
            images: List[Image.Image] | None = list(pdf2image.convert_from_bytes(f_bytes, fmt="jpg", output_folder="./pdf_to_images"))
            for image in images:
                image_file = Path(image.filename).read_bytes()
                yield self.create_blob_message(image_file, meta={'mime_type': 'image/jpeg'})
        except Exception as e:
            yield self.create_text_message(f"Failed to extract result, error: {str(e)}")

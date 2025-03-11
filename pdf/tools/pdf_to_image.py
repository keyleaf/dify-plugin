import io
import logging
from collections.abc import Generator
from pathlib import Path
from typing import Any, Optional

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
        # file = tool_parameters.get("pdf_file")

        logger.error("file {} type is {} mime type is {}".format(file, file.type, file.mime_type))
        if file.mime_type != "application/pdf":  # type: ignore
            yield self.create_text_message("not a valid pdf file")
            return
        #       将pdf拆分成图片并返回图片路径列表

        # data = self.session.storage.get(file.filename)
        # data = self.session.file

        config = self.runtime.json
        # file.url = "http://localhost" + file.url
        pdf_binary = io.BytesIO(file.blob)

        # file_key = "upload_files/" + ("f7beda2f-11a2-453a-a837-e17d099e60f2" or "") + "/" + "3a388f77-2710-4176-9194-0b6e34229374.pdf"
        # file_key = "upload_files/f7beda2f-11a2-453a-a837-e17d099e60f2/dcdbd4e9-78fb-4dfd-ab84-7b6db0a524cc.pdf"
        # logger.error("file_key is {}".format(config))
        # pdf_binary = self.session.storage.get(file_key)

        f_bytes = convert_to_bytes(pdf_binary)
        # images = list(pdf2image.convert_from_bytes(f_bytes, fmt="jpg", output_folder="/app/api/storage/pdf_to_images"))
        images = list(pdf2image.convert_from_bytes(f_bytes, fmt="jpg", output_folder="./pdf_to_images"))

        for image in images:
            imageFile = Path(image.filename).read_bytes()
            yield self.create_blob_message(imageFile,
                                           meta={'mime_type': 'image/jpeg'})

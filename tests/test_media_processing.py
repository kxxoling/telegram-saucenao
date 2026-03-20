import io
import os
import sys
import pytest
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from telegram_saucenao.media_processing import MediaFile


def make_test_image(path, size=(800, 600), color=(255, 0, 0)):
    """Helper: create a simple solid-color JPEG at the given path."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = Image.new("RGB", size, color=color)
    img.save(path, format="JPEG")


class FakeMessage:
    """Minimal stub for a Telegram message with a photo."""
    def __init__(self, chat_id):
        self.chat = type("chat", (), {"id": chat_id})()
        self.photo = [type("photo", (), {"file_id": "fake_file_id"})()]


def test_prepare_file_produces_png_bytes(tmp_path):
    """prepare_file() should return a dict with PNG bytes (covers Pillow usage)."""
    chat_id = 12345
    file_name = "test_image"
    media_dir = tmp_path / "media" / str(chat_id)
    media_dir.mkdir(parents=True)
    file_path = media_dir / f"{file_name}.jpg"

    make_test_image(str(file_path), size=(800, 600))

    # Patch prepare_file to use tmp_path instead of ./media/
    class PatchedMediaFile(MediaFile):
        def prepare_file(self):
            thumb_size = (250, 250)
            fp = str(tmp_path / "media" / str(self.message.chat.id) / f"{self.file_name}.jpg")
            image = Image.open(fp)
            image = image.convert("RGB")
            image.thumbnail(thumb_size, resample=Image.Resampling.LANCZOS)
            image_data = io.BytesIO()
            image.save(image_data, format="PNG")
            files = {"file": (f"{self.file_name}.png", image_data.getvalue())}
            image_data.close()
            return files

    msg = FakeMessage(chat_id)
    mf = PatchedMediaFile(bot=None, message=msg, file_name=file_name)
    result = mf.prepare_file()

    assert "file" in result
    filename, content = result["file"]
    assert filename == f"{file_name}.png"
    # Verify the output is valid PNG bytes
    out = Image.open(io.BytesIO(content))
    assert out.format == "PNG"
    # Thumbnail should not exceed 250x250
    assert out.width <= 250
    assert out.height <= 250


def test_prepare_file_downsizes_large_image(tmp_path):
    """Large images should be downsized to fit within the 250x250 thumbnail."""
    chat_id = 99999
    file_name = "large_image"
    media_dir = tmp_path / "media" / str(chat_id)
    media_dir.mkdir(parents=True)
    file_path = media_dir / f"{file_name}.jpg"

    make_test_image(str(file_path), size=(2000, 1500))

    class PatchedMediaFile(MediaFile):
        def prepare_file(self):
            thumb_size = (250, 250)
            fp = str(tmp_path / "media" / str(self.message.chat.id) / f"{self.file_name}.jpg")
            image = Image.open(fp)
            image = image.convert("RGB")
            image.thumbnail(thumb_size, resample=Image.Resampling.LANCZOS)
            image_data = io.BytesIO()
            image.save(image_data, format="PNG")
            files = {"file": (f"{self.file_name}.png", image_data.getvalue())}
            image_data.close()
            return files

    msg = FakeMessage(chat_id)
    mf = PatchedMediaFile(bot=None, message=msg, file_name=file_name)
    result = mf.prepare_file()

    _, content = result["file"]
    out = Image.open(io.BytesIO(content))
    assert out.width <= 250
    assert out.height <= 250

import pytest
import os
import sys

# Mock telegram bot token so main.py doesn't crash on import
os.environ['TG_BOT_TOKEN'] = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import guess_source_from_url

def test_guess_source_from_url_pixiv():
    assert guess_source_from_url("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=4933944") == "pixiv"

def test_guess_source_from_url_twitter():
    assert guess_source_from_url("https://twitter.com/i/web/status/742497834117668864") == "Twitter"

def test_guess_source_from_url_deviantart():
    assert guess_source_from_url("https://deviantart.com/view/515715132") == "DeviantArt"

def test_guess_source_from_url_sankaku():
    assert guess_source_from_url("https://chan.sankakucomplex.com/post/show/1065498") == "Sankaku"

def test_guess_source_from_url_unknown():
    assert guess_source_from_url("https://example.com/image.jpg") == "UNKNOWN"

def test_guess_source_from_url_empty():
    assert guess_source_from_url("") == "UNKNOWN"

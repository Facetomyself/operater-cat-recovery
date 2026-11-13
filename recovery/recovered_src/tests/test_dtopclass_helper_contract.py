from __future__ import annotations


def test_dtopclass_helper_resource_and_action_constants():
    from src.py.com.yun.mao.dclass import DTopClassHelper

    assert DTopClassHelper.RESOURCE_TYPE_PHOTO == "photo"
    assert DTopClassHelper.RESOURCE_TYPE_VIDEO_PHOTO == "video_photo"
    assert DTopClassHelper.RESOURCE_TYPE_VIDEO == "video"
    assert DTopClassHelper.RESOURCE_TYPE_FILE == "file"
    assert DTopClassHelper.RESOURCE_TYPE_TEXT == "text"
    assert DTopClassHelper.ACTION_AUTO == "auto"
    assert DTopClassHelper.ACTION_DOWNLOAD == "download"

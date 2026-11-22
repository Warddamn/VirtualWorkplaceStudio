"""Getting media in: live capture (USB webcam mode, RTMP over Wi-Fi) and SD-card import.

* :mod:`.devices`   what ffmpeg's avfoundation input can see, and picking the camera
* :mod:`.live`      ffmpeg command builders and :class:`~.live.SegmentRecorder`
* :mod:`.network`   the address the camera should stream to
* :mod:`.importer`  camera cards, folders and single files

Submodules are imported on demand (``from videonotes.capture import live``) so that
importing the package stays free of side effects.
"""

from __future__ import annotations

from ..media.ffmpeg import FFmpegError


class CaptureError(FFmpegError):
    """Media could not be captured or imported, for a reason the user can act on.

    The message is written for the person at the keyboard: it says what went wrong
    and what to do next.  It derives from :class:`~videonotes.media.ffmpeg.FFmpegError`
    so that every caller which already reports media problems as a plain message
    (the command line does) presents capture problems the same way instead of as an
    "unexpected error".
    """


__all__ = ["CaptureError"]

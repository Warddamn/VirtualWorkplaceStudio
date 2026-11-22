"""Bluetooth LE control of a DJI Osmo Action 4 / Osmo Action 5 Pro.

* :mod:`videonotes.dji.rsdk` -- DJI's official remote-control protocol ("R SDK"): frames,
  payloads, pairing handshake.  Pure functions and dataclasses.
* :mod:`videonotes.dji.duml` -- the reverse-engineered protocol that makes the camera join
  Wi-Fi and push an RTMP livestream.  Pure functions and dataclasses.
* :mod:`videonotes.dji.transport` -- the Bluetooth link (``bleak``, imported lazily) and a
  fake for tests; scanning for cameras.
* :mod:`videonotes.dji.camera` -- :class:`~videonotes.dji.camera.OsmoCamera`, the high-level
  asynchronous API, and synchronous helpers for the command line.

Importing this package needs no optional dependency.  None of it could be tried on a
camera when it was written; see ``docs/ARCHITECTURE.md`` §4.7.
"""

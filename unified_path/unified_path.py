# Copyright 2023 Emmanuel Chaboud
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pathlib
import re

from .path_helper import is_relative_to

_DRIVE_TRANSLATIONS = []
_VIRTUAL_DRIVES = []

_DRIVE_REGEX = re.compile(r'^[a-zA-Z]:')
_UNC_REGEX = re.compile(r'^\\')
_POSIX_REGEX = re.compile(r'^/[^/]')


def register_drive_translation(nt_drive, posix_path):
    assert re.match(r'^[A-Z]:/', nt_drive), "nt_drive should be like C:/"
    assert _POSIX_REGEX.match(posix_path), "posix_path should be like /path"

    _DRIVE_TRANSLATIONS.append({'nt': nt_drive, 'posix': posix_path})


def register_virtual_drive(nt_drive, local_path):
    assert re.match(r'^[A-Z]:/', nt_drive), "nt_drive should be like C:/"

    _VIRTUAL_DRIVES.append({'nt': nt_drive, 'local': local_path})


class _CommonPosixPath(pathlib.PurePath):

    def as_unified(self):
        if self.is_absolute():
            # Check mappings
            for mapping in _VIRTUAL_DRIVES:
                if is_relative_to(self, mapping['local']):
                    return pathlib.PureWindowsPath(mapping['nt'], self.relative_to(mapping['local'])).as_posix()

            # Translate mount point
            mount = next((m for m in _DRIVE_TRANSLATIONS if is_relative_to(self, m['posix'])), None)
            if mount is not None:
                return pathlib.PureWindowsPath(mount['nt'], self.relative_to(mount['posix'])).as_posix()

        return os.fspath(self)


class _CommonWindowsPath(pathlib.PurePath):

    def as_unified(self):
        if self.is_absolute():
            # Check mappings
            for mapping in _VIRTUAL_DRIVES:
                if is_relative_to(self, mapping['local']):
                    return pathlib.PureWindowsPath(mapping['nt'], self.relative_to(mapping['local'])).as_posix()

        return self.as_posix()


class _PurePosixPath(pathlib.PurePosixPath, _CommonPosixPath):
    pass


class _PureWindowsPath(pathlib.PureWindowsPath, _CommonWindowsPath):
    pass


class _PosixPath(pathlib.PosixPath, _CommonPosixPath):
    pass


class _WindowsPath(pathlib.WindowsPath, _CommonWindowsPath):
    pass


class PureUnifiedPath(pathlib.PurePath):
    """A pathlib.PurePath that handles OS-independent path conversion.
    """

    def __new__(cls, *args):
        if len(args) == 0:
            return _PureWindowsPath() if os.name == 'nt' else _PurePosixPath()

        root = args[0]
        if isinstance(root, pathlib.PurePath):
            root = os.fspath(root)

        if not isinstance(root, str):
            raise TypeError('argument should be a str object or an os.PathLike '
                            'object returning str, not %r' % type(root))

        if _DRIVE_REGEX.match(root):
            # Drive letter and colon: Windows path
            path = _PureWindowsPath(*args)
        elif _UNC_REGEX.match(root):
            # UNC path
            path = _PureWindowsPath(*args)
        elif _POSIX_REGEX.match(root):
            # Slash followed by non-slash: Posix path
            path = _PurePosixPath(*args)
        else:
            # Relative path
            path = _PureWindowsPath(*args)

        # Check mappings
        if isinstance(path, pathlib.PureWindowsPath):
            if path.is_absolute():
                for mapping in _VIRTUAL_DRIVES:
                    if is_relative_to(path, mapping['nt']):
                        if os.name == 'nt':
                            return _PureWindowsPath(mapping['local'], path.relative_to(mapping['nt']))
                        else:
                            return _PurePosixPath(mapping['local'], path.relative_to(mapping['nt']))

        # Nt -> posix conversion
        if os.name == 'posix' and isinstance(path, pathlib.PureWindowsPath):
            if path.is_absolute():
                mount = next((m for m in _DRIVE_TRANSLATIONS if is_relative_to(path, m['nt'])), None)
                assert mount is not None, 'Cannot convert absolute NT path to posix: %s' % os.fspath(path)

                return _PurePosixPath(mount['posix'], path.relative_to(mount['nt']))

            return _PurePosixPath(path)

        # Posix -> nt conversion
        if os.name == 'nt' and isinstance(path, pathlib.PurePosixPath):
            if path.is_absolute():
                mount = next((m for m in _DRIVE_TRANSLATIONS if is_relative_to(path, m['posix'])), None)
                assert mount is not None, 'Cannot convert absolute posix path to NT: %s' % os.fspath(path)

                return _PureWindowsPath(mount['nt'], path.relative_to(mount['posix']))

            return _PureWindowsPath(path)

        # No conversion needed
        return path


class UnifiedPath(pathlib.Path):
    """A pathlib.Path that handles OS-independent path conversion.
    """

    def __new__(cls, *args):
        unified_path = PureUnifiedPath(*args)
        return _WindowsPath(unified_path) if os.name == 'nt' else _PosixPath(unified_path)

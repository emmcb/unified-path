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

import os.path
from pathlib import Path


def absolute(path, root_dir=Path.cwd(), norm=False):
    """Helper function to convert a path to absolute.

    Unlike Path.resolve() and os.path.abspath, this function will not try to normalize by default the resulting path.

    Args:
        path: The path to transform.
        root_dir: The root directory, by default Path.cwd().
        norm: Should the path be normalized. False by default.
    Returns:
        The absolute path.
    """
    path_type = type(path)

    if not path.is_absolute():
        path = root_dir / path

    if norm:
        path = normalized(path)

    return path_type(path)


def normalized(path):
    """Helper function to normalize a path.

    This function is different from Path.resolve() because Path.resolve() will do actual filesystem access to resolve
    symlinks. This is more accurate but slower, and triggers https://bugs.python.org/issue35306 on Windows.

    This function instead use os.path.normpath to normalize the path, which does a simple string parsing that may be
    wrong if using Unix symlinks, but does not present the above issues.

    Args:
        path: The path to transform.
    Returns:
        The normalized path.
    """
    path_type = type(path)
    return path_type(os.path.normpath(path))


def find_common_prefix(files):
    """Find the common of prefix of the given file list.

    For example, common prefix of /tmp/file1.txt and /tmp/file2.txt is /tmp.

    Args:
        files: The file list.
    Returns:
        The path that it the common prefix of given files.
    """
    if len(files) == 0:
        return None

    all_parts = files[0].parts[:-1]
    common_parts = []

    for i, part in enumerate(all_parts):
        for f in files:
            if len(f.parts) - 1 <= i or f.parts[i] != part:
                return Path(*common_parts) if common_parts else None

        common_parts.append(part)

    return Path(*common_parts) if common_parts else None


def is_relative_to(path, *other):
    """Return True if the path is relative to another path or False.
    """
    try:
        path.relative_to(*other)
        return True
    except ValueError:
        return False


def with_stem(path, stem):
    """Return a new path with the stem changed.
    """
    return path.with_name(stem + path.suffix)


def append_stem(path, stem):
    """Return a new path with given stem added to the right of the current stem.
    """
    return with_stem(path, path.stem + stem)


def prepend_stem(path, stem):
    """Return a new path with given stem added to the left of the current stem.
    """
    return with_stem(path, stem + path.stem)


def append_name(path, name):
    """Return a new path with given name added to the right of the current name.
    """
    return path.with_name(path.name + name)


def prepend_name(path, name):
    """Return a new path with given name added to the left of the current name.
    """
    return path.with_name(name + path.name)

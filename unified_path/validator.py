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

import argparse

from .unified_path import UnifiedPath


def make_path_validator(extensions=None):
    """Generate a path validator that optionaly checks the file extension.

    This function can be used for argparse argument checking:

    parser.add_argument(..., type=make_path_validator(extensions=['.json']), ...)

    Args:
        extensions: List of allowed extensions (including the .), by default None.
    Returns:
        The validator function.
    """

    def validator(obj):
        path = UnifiedPath(obj)

        if extensions is not None and path.suffix.lower() not in extensions:
            raise argparse.ArgumentTypeError('Path "%s" must have one of the following extensions: %s' %
                                             (obj, extensions))

        return path

    return validator

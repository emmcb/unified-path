import os
from unittest.mock import patch

import pytest

import unified_path
from unified_path import PureUnifiedPath

root_dir = os.path.dirname(__file__)

unified_path.register_drive_translation('B:/', '/srv/database')
unified_path.register_virtual_drive('R:/', root_dir)


@patch('unified_path.os.name', 'posix')
def test_unified_path_posix():
    assert str(PureUnifiedPath('/srv/database/my/file')) == '/srv/database/my/file'
    assert str(PureUnifiedPath('B:/my/file')) == '/srv/database/my/file'
    assert str(PureUnifiedPath('B:\\my\\file')) == '/srv/database/my/file'

    assert str(PureUnifiedPath('/my/file')) == '/my/file'
    with pytest.raises(AssertionError):
        PureUnifiedPath('C:/my/file')
        PureUnifiedPath('C:\\my\\file')

    assert str(PureUnifiedPath('my/file')) == 'my/file'
    assert str(PureUnifiedPath('my\\file')) == 'my/file'


@patch('unified_path.os.name', 'nt')
def test_unified_path_nt():
    assert str(PureUnifiedPath('/srv/database/my/file')) == 'B:\\my\\file'
    assert str(PureUnifiedPath('B:/my/file')) == 'B:\\my\\file'
    assert str(PureUnifiedPath('B:\\my\\file')) == 'B:\\my\\file'

    assert str(PureUnifiedPath('C:/my/file')) == 'C:\\my\\file'
    assert str(PureUnifiedPath('C:\\my\\file')) == 'C:\\my\\file'
    with pytest.raises(AssertionError):
        PureUnifiedPath('/my/file')

    assert str(PureUnifiedPath('my/file')) == 'my\\file'
    assert str(PureUnifiedPath('my\\file')) == 'my\\file'


def test_unified_path_unified():
    assert PureUnifiedPath('/srv/database/my/file').as_unified() == 'B:/my/file'
    assert PureUnifiedPath('B:/my/file').as_unified() == 'B:/my/file'
    assert PureUnifiedPath('B:\\my\\file').as_unified() == 'B:/my/file'

    assert PureUnifiedPath('my/file').as_unified() == 'my/file'
    assert PureUnifiedPath('my\\file').as_unified() == 'my/file'


def test_unified_path_virtual_drive():
    assert str(PureUnifiedPath('R:/my/file')) == str(PureUnifiedPath(root_dir, 'my/file'))
    assert PureUnifiedPath(root_dir, 'my/file').as_unified() == 'R:/my/file'

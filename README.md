# Unified Path

Unified Path is a Python wrapper around `pathlib.PurePath` and `pathlib.Path`, that provides an OS-independent path representation.
It is especially useful in shared environments when you need to write to a path in a configuration file, and this file may be read from different OS.

## Installation

Install from pypi using pip:

```
pip install unified-path
```

## Drive translations

Let's say you have a shared drive containing pictures. This drive is accessible on Windows as `P:`, and on Linux as `/mnt/pictures`.
Using this library you can easily handle this situation by storing an unified path to the Pictures drive, that will be readable on both OS.

First you need to register the paths:

```python
import unified_path as up

up.register_drive_translation('P:/', '/mnt/pictures')
```

Then you can obtain the unified string representation using the `as_unified()` function:

```python
# In Linux
up.UnifiedPath('/mnt/pictures/folder/img.jpg').as_unified() # P:/folder/img.jpg

# In Windows
up.UnifiedPath('P:\\folder\\img.jpg').as_unified() # P:/folder/img.jpg

```

You can construct an `UnifiedPath` instance from either the local representation or either the unified representation.
As `UnifiedPath` inherits from `pathlib.Path`, you can use the result as any other `Path` object.

```python
# In Linux
up.UnifiedPath('P:/folder/img.jpg') # ok
up.UnifiedPath('P:\\folder\\img.jpg') # also ok

# In Windows
up.UnifiedPath('P:/folder/img.jpg') # ok
up.UnifiedPath('/mnt/pictures/folder/img.jpg') # also ok

```

## Virtual drives

It is also possible to assign a virtual drive letter to a dynamic path.
This allows to "hide" a part of the path that may change, so that the stored path will always remain valid.

```python
import unified_path as up

git_root = ... # obtain root path of current repository using some git command
up.register_virtual_drive('G:/', git_root)

up.UnifiedPath('G:/data/conf.json') # ok
```

## Usage with argparse

Unified Path can be used as argparse arguments:

```python
# Now you can use -i P:/folder/img.jpg in Linux
parser.add_argument('-i', type=up.UnifiedPath, required=True, help='input file')
```

The library also comes with a helper that constraints the file extension:

```python
# An error will be emitted if calling -i with a file that is not a .jpg
parser.add_argument('-i', type=up.make_path_validator(['.jpg']), required=True, help='input image')
```

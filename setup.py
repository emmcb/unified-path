from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(name='unified-path',
      version='1.0',
      description='A Python wrapper around pathlib providing an OS-independent path representation.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Emmanuel Chaboud',
      url='https://github.com/emmcb/unified-path',
      classifiers=[
          'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3 :: Only', 'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      python_requires='>=3')

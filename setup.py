import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name="qbittorrent.py",
      version="0.9.0",
      author="Raghu Rajagopalan",
      author_email="raghu.nospam@gmail.com",
      description=("CLI client for qBittorrent"),
      license = "BSD",
      keywords = "qbittorrent, cli",
      url = "https://github.com/raghur/qbittorrent.py.git",
      packages=['qbittorrent', 'tests'],
      install_requires = [
          'requests'
      ],
      entry_points = {
          'console_scripts': [
              'qbittorrent-cli = qbittorrent.main:main'
          ]
      },
      long_description='see https://github.org/raghur/qBittorrent.py',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Utilities",
          "License :: OSI Approved :: BSD License",
      ],
      )

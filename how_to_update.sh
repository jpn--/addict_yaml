#!/bin/bash

conda build ./conda --output-folder conda_builds/ -c jpn --python 3.6

conda build ./conda --output-folder conda_builds/ -c jpn --python 3.7

anaconda upload conda_builds/osx-64/addict_yaml-0.2.6-*.tar.bz2

conda convert --platform win-64 conda_builds/osx-64/addict_yaml-0.2.6-*.tar.bz2 -o conda_builds/
anaconda upload conda_builds/win-64/addict_yaml-0.2.6-*.tar.bz2

conda convert --platform linux-64 conda_builds/osx-64//addict_yaml-0.2.6-*.tar.bz2 -o conda_builds/
anaconda upload conda_builds/linux-64/addict_yaml-0.2.6-*.tar.bz2

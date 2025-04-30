# Installation

## Pre-packaged app

To download the pre-packaged app, go to the [Releases link](https://github.com/backyardbiomech/qtiConverter/releases) at the right of the page. Click on the most recent release, and download the zip file for your operating system.

Uncompress the zip file. Inside, you will find a folder called `qtiConverter`. Inside that folder, you will find a file called `qtiConverter.exe` (or `qtiConverter` on Mac). This is the app. You can move this folder anywhere you like, but it is recommended to keep it in a place where you can easily find it later.

The app is a simple GUI that allows you to select the input file(s), and then run the conversion. It also will allow you to load an image and select an area for hotspot questions. It is a simple wrapper around the command line script, so it does the same thing.

## Command line

The converter is a python script that must be run from the command line.

These instructions assume you have python installed. If you don't, I suggest you use miniconda to create a simply python environment.

1. Download this repository (click on green `Code` button and download zip, or clone).
2. If you downloaded the zip, unzip it. Put the whole folder somewhere easy to find, you'll need to know the path to it later.

If you are going to use hot spot type questions, I've included a small script that will load an image and record the coordinates of a polygon you define on the image by clicking on it. Only if you want to use that, you will need to also install `opencv-python` and `matplotlib` with `pip`.
    + `pip install opencv-python matplotlib`

Next step: [Preparing the document](formatting.md)
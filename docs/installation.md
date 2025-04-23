# Installation

## Pre-packaged app

To download the pre-packaged app, go to the [Actions tab](https://github.com/backyardbiomech/qtiConverter/actions) at the top of the repository. Click on the most recent build, and scroll down to the bottom of the page. There you will find a link to download the app for your operating system.

The app is a simple GUI that allows you to select the input file(s), and then run the conversion. It also will allow you to load an image and select an area for hotspot questions. It is a simple wrapper around the command line script, so it does the same thing.

## Command line

The converter is a python script that must be run from the command line.

These instructions assume you have python installed. If you don't, I suggest you use miniconda to create a simply python environment.

1. Download this repository (click on green `Code` button and download zip, or clone).
2. If you downloaded the zip, unzip it. Put the whole folder somewhere easy to find, you'll need to know the path to it later.

If you are going to use hot spot type questions, I've included a small script that will load an image and record the coordinates of a polygon you define on the image by clicking on it. Only if you want to use that, you will need to also install `opencv-python` and `matplotlib` with `pip`.
    + `pip install opencv-python matplotlib`

Next step: [Preparing the document](formatting.md)
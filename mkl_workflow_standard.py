#!/usr/bin/env python

from __future__ import division
from gimpfu import *
import os

# create an output function that redirects to gimp's Error Console
def gprint( text ):
   pdb.gimp_message(text)
   return

def calculateNewDimensions(oldWidth, oldHeight):
    newWidth = oldWidth
    newHeight = oldHeight
    if oldWidth > oldHeight: # landscape
      newWidth = 1500
      ratio = newWidth / oldWidth
      newHeight = oldHeight * ratio
    else:
      newHeight = 1200
      ratio = newHeight / oldHeight
      newWidth = oldWidth * ratio

    return newWidth, newHeight

# our script
def my_script_function(image, drawable) :

    pdb.plug_in_unsharp_mask(image, drawable, unsharpRadiusFirstPass, unsharpAmountFirstPass, 0)
    oldWidth = drawable.width
    oldHeight = drawable.height
    newWidth, newHeight = calculateNewDimensions(oldWidth, oldHeight)
    pdb.gimp_image_scale(image, newWidth, newHeight)
    pdb.plug_in_unsharp_mask(image, drawable, 0.1, 0.1, 0)

    filename = image.filename
    base = os.path.splitext(filename)[0]
    newName = base + ".jpg"
    quality = 0.9
    pdb.file_jpeg_save(image, drawable, newName, newName, quality, 0, 0, 0, "", 0, 1, 0, 0)
    pdb.gimp_image_clean_all(image)
    #gprint("saved %dx%d %s" % (newWidth, newHeight, os.path.split(newName)[-1]))

    return

# This is the plugin registration function
register(
      "mkl_workflow_standard"
    , "RAW to JPG with my favourite parameters"
    , "applies in this order: unsharp mask, downscale, unsharp mask, save as jpg"
    , "Markus Klinik"
    , ""
    , "2014"
    , "<Image>/MyScripts/Standard Sharpen and Scale"
    , "*"
    , []
    , []
    , my_script_function
    )

main()

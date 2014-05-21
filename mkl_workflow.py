#!/usr/bin/env python

from __future__ import division
from gimpfu import *
import os

defaultUnsharpRadiusFirstPass = 3.0
defaultUnsharpAmountFirstPass = 0.3
defaultProposedNewWidth = 1000
defaultProposedNewHeight = 800
defaultDoSave = True

# create an output function that redirects to gimp's Error Console
def gprint( text ):
   pdb.gimp_message(text)
   return

def calculateNewDimensions(oldWidth, oldHeight, proposedNewWidth, proposedNewHeight):
    newWidth = oldWidth
    newHeight = oldHeight
    if oldWidth > oldHeight: # landscape
      newWidth = proposedNewWidth
      ratio = newWidth / oldWidth
      newHeight = oldHeight * ratio
    else:
      newHeight = proposedNewHeight
      ratio = newHeight / oldHeight
      newWidth = oldWidth * ratio

    return newWidth, newHeight

def mkl_workflow_parameterized(image, drawable,
    unsharpRadiusFirstPass,
    unsharpAmountFirstPass,
    proposedNewWidth,
    proposedNewHeight,
    doSave) :

    pdb.gimp_image_undo_group_start(image)

    pdb.plug_in_unsharp_mask(image, drawable, unsharpRadiusFirstPass, unsharpAmountFirstPass, 0)
    oldWidth = drawable.width
    oldHeight = drawable.height
    newWidth, newHeight = calculateNewDimensions(oldWidth, oldHeight, proposedNewWidth, proposedNewHeight)
    pdb.gimp_image_scale(image, newWidth, newHeight)
    pdb.plug_in_unsharp_mask(image, drawable, 0.1, 0.1, 0)

    if doSave:
        filename = image.filename
        base = os.path.splitext(filename)[0]
        newName = base + ".jpg"
        quality = 0.95
        pdb.file_jpeg_save(image, drawable, newName, newName, quality, 0, 0, 0, "", 0, 1, 0, 0)
        pdb.gimp_image_clean_all(image)

    pdb.gimp_image_undo_group_end(image)

    return

def mkl_workflow_standard(image, drawable) :
    mkl_workflow_parameterized(
      image,
      drawable,
      defaultUnsharpRadiusFirstPass,
      defaultUnsharpAmountFirstPass,
      defaultProposedNewWidth,
      defaultProposedNewHeight,
      defaultDoSave)
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
    , mkl_workflow_standard
    )

register(
      "mkl_workflow_parameterized"
    , "raw to jpg with given parameters"
    , "applies in this order: unsharp mask, downscale, unsharp mask, save as jpg"
    , "Markus Klinik"
    , ""
    , "2014"
    , "<Image>/MyScripts/Parametrized Sharpen and Scale"
    , "*"
    , [ (PF_FLOAT, 'unsharpRadiusFirstPass', 'Unsharp radius for the first pass', defaultUnsharpRadiusFirstPass)
      , (PF_FLOAT, 'unsharpAmountFirstPass', 'Unsharp amount for the first pass', defaultUnsharpAmountFirstPass)
      , (PF_INT, 'proposedNewWidth', 'new width for landscape photos', defaultProposedNewWidth)
      , (PF_INT, 'proposedNewHeight', 'new height for portrait photos', defaultProposedNewHeight)
      , (PF_BOOL,  'doSave', 'Save afterwards', defaultDoSave)
      ]
    , []
    , mkl_workflow_parameterized
    )

main()


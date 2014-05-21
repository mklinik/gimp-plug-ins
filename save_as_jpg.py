#!/usr/bin/env python

# save_as_jpg.py
# version 1.1 [gimphelp.org]
# last modified/tested by Paul Sherman
# 01/31/2013 on GIMP-2.8
#
# original release 12/20/2012
# 1.1 added file-overwrite prompt and actually saves
# any comment entered (ooops)
#
# an offshoot of Akkana Peck's Save/export clean plug-in:
# ==== Original Information ====================================================
# Save or export the current image -- do the right thing whether it's
# XCF (save) or any other format (export). This will mark the image clean,
# so GIMP won't warn you when you exit.
# Warning: this does not show a lot of extra dialogs, etc. or warn you
# if you're about to overwrite something! Use with caution.

# Copyright 2012 by Akkana Peck, http://www.shallowsky.com/software/
# You may use and distribute this plug-in under the terms of the GPL v2
# or, at your option, any later GPL version.
# ========================================================

from gimpfu import *
import gtk
import os, sys
import collections

def python_export_clean(img, drawable) :
	filename = img.filename
	quality = 0.95
	if filename :
		base = os.path.splitext(filename)[0]
		newname = base + ".jpg"
		pdb.file_jpeg_save(img, drawable, newname, newname, quality, 0, 0, 0, "", 0, 1, 0, 0)
                pdb.gimp_image_clean_all(img)


register(
		"python_fu_save_as_JPG",
		"Save the image as a JPG file, set the output quality\nand include a comment if desired...\n\nFor more options and a proper file overwrite protected dialog, \nuse the FILE > EXPORT menu item when saving as a JPG.\n\n",
		"",
		"Paul Sherman",
		"GPL",
		"2012",
		"Save as JPG",
		"*",
		[
			(PF_IMAGE, "image", "Input image", None),
			(PF_DRAWABLE, "drawable", "Input drawable", None),
		],
		[],
		python_export_clean,
		menu = "<Image>/File/Save/"
)

main()

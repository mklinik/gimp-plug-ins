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

def python_export_clean(img, drawable, quality, comment) :
	filename = img.filename
	qual = quality/100
#	fullpath = pdb.gimp_image_get_uri(img)
#	pdb.gimp_message(filename)

	if not filename :
		chooser = gtk.FileChooserDialog(
			title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,
			buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK)
			)
		# save folder will be desktop
		save_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
			
		chooser.set_current_folder(save_dir)
		chooser.set_current_name("UNTITLED.jpg")
		chooser.set_do_overwrite_confirmation(True)
		
		filter = gtk.FileFilter()
		filter.set_name("Save as JPG")
		filter.add_pattern("*.jpg")
		chooser.add_filter(filter) 
		
		response = chooser.run()
		if response != gtk.RESPONSE_OK:
			return
		filename = chooser.get_filename()
		img.filename = filename
		chooser.destroy()
	
		pdb.file_jpeg_save(img, drawable, filename, filename, qual, 0, 0, 0, comment, 0, 1, 0, 0)
		pdb.gimp_image_clean_all(img)		
			
		
	else:
		base = os.path.splitext(filename)[0]
		newname = base + ".jpg"

		pdb.gimp_edit_copy(img.active_drawable)
		image2 = pdb.gimp_edit_paste_as_new()
		pdb.file_jpeg_save(image2, drawable, newname, newname, qual, 0, 0, 0, comment, 0, 1, 0, 0)
		pdb.gimp_image_delete(image2)		
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
			(PF_SLIDER, "quality", "Set the JPG output quality", 90, (30, 100, 5) ),
			(PF_STRING, "comment", "Write comment (unseen) into file... ", "" )
		],
		[],
		python_export_clean,
		menu = "<Image>/File/Save/"
)

main()

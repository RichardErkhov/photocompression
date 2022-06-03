# Some code for photo compression and archive encryption
If you are using my code, please leave a link to my github.
This code is mess, that's True, one day I will fix it! Thank you for understanding.
This code is not working properly (probably), there are a lot of unused libraries, so I'm going to fix them soon.
There is gui version (just run python gui.py).
Main code is in main.py. You can edit it to make fit you purpose.
There are 2 main functions (in main.py): make_archive() and open_archive()

A little bit of documentation: 
=============================
make_archive() has 4 arguments (2 only mandatory):
-archive_name (required: str): Self-explanatory.
-folder_name (required: str): the name/path of directory with photos.
-password (not required, default: "password"): Password used for encryption.
-output_folder (not required, default: "."): output folder where archive will be stored.
=============================
open_archive has 3 arguments (2 only mandatory):
-archive_name (required: str): Seld-explanatory.
-folder_name (required: str): where to output contents of archive.
-password (not required, default: "password"): Password used for decryption.
=============================




#TODO learn to write normal descriptions.
#TODO count files in archive and output their name.
#TODO view files without extracting archive
#TODO clean the code
#TODO compile it for windows

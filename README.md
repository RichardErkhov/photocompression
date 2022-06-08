# Some code for photo compression and archive encryption
If you are using my code, please leave a link to my github.

There is gui version (just run python gui.py) and cli version (just run python cli.py).

Main code is in main.py. You can edit it to make fit you purpose.

There are 2 main functions (in main.py): make_archive() and open_archive()

A little bit of documentation: 

make_archive() has 4 arguments (2 only mandatory):

-archive_name (required: str): Self-explanatory.

-folder_name (required: str): the name/path of directory with photos.

-password (not required, default: "password"): Password used for encryption.

-output_folder (not required, default: "."): output folder where archive will be stored.

-kmeans (not required, default: False): use of Kmeans for better compression. Usually we don't use it because of high system resource usage.

-K_number (not required, default: 8): number of classes if kmeans is used

open_archive has 3 arguments (2 only mandatory):

-archive_name (required: str): Self-explanatory.

-folder_name (required: str): where to output contents of archive.

-password (not required, default: "password"): Password used for decryption.







TODO section
#TODO learn to write normal descriptions.

#TODO count files in archive and output their name.

#TODO view files without extracting archive

#TODO remove opencv from there to lower compiled program's weight

#TODO make it to work with different resolutions

#TODO choose how loss works (now just lossless)

#TODO add comments to code

#TODO add different types of encryption

#TODO check the difference between images and sort by least difference

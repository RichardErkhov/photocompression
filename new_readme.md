# Photocompression with encryption
## Overview
This script is designed to create and manage encrypted image archives. The archives are compressed using a video format to save storage space, and can be encrypted for added security. This script allows you to create, open, and repack encrypted image archives.

## Required external libraries
- numpy
- cv2 (OpenCV)
- PIL (Python Imaging Library)
- pyAesCrypt
- skvideo.io 
- tqdm
- imageio

## Functions
### sort(folder, k=3, size=False, resample=256, move=False)
This function sorts the images in the given folder using the k-means clustering algorithm. It takes the following parameters:

- `folder`: The folder containing the images.
- `k`: The number of clusters.
- `size`: If True, resize the images before clustering.
- `resample`: The resolution for resampling the images.
- `move`: If True, move the images into their respective clusters.

### get_files(folder)
This function returns a list of image files in the given folder. It takes the following parameter:

- `folder`: The folder containing the images.

### create_video(folder, files, video_name, output_folder='.', kmeans=False)
This function creates a video from the given image files. It takes the following parameters:

- `folder`: The folder containing the images.
- `files`: A list of image file names.
- `video_name`: The name of the output video file.
- `output_folder`: The folder to store the output video file.
- `kmeans`: If True, the files list is a k-means object.

### create_archive(video_name, archive_name, output_folder='.')
This function creates an archive from the given video file. It takes the following parameters:

- `video_name`: The name of the video file.
- `archive_name`: The name of the output archive file.
- `output_folder`: The folder to store the output archive file.

### encrypt_archive(archive_name, password='password', output_folder='.')
This function encrypts the given archive file. It takes the following parameters:

- `archive_name`: The name of the archive file.
- `password`: The password to use for encryption.
- `output_folder`: The folder containing the archive file.

### decrypt_archive(archive_name, password='password')
This function decrypts the given encrypted archive file. It takes the following parameters:

- `archive_name`: The name of the encrypted archive file.
- `password`: The password to use for decryption.

### get_filesx(archive_name, password='password')
This function reads the file names from the given archive without extracting the images. It takes the following parameters:

- `archive_name`: The name of the archive file.
- `password`: The password to use for decryption.

### get_files_count(archive_name, password='password')
This function returns the number of image files in the given archive. It takes the following parameters:

- `archive_name`: The name of the archive file.
- `password`: The password to use for decryption.

### unpack_archive(archive_name)
This function extracts the contents of the given archive file. It takes the following parameter:

- `archive_name`: The name of the archive file.

### extract_frames(video_name, folder)
This function extracts the images from the given video file. It takes the following parameters:

- `video_name`: The name of the video file.
- `folder`: The folder to store the extracted images.

### make_archive(archive_name, folder_name, password=None, output_folder='.', kmeans=False, k_number=8)

This function creates an encrypted image archive from the given folder. It takes the following parameters:

- `archive_name`: The name of the output archive file.
- `folder_name`: The folder containing the images.
- `password`: The password to use for encryption (default: None).
- `output_folder`: The folder to store the output archive file (default: '.').
- `kmeans`: If True, the images will be sorted using k-means clustering before archiving (default: False).
- `k_number`: The number of clusters for k-means clustering (default: 8).

### open_archive(archive_name, folder_name, password=None)
This function opens an encrypted image archive and extracts its contents. It takes the following parameters:

- `archive_name`: The name of the encrypted archive file.
- `folder_name`: The folder to store the extracted images.
- `password`: The password to use for decryption (default: None).

### repack_pre_0_3_archive(archive_name, folder_name, password=None)
This function repacks an encrypted image archive created by a previous versions (<0.3) of the script. It takes the following parameters:

- `archive_name`: The name of the encrypted archive file.
- `folder_name`: The folder containing the images.
- `password`: The password to use for decryption (default: None).

## Usage
To use this script, you can import it as a module in another script or run it directly from the command line. Here's an example of how to create an encrypted image archive:
```python
make_archive("test.zip", "catz", password='password', kmeans=True)
```
To open an encrypted image archive and extract its contents, you can use the following example:
```python
open_archive("test.zip", "test", password='password')
```
The script also includes a function for repacking encrypted archives created by a previous version (<0.3) of the script:
```python
repack_pre_0_3_archive("test.zip.aes", "test", password="test")
```

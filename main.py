import os
import shutil
import subprocess
import sys
import time
import zipfile
import glob
import numpy as np
import cv2
from PIL import Image
import pyAesCrypt
import skvideo.io
import tqdm
import io
import imageio
def get_files(folder):
    files = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            files.append(os.path.join(filename))
    return files

def create_video(folder, files, video_name, output_folder='.'):
    with open(os.path.join(output_folder, "files.txt"), mode='w') as f:
        out = skvideo.io.FFmpegWriter(os.path.join(output_folder,video_name), outputdict={
  '-vcodec': 'libx264',  #use the h.264 codec
  '-crf': '0',           #set the constant rate factor to 0, which is lossless
  '-preset':'veryslow'   #the slower the better compression, in princple, try 
                         #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
}) 
        for filename in tqdm.tqdm(files, desc="compressing files"):
            img = cv2.imread(os.path.join(folder,filename))
            f.write(filename + "\n")
            out.writeFrame(img[:,:,::-1])
        out.close()
    
def create_archive(video_name, archive_name, output_folder='.'):
    with zipfile.ZipFile(os.path.join(output_folder, archive_name), 'w') as myzip:
        myzip.write(os.path.join(output_folder, video_name))
        myzip.write(os.path.join(output_folder, "files.txt"))

def encrypt_archive(archive_name, password='password', output_folder='.'):
    bufferSize = 64 * 1024
    pyAesCrypt.encryptFile(os.path.join(output_folder, archive_name),
                        os.path.join(output_folder, archive_name + ".aes"), 
                        str(password), bufferSize)
    os.remove(os.path.join(output_folder, archive_name))

def decrypt_archive(archive_name, password='password'):
    bufferSize = 64 * 1024
    pyAesCrypt.decryptFile(archive_name + ".aes", archive_name, str(password), bufferSize)

#in memory we need to decrypt archive
#and read get files.txt without extracting it to drive
def get_filesx(arhive_name, password='password'):
    #decrypt archive
    #use pyAesCrypt.decryptStream
    decypted_archive = io.BytesIO()
    with open(arhive_name, 'rb') as f:
        length = os.path.getsize(arhive_name)
        pyAesCrypt.decryptStream(f, decypted_archive, password, 64 * 1024, length)
    decypted_archive.seek(0)
    #read files.txt
    with zipfile.ZipFile(decypted_archive) as myzip:
        with myzip.open("files.txt") as f:
            files = f.read().decode().splitlines()
    return files

#get random frame from video from aes archive
#you can do the same that we did with files.txt
def get_random_frame(archive_name, password='password'):
    #decrypt archive
    #use pyAesCrypt.decryptStream
    decypted_archive = io.BytesIO()
    with open(archive_name, 'rb') as f:
        length = os.path.getsize(archive_name)
        pyAesCrypt.decryptStream(f, decypted_archive, password, 64 * 1024, length)
    decypted_archive.seek(0)
    #read files.txt
    with zipfile.ZipFile(decypted_archive) as myzip:
        with myzip.open("video.avi") as video:
            print(type(video.read()))
            #using imageio iterate over frames in the videio

            for frame in imageio.get_reader(video.read(), 'ffmpeg'):
                print(frame.shape)

            #videogen = skvideo.io.vreader(video.read())
            #e, img = cap.read()
            #for frame in vid:
            #    cv2.imshow("frame", frame)
            #    cv2.waitKey(0)
                #if e:
                    #show images
                    #cap.release()
                    #cap.release()
                    #return img
                #else:
                    #cap.release()
                    #return None
    #get random frame
    rand_file = np.random.choice(files)
    return rand_file
    
def unpack_archive(archive_name):
    with zipfile.ZipFile(archive_name, 'r') as myzip:
        myzip.extractall()
    os.remove(archive_name)


def extract_frames(video_name, folder):
    if not os.path.exists(folder):
        if folder.strip() == '':
            folder = 'test'
        os.makedirs(folder)
    cap = cv2.VideoCapture(video_name)
    
    with open("files.txt", mode='r') as f:
        for line in tqdm.tqdm(f, desc='extracting images'):
            line = line.strip()
            e, img = cap.read()
            if e:
                cv2.imwrite(os.path.join(folder,line), img)
            else:
                cap.release()
                break 
    try: cap.release()
    except: pass
    time.sleep(1)
    os.remove(video_name)
    os.remove("files.txt")
def make_archive(archive_name: str, folder_name: str, password=None, output_folder='.'):
    #check if folder exists, if not create it 
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    #get files
    files = get_files(folder_name)
    #create video
    video_name = "video.avi"
    create_video(folder_name, files, video_name, output_folder=output_folder)
    #create archive
    create_archive(video_name, archive_name, output_folder=output_folder)
    #encrypt archive
    if password is not None:
        encrypt_archive(archive_name, password = password, output_folder=output_folder)
    else:
        encrypt_archive(archive_name, password='password', output_folder=output_folder)
    #remove video
    os.remove(os.path.join(output_folder, video_name))
    os.remove(os.path.join(output_folder, "files.txt"))
def open_archive(archive_name, folder_name, password=None):
    #decrypt archive
    if password is not None:
        decrypt_archive(archive_name, password = password)
    else:
        decrypt_archive(archive_name, password='password')
    #unpack archive
    unpack_archive(archive_name)
    #extract frames
    video_name = "video.avi"
    extract_frames(video_name, folder_name)

if __name__ == "__main__":
    make_archive("test.zip", "test", password='password')
    open_archive("test.zip", "test", password='password')

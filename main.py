#https://github.com/victorqribeiro/groupImg
import os
from zipfile import ZipFile
from glob import glob
import numpy as np
import cv2
from PIL import Image
import pyAesCrypt
from skvideo.io import FFmpegWriter
import tqdm
import io
import math
import warnings
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
#import imageio.v3 as iio
from imageio.v3 import imread
from kmeans import K_means
Image.MAX_IMAGE_PIXELS = None
warnings.simplefilter('ignore')

def sort(folder, k=3, size=False, resample=256, move=False):
    types = ('*.jpg', '*.JPG', '*.png', '*.jpeg')
    imagePaths = []
    folder = folder
    if not folder.endswith("/") :
        folder+="/"
    for files in types :
        imagePaths.extend(sorted(glob(folder+files)))
    nimages = len(imagePaths)
    nfolders = int(math.log(k, 10))+1
    if nimages <= 0 :
        print("No images found!")
        exit()
    if resample < 16 or resample > 256 :
        print("-r should be a value between 16 and 256")
        exit()
    k = K_means(k,size,resample)
    k.generate_k_clusters(imagePaths)
    k.rearrange_clusters()
    return k
    
def get_files(folder):
    files = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            files.append(os.path.join(filename))
    return files

def create_video(folder, files, video_name, output_folder='.', kmeans=False):
    with open(os.path.join(output_folder, "files.txt"), mode='w') as f:
        out = FFmpegWriter(os.path.join(output_folder,video_name), outputdict={
  '-vcodec': 'libx264',  #use the h.264 codec
  '-crf': '0',           #set the constant rate factor to 0, which is lossless
  '-preset':'veryslow'   #the slower the better compression, in princple, try 
                         #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
}) 
        if kmeans == False:
            for filename in tqdm.tqdm(files, desc="compressing files"):
                img = cv2.imread(os.path.join(folder,filename))
                f.write(f"{filename}|{img.shape[0]}|{img.shape[1]}\n")
                out.writeFrame(img[:,:,::-1])
        else:
            sorts = []
            for i in range(files.k):
                sorts.append([])
            for filename in range(len(files.end)):
                sorts[files.cluster[filename]].append(files.end[filename])
            for i in tqdm.tqdm(sorts, desc="compressing files"):
                for filename in tqdm.tqdm(i, leave=False):
                    img = cv2.imread(filename)
                    f.write(f"{os.path.split(filename)[-1]}|{img.shape[0]}|{img.shape[1]}\n")
                    out.writeFrame(img[:,:,::-1])
        out.close()
    
def create_archive(video_name, archive_name, output_folder='.'):
    if not archive_name.endswith(".zip"): 
        archive_name += ".zip"
    with ZipFile(os.path.join(output_folder, archive_name), 'w') as myzip:
        myzip.write(os.path.join(output_folder, video_name))
        myzip.write(os.path.join(output_folder, "files.txt"))

def encrypt_archive(archive_name, password='password', output_folder='.'):
    if not archive_name.endswith(".zip"):
        archive_name += ".zip" 
    bufferSize = 64 * 1024
    pyAesCrypt.encryptFile(os.path.join(output_folder, archive_name),
                        os.path.join(output_folder, archive_name + ".aes"), 
                        str(password), bufferSize)
    os.remove(os.path.join(output_folder, archive_name))

def decrypt_archive(archive_name, password='password'):
    bufferSize = 64 * 1024
    pyAesCrypt.decryptFile(archive_name + ".aes", archive_name, str(password), bufferSize)

def get_filesx(arhive_name, password='password'):
    decypted_archive = io.BytesIO()
    with open(arhive_name, 'rb') as f:
        length = os.path.getsize(arhive_name)
        pyAesCrypt.decryptStream(f, decypted_archive, password, 64 * 1024, length)
    decypted_archive.seek(0)
    with ZipFile(decypted_archive) as myzip:
        with myzip.open("files.txt") as f:
            files = f.read().decode().splitlines()
    return files

def get_files_count(archive_name, password='password'):
    return len(get_filesx(archive_name, password))

def unpack_archive(archive_name):
    with ZipFile(archive_name, 'r') as myzip:
        myzip.extractall()
    os.remove(archive_name)

def extract_frames(video_name, folder):
    #TODO extract directly from encypted archive
    if folder.strip() == '' or folder.strip() == '.':
        folder = 'test'
    if not os.path.exists(folder):
        os.makedirs(folder)
    cap = cv2.VideoCapture(video_name)
    with open("files.txt", mode='r') as f:
        for line in tqdm.tqdm(f, desc='extracting images'):
            line = line.strip()
            info = line.split('|')
            e, img = cap.read()
            if e:
                img = cv2.resize(img, (int(info[2]), int(info[1])))
                cv2.imwrite(os.path.join(folder,info[0]), img)
            else:
                cap.release()
                break 
    try: cap.release()
    except: pass
    os.remove(video_name)
    os.remove("files.txt")
def make_archive(archive_name: str, folder_name: str, password=None, output_folder='.', kmeans=False, k_number=8):
    #check if folder exists, if not create it 
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    #get files
    if kmeans == False:
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
    if kmeans == True:
        k_sorted = sort(folder_name, k=k_number)
        nfolders = int(math.log(k_number, 10))+1
        folder_name = os.path.join(folder_name, "out")
        files = []
        #create video
        video_name = "video.avi"
        create_video(folder_name, k_sorted, video_name, output_folder=output_folder, kmeans=True)
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


def repack_pre_0_3_archive(archive_name, folder_name, password=None):
    decypted_archive = io.BytesIO()
    with open(archive_name, 'rb') as f:
        length = os.path.getsize(archive_name)
        pyAesCrypt.decryptStream(f, decypted_archive, password, 64 * 1024, length)
    decypted_archive.seek(0)
    with ZipFile(decypted_archive) as myzip:
        with myzip.open("files.txt") as f:
            files = f.read().decode().splitlines()
    #get the resolution of the video inside the archive without extracting video
    with ZipFile(decypted_archive, 'r') as myzip:
        with myzip.open("video.avi") as f:
            frames = imread(f.read(), index=None, format_hint='.avi')
            resolution = frames[0][0:1].shape
    with ZipFile(decypted_archive, mode='w') as myzip:
        with myzip.open("files.txt", mode='w') as f:
            for i in files:
                f.write(f"{i}|{resolution[0]}|{resolution[1]}\n")




if __name__ == "__main__":
    
    make_archive("test.zip", "catz", password='password', kmeans=True)
    #repack_pre_0_3_archive("test.zip.aes", "test", password="test")
    #decrypt_archive("test.zip", password="password")
    open_archive("test.zip", "test", password='password')
    #print(get_files_count("test.zip.aes", password="password"))

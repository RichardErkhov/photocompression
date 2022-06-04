#https://github.com/victorqribeiro/groupImg
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
import math
import warnings
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count

Image.MAX_IMAGE_PIXELS = None
warnings.simplefilter('ignore')

class K_means:

  def __init__(self, k=3, size=False, resample=32):
    self.k = k
    self.cluster = []
    self.data = []
    self.end = []
    self.i = 0
    self.size = size
    self.resample = resample

  def manhattan_distance(self,x1,x2):
    s = 0.0
    for i in range(len(x1)):
      s += abs( float(x1[i]) - float(x2[i]) )
    return s

  def euclidian_distance(self,x1,x2):
    s = 0.0
    for i in range(len(x1)):
      s += math.sqrt((float(x1[i]) - float(x2[i])) ** 2)
    return s

  def read_image(self,im):
    if self.i >= self.k :
      self.i = 0
    try:
      img = Image.open(im)
      osize = img.size
      img.thumbnail((self.resample,self.resample))
      v = [float(p)/float(img.size[0]*img.size[1])*100  for p in np.histogram(np.asarray(img))[0]]
      if self.size :
        v += [osize[0], osize[1]]
      #pbar.update(1)
      i = self.i
      self.i += 1
      return [i, v, im]
    except Exception as e:
      print("Error reading ",im,e)
      return [None, None, None]


  def generate_k_means(self):
    final_mean = []
    for c in range(self.k):
      partial_mean = []
      for i in range(len(self.data[0])):
        s = 0.0
        t = 0
        for j in range(len(self.data)):
          if self.cluster[j] == c :
            s += self.data[j][i]
            t += 1
        if t != 0 :
          partial_mean.append(float(s)/float(t))
        else:
          partial_mean.append(float('inf'))
      final_mean.append(partial_mean)
    return final_mean

  def generate_k_clusters(self,folder):
    pool = ThreadPool(cpu_count())
    result = pool.map(self.read_image, folder)
    pool.close()
    pool.join()
    self.cluster = [r[0] for r in result if r[0] != None]
    self.data = [r[1] for r in result if r[1] != None]
    self.end = [r[2] for r in result if r[2] != None]

  def rearrange_clusters(self):
    isover = False
    while(not isover):
      isover = True
      m = self.generate_k_means()
      for x in range(len(self.cluster)):
        dist = []
        for a in range(self.k):
          dist.append( self.manhattan_distance(self.data[x],m[a]) )
        _mindist = dist.index(min(dist))
        if self.cluster[x] != _mindist :
          self.cluster[x] = _mindist
          isover = False
def sort(folder, k=3, size=False, resample=256, move=False):
    #ap = argparse.ArgumentParser()
    #ap.add_argument("-f", "--folder", required=True, help="path to image folder")
    #ap.add_argument("-k", "--kmeans", type=int, default=5, help="how many groups")
    #ap.add_argument("-r", "--resample", type=int, default=128, help="size to resample the image by")
    #ap.add_argument("-s", "--size", default=False, action="store_true", help="use size to compare images")
    #ap.add_argument("-m", "--move", default=False, action="store_true", help="move instead of copy")
    
    #args = vars(ap.parse_args())
    types = ('*.jpg', '*.JPG', '*.png', '*.jpeg')
    imagePaths = []
    folder = folder
    if not folder.endswith("/") :
        folder+="/"
    for files in types :
        imagePaths.extend(sorted(glob.glob(folder+files)))
    nimages = len(imagePaths)
    nfolders = int(math.log(k, 10))+1
    if nimages <= 0 :
        print("No images found!")
        exit()
    if resample < 16 or resample > 256 :
        print("-r should be a value between 16 and 256")
        exit()
    #pbar = tqdm(total=nimages)
    k = K_means(k,size,resample)
    k.generate_k_clusters(imagePaths)
    k.rearrange_clusters()
    for i in range(k.k) :
        try :
            os.makedirs(folder+"out/"+str(i+1).zfill(nfolders))
        except :
            print("Folder already exists")
    action = shutil.copy
    if move :
        action = shutil.move
    for i in range(len(k.cluster)):
        action(k.end[i], folder+"/out/"+str(k.cluster[i]+1).zfill(nfolders)+"/")
    
def get_files(folder):
    files = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            files.append(os.path.join(filename))
    return files

def create_video(folder, files, video_name, output_folder='.', kmeans=False):
    with open(os.path.join(output_folder, "files.txt"), mode='w') as f:
        out = skvideo.io.FFmpegWriter(os.path.join(output_folder,video_name), outputdict={
  '-vcodec': 'libx264',  #use the h.264 codec
  '-crf': '0',           #set the constant rate factor to 0, which is lossless
  '-preset':'veryslow'   #the slower the better compression, in princple, try 
                         #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
}) 
        if kmeans == False:
            for filename in tqdm.tqdm(files, desc="compressing files"):
                img = cv2.imread(os.path.join(folder,filename))
                f.write(filename + "\n")
                out.writeFrame(img[:,:,::-1])
        else:
            was = []
            for i in os.listdir(folder):
                if os.path.isdir(os.path.join(folder,i)):
                    for filename in tqdm.tqdm(os.listdir(os.path.join(folder,i)), desc="compressing files"):
                        if filename not in was:
                            img = cv2.imread(os.path.join(folder,i,filename))
                            f.write(filename + "\n")
                            out.writeFrame(img[:,:,::-1])
                            was.append(filename)
        
        out.close()
    
def create_archive(video_name, archive_name, output_folder='.'):
    if not archive_name.endswith(".zip"): 
        archive_name += ".zip"
    with zipfile.ZipFile(os.path.join(output_folder, archive_name), 'w') as myzip:
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
    if folder.strip() == '' or folder.strip() == '.':
        folder = 'test'
    if not os.path.exists(folder):
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
        sort(folder_name, k=k_number)
        nfolders = int(math.log(k_number, 10))+1
        folder_name = os.path.join(folder_name, "out")
        files = []
        for i in range(1,k_number+1):
            files += get_files(os.path.join(folder_name, str(i).zfill(nfolders)))
        #create video
        video_name = "video.avi"
        create_video(folder_name, files, video_name, output_folder=output_folder, kmeans=True)
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
        #os.remove(os.path.join(folder_name))
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
    make_archive("test.zip", "catz", password='password', kmeans=False)
    open_archive("test.zip", "test", password='password')
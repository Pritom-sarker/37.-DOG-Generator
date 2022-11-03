from flask import Flask
from flask import send_file
import os
import glob
import shutil
import random
from PIL import Image
import json
import pandas as pd
from flask import Flask, request, jsonify
app = Flask(__name__)

def createLayerConfig(folder_name ):
   files = glob.glob('./{}/*/*.png'.format(folder_name ))
   layer_data = []
   layers = []
   for file in files:
      temp = file.split(os.sep)
      if temp[2] not in layers:
         layers.append(temp[2])
      layer_data.append([temp[2], file, (str(temp[-1]).split('#')[-1][:-4])])

   final_file = {}
   for layer in layers:
      files = []
      weight = []
      for data in layer_data:
         if layer in data:
               files.append(data[1])
               weight.append(int(data[2]))

      final_file[layer] = [files, weight]
   return final_file

def createImage(pathArray,fileName):
    newsize = (4000, 4000)
    im1 = Image.open(pathArray[0]).convert('RGBA').resize(newsize)
    im2 = Image.open(pathArray[1]).convert('RGBA').resize(newsize)
    com = Image.alpha_composite(im1, im2)
    for path in range(2,len(pathArray)):
        imgData = Image.open(pathArray[path]).convert('RGBA').resize(newsize)
        com = Image.alpha_composite(com, imgData)

    rgb_im = com.convert('RGB')
    rgb_im.save("./img/{}.png".format(fileName))

def getName(url):
    s = str(url).split(os.sep)
    s =  s[-1].split('#')
    return s[0]

def writeMetaData(jsn,name):
    f = open('./metadata/{}.json'.format(name),'w')
    f.write(json.dumps((jsn), indent = 4))
    f.close()

def getOtherAttr(name):
    global values
    data = []
    for val in values:
        if val[0].lower() in name.lower():
            for v in val[1:]:
                data.append(random.randint(int(v.split('-')[0]),int(v.split('-')[1])))
            return data

    return data


def generate_stats(dog_breed):
    global contractStat,values
    
    stats = {}
    stats[contractStat[0]]=100
    stats[contractStat[1]] = random.randint(int(str(values[dog_breed][0]).split('-')[0]),int(str(values[dog_breed][0]).split('-')[1]))
    stats[contractStat[2]] = random.randint(int(str(values[dog_breed][1]).split('-')[0]),int(str(values[dog_breed][1]).split('-')[1]))
    stats[contractStat[3]] = random.randint(int(str(values[dog_breed][2]).split('-')[0]),int(str(values[dog_breed][2]).split('-')[1]))
    stats[contractStat[4]] = 100
    stats[contractStat[5]] = (stats[contractStat[1]] + stats[contractStat[2]])/2
    stats[contractStat[6]] = (stats[contractStat[1]] + stats[contractStat[5]])*2
    stats[contractStat[7]] = random.randint(int(str(values[dog_breed][3]).split('-')[0]),int(str(values[dog_breed][3]).split('-')[1]))
    stats[contractStat[8]] = stats[contractStat[2]] + stats[contractStat[5]] + stats[contractStat[3]] + stats[contractStat[0]] 
    stats[contractStat[9]] = stats[contractStat[1]] + stats[contractStat[4]] + stats[contractStat[5]] + stats[contractStat[6]]

    return stats
   
@app.route('/', methods=['GET'])
def index():
   return "Server Is working!!"

@app.route('/get_image', methods=['GET'])
def get_image():
   id_ = request.args.get("id")
   filename = './img/{}.png'.format(id_)
   return send_file(filename, mimetype='image/gif')

@app.route('/get_stats', methods=['GET'])
def get_stats():
   global all_stats
   id_ = request.args.get("id")
   file = all_stats[int(id_)]
   return file

@app.route('/get_metadata', methods=['GET'])
def get_metadata():
   global all_stats
   id_ = request.args.get("id")
   file = all_metadata[int(id_)]
   return file

@app.route('/mint', methods=['GET']) 
def mint():
   global img,allUniqueHash,all_metadata
   Breed = request.args.get("breed")
   Gender = request.args.get("gender")
   print(Breed,Gender)
   layers_data = createLayerConfig('{}_{}'.format(Breed,Gender))
   # print( layers_data)
   layers =  ['Background','Soul Ring','Color','Belly','Pattern','Soul Particle','Soul Beam']
   while True:
      # try:
         print('Number Of Image: ', img)
         imgPathArray = []
         stringOfImgPath = ''
         attrData = []
         data = []
         for layer in layers:
               weight = list(layers_data[layer][1])
               files = list(layers_data[layer][0])
               imgFileName = random.choices(files, weight,k=len(weight))[0]
               imgPathArray.append(imgFileName)
               stringOfImgPath +=  imgFileName
               attrData.append({"trait_type":layer,"value": getName(imgFileName)})


         if hash(stringOfImgPath) in allUniqueHash:
               print('Same! Img')
               continue
         else:
               allUniqueHash.append(hash(stringOfImgPath))
         metaData = {}
         metaData["Name"] = "Dog #{}".format(img)
         metaData["Description"] = "Its a dog- DoRac greyhounds used for races and other good stuff in DoRacVerse"
         metaData["image"] = "{}.png".format(img)
         metaData["attributes"] = attrData
         data.append('{}.json'.format(img))
         data.append('{}.png'.format(img))
         all_data.append(data)
         all_metadata[img]= metaData
         all_stats[img] = generate_stats(Breed)
         createImage(imgPathArray, img)
         img+=1
         break
   return str(img-1)



if __name__ == '__main__':
       # Put Layer names in sequence
       
   img = 0
   all_metadata = {}
   all_stats = {}
   all_data = []
   allUniqueHash = []
   layers= ['Background','Soul Ring','Color','Belly','Pattern','Eyes','Soul Particle','Soul Beam']
   contractStat = ['Health','Agility','strength','weight','Stamina','Power','Endurance','Luck','Toughness','Swiftness']
   values ={'falon':['22-26','12-14','14-18','6-22'],
            'belphegor':['21-25','11-13','13-17','7-22'],
            'cinder': ['19-23','11-13','12-16','10-12','8-21'],
            'bess':['18-22','9-11','11-15','9-21']
         ,'barto':['16-20','8-10','10-14','10-20'],
         'scruffy':['15-19','7-9','9-13','11-20']}
   try:
      shutil.rmtree('img')
   except:
      pass
   try:
      os.mkdir('img')
   except:
      pass
   try:
      shutil.rmtree('metadata')
   except:
      pass
   try:
      os.mkdir('metadata')
   except:
      pass
   

   app.run(host='192.248.172.104', port=80)
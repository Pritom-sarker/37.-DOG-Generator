import os
import glob
import shutil
import random
from PIL import Image
import json
import pandas as pd


def createLayerConfig(folder_name,gender,typee):
    print('./{}/{}/{}/*/*.png'.format(folder_name,gender,typee))
    files = glob.glob('./{}/{}/{}/*/*.png'.format(folder_name,gender,typee))
    layer_data = []
    layers = []
    for file in files:
        temp = file.split(os.sep)
        if temp[2] not in layers:
            layers.append(temp[1])
        layer_data.append([temp[1], file, (str(temp[-1]).split('#')[-1][:-4])])

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
    s = str(url).split('\\')
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

# strength varies from breed to breed but is not calculated from other stats
# Health is hard value - 100
# weight varies - per breed but is not calculated from any other stat
# agility varies from breed to breed but is not calculated from other stats
# Stamina is hard value for all - 100
# endurance - is calculated: (agility+power)*2
# power - is calculated: (agility+strenght) /2
# Luck is hard value 

# plus 
# Toughness - strength + health + stamina + power
# Swiftness - agility+stamina+power+endurance



def generate_stats(dog_breed):
    global contractStat,values
    
    stats = {}
    
    stats[contractStat[0]]=100
    stats[contractStat[1]] = random.randint(str(values[dog_breed][0]).split('-')[0],str(values[dog_breed][0]).split('-')[1])
    stats[contractStat[2]] = random.randint(str(values[dog_breed][1]).split('-')[0],str(values[dog_breed][1]).split('-')[1])
    stats[contractStat[3]] = random.randint(str(values[dog_breed][2]).split('-')[0],str(values[dog_breed][2]).split('-')[1])
    stats[contractStat[4]] = 100
    stats[contractStat[5]] = (stats[contractStat[1]] + stats[contractStat[2]])/2
    stats[contractStat[6]] = (stats[contractStat[1]] + stats[contractStat[5]])*2
    stats[contractStat[7]] = random.randint(str(values[dog_breed][3]).split('-')[0],str(values[dog_breed][3]).split('-')[1])
    stats[contractStat[8]] = stats[contractStat[2]] + stats[contractStat[0]] + stats[contractStat[4]] + stats[contractStat[5]] 
    stats[contractStat[9]] = stats[contractStat[1]] + stats[contractStat[4]] + stats[contractStat[5]] + stats[contractStat[6]]
    
    
    

if __name__ == '__main__':

    # Put Layer names in sequence
    all_data = []
    layers= ['Background','Soul Ring','Color','Belly','Pattern','Eyes','Soul Particle','Soul Beam']
    contractStat = ['Health','Agility','strength','weight','Stamina','Power','Endurance','Luck','Toughness','Swiftness']
    values ={'Falon':['22-26','12-14','14-18','6-22'],
             'Belphegor':['21-25','11-13','13-17','7-22'],
             'Cinder': ['19-23','11-13','12-16','10-12','8-21'],
             'Bess':['18-22','9-11','11-15','9-21']
            ,'Barto':['16-20','8-10','10-14','10-20'],
            'Scruffy':['15-19','7-9','9-13','11-20']}
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




    layers_data = createLayerConfig('First-Draft','Male','Belphegor')

    allUniqueHash = []
    img = 0
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
                if layer == 'Color':
                    data = getOtherAttr(getName(imgFileName))


            if hash(stringOfImgPath) in allUniqueHash:
                print('Same! Img')
                continue
            else:
                allUniqueHash.append(hash(stringOfImgPath))
            
            img+=1
            metaData = {}
            metaData["Name"] = "Dog #{}".format(img)
            metaData["Description"] = "Hello world!!"
            metaData["image"] = "{}.png".format(img)
            metaData["attributes"] = attrData
            data.append('{}.json'.format(img))
            data.append('{}.png'.format(img))
            all_data.append(data)
            writeMetaData(metaData,img)
            createImage(imgPathArray, img)

            
            break



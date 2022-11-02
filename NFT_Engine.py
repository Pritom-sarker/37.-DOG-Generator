import os
import glob
import shutil
import random
from PIL import Image
import json
import pandas as pd


def createLayerConfig(folder_name):
    files = glob.glob('./{}/*/*.png'.format(folder_name))
    layer_data = []
    layers = []
    for file in files:
        temp = file.split(os.sep)
        if temp[1] not in layers:
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
    im1 = Image.open(pathArray[0]).convert('RGBA')
    im2 = Image.open(pathArray[1]).convert('RGBA')
    com = Image.alpha_composite(im1, im2)
    for path in range(2,len(pathArray)):
        imgData = Image.open(pathArray[path]).convert('RGBA')
        com = Image.alpha_composite(com, imgData)

    rgb_im = com.convert('RGB')
    rgb_im.save("./img/{}.png".format(fileName))


def getName(url):
    s = str(url).split('/')
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




if __name__ == '__main__':

    # Put Layer names in sequence
    all_data = []
    layers = ['Background','Bloodline','Belly','Pattern','Eyes','Nose','Claws','Ears','SoulBeams','Rune','Fog']
    values =[['Falon','9-20','20-24','11-13'],['Belphegor','9-20','18-22','10-12'],['Cinder','7-20','14-16','9-11'],['Bess','7-20','13-15','8-10']
        ,['Barto','5-20','11-13','7-9'],['Scruffy','5-20','10-12','6-8']]
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




    layers_data = createLayerConfig('First-Draft')
    #print(layers_data)
    allUniqueHash = []
    numOfImage = 500
    img = 0
    layers = ['Background','Bloodline','Belly','Pattern','Eyes','Nose','Claws','Ears','SoulBeams','Rune','Fog']
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

            if img == numOfImage:
                break
        # except:
        #     print("error!!")

    df = pd.DataFrame(all_data,columns=['luck','agility','weight','File','img'])
    df.to_csv('mintingData.csv')



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




if __name__ == '__main__':

    # Put Layer names in sequence
    all_data = []
    layers= ['Background','Soul Ring','Color','Belly','Pattern','Eyes','Soul Particle','Soul Beam']
    values =[['Falon','6-22','22-26','14-18','12-14','8-10','61-72','143-152','217-238'],['Belphegor','7-22','21-25','13-17','11-13','8-9','58-69','140-149','211-232'],['Cinder','8-21','19-23','12-16','10-12','7.25-8.75','52.5-63.5','138-147','202-223'],['Bess','9-21','18-22','11-15','9-11','6.75-8.25','49.5-60.5','133.50-142.50','194.50-215.50']
        ,['Barto','10-20','16-20','10-14','8-10','6-7.5','44-55','130-139','184-205'],['Scruffy','11-20','15-19','9-13','7-9','5.5-7','41-52','127-136','178-199']]
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
    numOfImage = 500
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

            if img == numOfImage:
                break
        # except:
        #     print("error!!")

    df = pd.DataFrame(all_data,columns=['Luck','Agility','Weight','Strenght','Power','Endurance','Toughness','Swiftness','File','img'])
    df.to_csv('mintingData.csv')



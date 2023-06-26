#Creating a Synthetic data of a Check leaf
#The packages needed
from PIL import Image , ImageDraw , ImageFont
from bs4 import BeautifulSoup
import glob
import shutil
import os
import sys
import getopt
from faker import Faker
import random
import inflect
from random import randint
import datetime

templates = ['./templates/bankofamerica.jpg','./templates/jpmorgan_chase.jpg']
templates_xml = ['./templates/bankofamerica.xml','./templates/jpmorgan_chase.xml']
output_folder = "./output_images"

#to get 10 Different outputs
def generate_images(templates, templates_xml):
    for template, template_xml in zip(templates , templates_xml):
        print ("template :", template)
        img = Image.open(template)
        input_file = template.split("/")[2]
        input_filename = input_file.split(".")[0]
        xml_file ="./templates/"+input_filename+'.xml'
        bboxes = get_coordinates(xml_file)
        
        for i in range(1,21):
            output_filename = output_folder+ "/"+ input_filename +'_' + str(i)+'.jpg'
            img = Image.open(template)
           
            img, name = get_name(img,bboxes)
            img, display_amount_number = get_amount_in_number(img,bboxes)
            img = get_amount_in_text(img, display_amount_number, bboxes)
            img = get_address(img, bboxes)
            img = get_date(img,bboxes)
            img = get_signature(img,bboxes,name)
            img = get_memo(img , bboxes)
            img.save(output_filename)
            img.close()
        
#to get the Coordinates of the bounding boxes after annotating
def get_coordinates(xml_file):
    bboxes =[]
    
    with open(xml_file ,"r") as f:
        data = f.readlines()
        data = " ".join(data)
        bs_data = BeautifulSoup(data,"lxml")

    names = bs_data.find_all('name')
    bndboxes = bs_data.find_all('bndbox')

    for name , bndbox in zip(names , bndboxes):
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        print(name.text,xmin,ymin,xmax,ymax)

        bboxes.append([name.text,[xmin,ymin,xmax,ymax]])
    return bboxes

#To get the name using random inside the sign file folder
def get_name(img, bndboxes):
    
    title_font = ImageFont.truetype('Playfair.ttf', 50)
    folder = r"/home/laal/PROJECTS/synthetic data/synthetic_dataset_check/sign_file"
    name = random.choice(os.listdir(folder))
    display_name_1 = name.split("_")[0]
    display_name_2 = name.split("_")[1]
    display_name_3 = display_name_2.split(".")[0]
    display_name_on_image = display_name_1+" "+display_name_3
    for item in bndboxes:
        if item[0] == 'display_name':
            title_text = "**"+" "+display_name_on_image+" "+"**"
            image_edit = ImageDraw.Draw(img)
            xmin = item[1][0]
            ymin = item[1][1]
            xmax = item[1][2]
            ymax = item[1][3]
            image_edit.text([xmin,ymin,xmax,ymax], title_text, (0, 0, 0), font=title_font)
    #img.save(image_name)
    return img , name

#To get a random amount 
def get_amount_in_number(img, bndboxes):
    #img = Image.open(image_name)
    title_font = ImageFont.truetype('Playfair.ttf', 50)
    display_amount = random.randint(500,2000)
    display_amount_number = str(display_amount)+'.00'
    for item in bndboxes:
        if item[0] == 'amount_in_numbers':
            title_text = "**"+" "+ display_amount_number +" "+"**"
            image_edit = ImageDraw.Draw(img)
            xmin = item[1][0]
            ymin = item[1][1]
            xmax = item[1][2]
            ymax = item[1][3]
            image_edit.text([xmin,ymin,xmax,ymax], title_text, (0, 0, 0), font=title_font)
    #img.save("result.jpg")
    return img, display_amount

#To get the text of the amount given in numbers
def get_amount_in_text(img, display_amount_number, bndboxes):
    p = inflect.engine()
    #img = Image.open(image_name)
    title_font = ImageFont.truetype('Playfair.ttf', 50)
    amount_text = p.number_to_words(display_amount_number).replace(",","")
    display_amount_text = amount_text.title()
    for item in bndboxes:
        if item[0] == 'amount_in_text':
            title_text = "**"+" "+ display_amount_text+" "+"**"
            image_edit = ImageDraw.Draw(img)
            xmin = item[1][0]
            ymin = item[1][1]
            xmax = item[1][2]
            ymax = item[1][3]
            image_edit.text([xmin,ymin,xmax,ymax], title_text, (0, 0, 0), font=title_font)
    #img.save("result.jpg")
    return img

#To get a random address using faker
def get_address(img , bndboxes):
    #img = Image.open(image_name)
    title_font = ImageFont.truetype('Playfair.ttf', 50)
    faker = Faker()
    display_address_text = faker.address()
    for item in bndboxes:
        if item[0] == 'display_address':
            title_text = display_address_text
            image_edit = ImageDraw.Draw(img)
            xmin = item[1][0]
            ymin = item[1][1]
            xmax = item[1][2]
            ymax = item[1][3]
            image_edit.text([xmin,ymin], title_text, (0, 0, 0), font=title_font)
    #img.save("result.jpg")
    return img

#to get a random date
def get_date(img , bndboxes):
    #img = Image.open(image_name)
    today_date = datetime.datetime.now()
    till_date = random.randint(10,500)
    delta_date = datetime.timedelta(till_date)
    difference = today_date - delta_date
    display_date = difference.strftime("%m-%d-%Y")
    #display_date=str(datetime.date(randint(2010,2020), randint(1,12),randint(1,30)))
    title_font = ImageFont.truetype('Playfair.ttf', 50)
    
    for item in bndboxes:
        if item[0] == 'date':
            title_text = display_date
            image_edit = ImageDraw.Draw(img)
            xmin = item[1][0]
            ymin = item[1][1]
            xmax = item[1][2]
            ymax = item[1][3]
            image_edit.text([xmin,ymin,xmax,ymax], title_text, (0, 0, 0), font=title_font)
    #img.save("result.jpg")
    return img

#To paste the signature file if the name printed matched the file name
def get_signature(img, bndboxes , name):
    
    file_name = "./sign_file/"+name
    image = Image.open(file_name)
    
    for item in bndboxes:
        if item[0] == 'signature':
            xmin = item[1][0]
            ymin = item[1][1]
            xmax = item[1][2]
            ymax = item[1][3]
    width = xmin
    height = ymin 
    img.paste(image,(width,height),image)
    #img.save("result.png" , format ="png")
    return img

#To get the memo for the check
def get_memo(img,bndboxes):
    memo_of_check = ['School Fee','College Fee','Gardening Bill','Gift','Salary','Hostle Fee','Increment','Bonus','Contract Payment','Vehicle']
    display_memo = random.choice(memo_of_check)
    title_font = ImageFont.truetype('Playfair.ttf', 50)
    for item in bndboxes:
        if item[0] == 'memo':
            title_text = "**"+" "+display_memo+" "+"**"
            image_edit = ImageDraw.Draw(img)
            xmin = item[1][0]
            ymin = item[1][1]
            xmax = item[1][2]
            ymax = item[1][3]
            image_edit.text([xmin,ymin,xmax,ymax], title_text, (0, 0, 0), font=title_font)
    return img

generate_images(templates, templates_xml)





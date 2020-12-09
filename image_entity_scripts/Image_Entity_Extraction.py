# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:28:23 2020

@author: Vikas Gupta
"""

import os
import re
import pandas as pd
from flair.models import SequenceTagger
from flair.data import Sentence

from Python_Images_Text import imageprocessing
from Python_Images_Text import imageprocessing_canny
from Python_Images_Text import imageprocessing_

tagger = SequenceTagger.load("ner-ontonotes-fast")

non_decimal = re.compile(r'[^\d.+-\\s:;]+')
person_name_regex = re.compile(r'(<B-PERSON>.*<E-PERSON>)')
organisation_name_regex = re.compile(r'(<B-ORG>.*<E-ORG>)')

phone_number = []
email_list = []
file_names = []
name = []
organisation_name = []

def name_extraction(line):
    person_name = ""
    line = line.title()
    if (line.strip() != ""):
        sentence = Sentence(line.title())
        tagger.predict(sentence)
        tagged_name = sentence.to_tagged_string()
        tagged_data = tagged_name.split()
        if ("<B-PERSON>" in tagged_name):
            Starting_Index = tagged_data.index("<B-PERSON>")
            person_name = person_name_regex.search(tagged_name)
            person_name_text = person_name.group(0)
            Person_Name = tagged_data[Starting_Index - 1] + " " +  person_name_text
            Person_Name = re.sub( r"<.*?>", "", Person_Name)
            # if "<B-PERSON>" in tagged_name:
            #     person_name = line
            return Person_Name
    

def organisation_extraction(line):
    organisation_name = ""
    line = line.title()
    if (line.strip() != ""):
        sentence = Sentence(line.title())
        tagger.predict(sentence)
        tagged_name = sentence.to_tagged_string()
        tagged_data = tagged_name.split()
        if ("<B-ORG>" in tagged_name):
            Starting_Index = tagged_data.index("<B-ORG>")
            organisation_name =  organisation_name_regex.search(tagged_name)
            organisation_name_text =  organisation_name.group(0)
            Organisation_Name = tagged_data[Starting_Index - 1] + " " +  organisation_name_text
            Organisation_Name = re.sub( r"<.*?>", "", Organisation_Name)
            # if "<B-PERSON>" in tagged_name:
            #     person_name = line
            return Organisation_Name

def email_extraction(line):
    email_regex=re.compile(r'(([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+)\.[a-zA-Z0-9-.]+)')
    email_text = email_regex.search(line)
    if (email_text):
        email = email_text.group(0).replace(") ", "")
        organisation = email_text.group(3)
        return email, organisation
    
def phone_number_extraction(line):
    #phone_number_regex = re.compile(r'((\+91)(\s|\-)(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$)|((\d{3})-(\d{3})-(\d{4})$)|^((\d{3})-(\d{3})-(\d{4})-(\d+)$)|^((\d{3})\D*(\d{3})\D*(\d{4}))|^((\d{3})\D+(\d{3})\D+(\d{4})\D+(\d+)$)|^((\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$)|^(\D*(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$)|((\d{2})\D*(\d{4})\D*(\d{4})\D*(\d*)$)|((\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$)|((\d{4})\D*(\d{3})\D*(\d{3})\D*(\d*)$)|((\+46\(0\))(\d{3})-(\d{3})(-|\s)(\d{2}))|((\+46\(0\))(\d{2})-(\d{3})(-|\s)(\d{2}(-|\s)(\d{2})))', re.IGNORECASE)
    phone_number_regex = re.compile(r'((\+46\(0\))(\d{3})-(\d{3})(-|\s)(\d{2}))|((\+46\(0\))(\d{2})-(\d{3})(-|\s)(\d{2}(-|\s)(\d{2})))|((\+65|65|\(65\)|010|011)(\s|\-)(([0-9]{4})(\D|\s)([0-9]{4})|[0-9]{8}))|((((\+(\s)?(91|33|1))(-|\s|\.|\s-\s))|((91|33|1)(-|\s|\.))|((\+91|33|1)))(([0-9]{10})|(([\(0-9\)]{2,4})\D([0-9]{2,4})\D*([0-9]{3,4}))|(\s[0-9]{10})|([\(0-9\)]{2,5}(\D|\s)[0-9]{5,8})|([0-9]{7}(\D|\s)[0-9]{3})))|([0-9]{10})|([0-9]{5}\D[0-9]{5})')
    phone_number_text = phone_number_regex.search(line)
    if (phone_number_text):
        phone = phone_number_text.group(0)
        return phone
        
def entityextraction(filename_list):
    for filename in filename_list:
        Image_File_Name = filename.split("\\n")[-1]
        print (Image_File_Name)
        phone_numbers = []
        emails = []
        names = []
        organisation_names = []
        file_data = imageprocessing(filename).split("\n")
        file_data_denoised = imageprocessing_canny(filename).split("\n")
        file_data_denoised_ = imageprocessing_(filename).split("\n")
        Count = 0
        for line in file_data:
            if (line.strip() != ""):
                if (name_extraction(line)) and Count == 0:
                    Count += 1
                    names.append(name_extraction(line))
                if (organisation_extraction(line)):
                    organisation_names.append(organisation_extraction(line))
                elif (email_extraction(line)):
                    organisation_names.append(email_extraction(line)[1])
            line = line.replace(",",".")
            if (email_extraction(line)):
                emails.append(email_extraction(line)[0])
            if (phone_number_extraction(line)):
                phone_numbers.append(phone_number_extraction(line))
        if (len(emails)== 0):
            for line in file_data_denoised:
                if (email_extraction(line)):
                    emails.append(email_extraction(line)[0])
        if (len(phone_numbers)== 0):
            for line in file_data_denoised:
                if (phone_number_extraction(line)):
                    phone_numbers.append(phone_number_extraction(line))
        if (len(emails)== 0):
            for line in file_data_denoised_:
                if (email_extraction(line)):
                    emails.append(email_extraction(line)[0])
        if (len(phone_numbers)== 0):
            for line in file_data_denoised_:
                if (phone_number_extraction(line)):
                    phone_numbers.append(phone_number_extraction(line))
        if (len(names) == 0):
            for line in file_data_denoised:
              if (line.strip() != ""):
                 if (name_extraction(line)) and Count == 0:
                    Count += 1
                    names.append(name_extraction(line)) 
        if (len(names) == 0):
            for line in file_data_denoised_:
              if (line.strip() != ""):
                 if (name_extraction(line)) and Count == 0:
                    Count += 1
                    names.append(name_extraction(line))
        if (len(organisation_names) == 0):
            for line in file_data_denoised:
                if (organisation_extraction(line)):
                    organisation_names.append(organisation_extraction(line))
                elif (email_extraction(line)):
                    organisation_names.append(email_extraction(line)[1])
        if (len(organisation_names) == 0):
            for line in file_data_denoised_:
                if (organisation_extraction(line)):
                    organisation_names.append(organisation_extraction(line))
                elif (email_extraction(line)):
                    organisation_names.append(email_extraction(line)[1])
        file_names.append(Image_File_Name)
        cleaned_phone_numbers = ", ".join(phone_numbers)
        cleaned_emails = ", ".join(emails)
        cleaned_name = ", ".join(names)
        cleaned_organisation_name = ", ".join(organisation_names)
        phone_number.append(cleaned_phone_numbers)
        email_list.append(cleaned_emails)
        name.append(cleaned_name)
        organisation_name.append(cleaned_organisation_name.title())
    df = pd.DataFrame({'File Names': file_names})
    df1 = pd.DataFrame({'Contact Information': phone_number})
    df2 = pd.DataFrame({'Email ID':email_list})
    df3 = pd.DataFrame({'Names':name})
    df4 = pd.DataFrame({'Organisation Names':organisation_name})
    writer = pd.ExcelWriter(outputlocation + "/" +"Image_Metadata" + ".xlsx")
    df.to_excel(writer, sheet_name='Sheet1',index=False,startcol=0)
    df1.to_excel(writer, sheet_name='Sheet1',index=False,startcol=1)                
    df2.to_excel(writer, sheet_name='Sheet1',index=False,startcol=2)
    df3.to_excel(writer, sheet_name='Sheet1',index=False,startcol=3)
    df4.to_excel(writer, sheet_name='Sheet1',index=False,startcol=4)
    writer.save()

filename_list = []

inputlocation = input("please enter the location of image files.\n")
outputlocation = input("please enter the location of processed files.\n")
#Resized_Images_Location = input("please enter the location of resized files.\n")

def gettingfiles():
    for dirpath,dirname,filenames in os.walk(inputlocation):
        for file in filenames:
            try:
                if(file.endswith('.jpg') or (file.endswith('.jpeg'))):
                    path=(os.path.abspath(os.path.join(dirpath,file)))
                    filename_list.append(path)
                else:
                    continue
            except (FileNotFoundError, IOError):
                print("runtime exception")
    return filename_list

gettingfiles()
entityextraction(filename_list)
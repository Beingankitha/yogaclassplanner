from cgi import print_arguments
from django.http import HttpResponse
from django.shortcuts import render,get_list_or_404
from yogas.models import Asana, AsanaImages,YogaImage
from os import listdir
from os.path import isfile, join
from django.contrib.staticfiles.storage import staticfiles_storage

def add_images(request):
    mypath = "/home/ankita/wc1/code/trunk/yogaclassplanner/static/images/yogas/"
    
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    asanas = Asana.objects.all()
    for asan in asanas:
        my_large_list=[]
        my_small_list=[]
        for item in onlyfiles:
            new_name = item.replace('-','')
            import re
            match = re.match(r"([a-z]+)([0-9]+)", new_name, re.I)
            if match:
                itemss = match.groups()
                # print(itemss[0])
            asanaName = asan.asana_name.replace("-",'')
            if asanaName == itemss[0]:
                if "800" in item:
                    my_small_list.append(item)
                elif "1600" in item:
                    my_large_list.append(item)
        my_large_list.sort()
        my_small_list.sort()
        # if len(my_large_list) != len(my_small_list):
        #     print(asan.asana_name)
        # print(my_large_list)
        # print(my_small_list)
        for mynum in range(len(my_large_list)):
            asna_images = YogaImage()
            #yoga_images = YogaImage()
            #asna_images.asana_id = asan
            #yoga_images.asana_id = asan
            asna_images.asana = asan
            asna_images.images = mypath+my_small_list[mynum] 
            asna_images.save()

    return HttpResponse("Hi")


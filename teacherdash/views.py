
import datetime
import json
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from users.models import WebsiteUser, MedicalInformation
from classcalendar.models import YogaClass, ClassMember
from yogas.models import Asana, YogaImage, YogaDificulty, YogaPosition, YogaType, favouriteAsana
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from .forms import AsanaForm, YogaImageForm
from django.forms import inlineformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse


# Create your views here.
def teacherdash(request):
    if request.session.get("useremail") is not None:
        return render(request,"teacherdash.html")
    else:
        return redirect("/userlogin")
    
def teacherprofile(request):
    if request.session.get("useremail") is not None:
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        context = {'user':user}
        return render(request,"teacherprofile.html", context)
    else:
        return redirect("/userlogin")
    
def edituserprofile(request):
    if request.session.get("useremail") is not None:
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        postcode = user.address[-7:]       
        context = {'user':user, 'postcode':postcode}
        return render(request,"teachereditprofile.html", context)
    else:
        return redirect("/userlogin")
    
def saveuserprofile(request):
    if request.session.get("useremail") is not None:
        if request.method=="POST":
            user = WebsiteUser.objects.get(email=request.session.get("useremail"))
            email = request.POST["email"]
            fullname =request.POST["fullname"]
            gender =request.POST.get("gender", user.gender)
            Health_cond=request.POST["chk"]
            Hinfo=request.POST["txtBox"]
            fulladd=request.POST["fulladd"]
            
            if 'first_line' in request.POST:
                add = request.POST['first_line']
            elif 'second_line' in request.POST:
                add = add +' '+request.POST["second_line"]
            elif 'third_line' in request.POST:
                add = add +' '+request.POST["third_line"]
            elif 'post_town' in request.POST:
                add = add +' '+request.POST["post_town"]
            elif 'postcode' in request.POST:
                add = add +' '+request.POST["postcode"]
            
            if fulladd == add:
                fulladd = user.address
                
            print(fulladd)
            app = WebsiteUser.objects.filter(email=request.session.get("useremail")).update(email=email,fullname=fullname,gender=gender,address = fulladd, is_health=Health_cond, health_info = Hinfo)
            request.session["username"] = fullname.title()
            messages.success(request,"User Profile updated")
            return redirect('bypassurl')
        else:
            return render(request,"teacherprofile.html")
        
        
def bypassurl(request):
    if request.session.get("useremail") is not None:
        return redirect('teacherprofile')
    
def is_valid_query_param(param):
    return param != '' and param is not None

def tyogadictionary(request):
    if request.session.get("useremail") is not None:
        asanas = Asana.objects.all()
        asanas_sys = Asana.objects.filter(created_by = "system")
        asanas_usr = Asana.objects.filter(created_by = request.session.get("useremail"))
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        fav_asan = favouriteAsana.objects.all().filter(user=user)
        
        print(fav_asan)
        asanas_final =  []
        users_asan_Set = set()
        sys_asan_Set = set()
        for asanausr in asanas_usr:
            users_asan_Set.add(asanausr.asana_name)
        
        print(len(users_asan_Set))
        for asnaaa_ in asanas_sys:
            sys_asan_Set.add(asnaaa_.asana_name)
        print(len(sys_asan_Set))
        
        for asnaaa in asanas_sys:
            if asnaaa.asana_name in users_asan_Set:
                
                for asanausrr in asanas_usr:
                    # print("users asn is innnn ")
                    if asnaaa.asana_name == asanausrr.asana_name and asnaaa.created_by != asanausr.created_by:
                        asanas_final.append(asanausrr)
                    else:
                        pass
            else:
                # print("is ")
                asanas_final.append(asnaaa)
        
        for asnaaa_u in asanas_usr:
            if asnaaa_u.asana_name not in sys_asan_Set:
                # print("No in")
                asanas_final.append(asnaaa_u)   
                
                
        print(len(asanas_final))
        
        
        
        level = YogaDificulty.objects.all()
        position = YogaPosition.objects.all()
        type_ = YogaType.objects.all()
        
        if request.method == "GET":
            
            lev = request.GET.get('level')
            pos = request.GET.get('position')
            typ = request.GET.get('type')
            mus = request.GET.get('muscle')
        
            
            if is_valid_query_param(lev) and not is_valid_query_param(pos) and not is_valid_query_param(typ) and not is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj)
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
                
            elif not is_valid_query_param(lev) and is_valid_query_param(pos) and not is_valid_query_param(typ) and not is_valid_query_param(mus):
                pos_obj= YogaPosition.objects.get(position_name=pos)
                asanas_search = Asana.objects.filter(asana_position=pos_obj)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and not is_valid_query_param(pos) and is_valid_query_param(typ) and not is_valid_query_param(mus):
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_type=typ_obj)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and is_valid_query_param(pos) and not is_valid_query_param(typ) and is_valid_query_param(mus):
                pos_obj= YogaPosition.objects.get(position_name=pos)
                asanas_search = Asana.objects.filter(asana_position=pos_obj,benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and not is_valid_query_param(pos) and is_valid_query_param(typ) and is_valid_query_param(mus):
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_type=typ_obj,benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            if is_valid_query_param(lev) and not is_valid_query_param(pos) and not is_valid_query_param(typ) and is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,benifit__icontains=mus)
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and not is_valid_query_param(pos) and not is_valid_query_param(typ) and is_valid_query_param(mus):
                asanas_search = Asana.objects.filter(benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and is_valid_query_param(pos) and is_valid_query_param(typ) and not is_valid_query_param(mus):
                pos_obj= YogaPosition.objects.get(position_name=pos)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_position=pos_obj,asana_type=typ_obj)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and is_valid_query_param(pos) and is_valid_query_param(typ) and is_valid_query_param(mus):
                pos_obj= YogaPosition.objects.get(position_name=pos)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_position=pos_obj,asana_type=typ_obj,benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif is_valid_query_param(lev) and not is_valid_query_param(pos) and is_valid_query_param(typ) and not is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_type=typ_obj)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif is_valid_query_param(lev) and not is_valid_query_param(pos) and is_valid_query_param(typ) and is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_type=typ_obj,benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif is_valid_query_param(lev) and is_valid_query_param(pos) and not is_valid_query_param(typ) and not is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                pos_obj= YogaPosition.objects.get(position_name=pos)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_position=pos_obj)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif is_valid_query_param(lev) and is_valid_query_param(pos) and not is_valid_query_param(typ) and is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                pos_obj= YogaPosition.objects.get(position_name=pos)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_position=pos_obj,benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif is_valid_query_param(lev) and is_valid_query_param(pos) and is_valid_query_param(typ) and not is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                pos_obj= YogaPosition.objects.get(position_name=pos)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_position=pos_obj, asana_type=typ_obj)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            elif is_valid_query_param(lev) and is_valid_query_param(pos) and is_valid_query_param(typ) and is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                pos_obj= YogaPosition.objects.get(position_name=pos)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_position=pos_obj, asana_type=typ_obj, benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':asanas_search, 'fav_asan':fav_asan}
                return render(request,"tyogadictionary.html", context)
            
            else:
                asanas = asanas_final    
        
        paginator = Paginator(asanas, per_page=8)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        # context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas}         
        context = {'level':level,'pos':position,'type':type_ ,'aname':asanas_final,'asanas':page_obj.object_list, 'paginator':paginator, 'page_number':int(page_number), 'fav_asan':fav_asan}         
        return render(request,"tyogadictionary.html", context)     
        
    else:
        return redirect("/userlogin")
    
#search/?asanname=sha ASANA AUTOCOMPLETE

def search(request):
    qs = Asana.objects.all()
    asananame = request.GET.get('asananame')
    payload = []
    if asananame:
        asan_name_objs = Asana.objects.filter(asana_name__icontains=asananame)
        for asan_name_obj in asan_name_objs:
            payload.append(asan_name_obj.asana_name)
            
    return JsonResponse({'status':200, 'data': payload})

def yoga_detail(request,id):
    if request.session.get("useremail") is not None:
        asana = get_object_or_404(Asana, id=id)
        yoga_images = YogaImage.objects.filter(asana_id=asana.id)
        
        context = {'asana':asana, 'yoga_images':yoga_images}         
        return render(request,"tyoga_detail.html", context)
    else:
        return redirect("/userlogin")
    
 
def addyogaasana(request):
    if request.session.get("useremail") is not None:
        if request.method == "GET":
            
            lev = YogaDificulty.objects.all()
            pos = YogaPosition.objects.all()
            typ = YogaType.objects.all()
            asanas = Asana.objects.all()  
            
            context = {'position': pos, 'type':typ, 'level':lev}
            return render(request,"taddyogaasana.html", context)

        if request.method == "POST":
            yoga_name = request.POST.get("yoga_name")
            yoga_sanskrut_name = request.POST.get("yoga_sanskrut_name")
            yoga_pose_name = request.POST.get("yoga_pose_name")
            yoga_pos = request.POST.get("yoga_pos")
            yoga_typ = request.POST.get("yoga_typ")
            yoga_lev = request.POST.get("yoga_lev")
            yoga_desc = request.POST.get("yoga_desc")
            yoga_benifit = request.POST.get("yoga_benifit")
            yoga_caution = request.POST.get("yoga_caution")
            yoga_start_pos = request.POST.get("yoga_start_pos")
            yoga_conc = request.POST.get("yoga_conc")
            yoga_breath = request.POST.get("yoga_breath")
            yoga_rept = request.POST.get("yoga_rept") 
            
            files = request.FILES.getlist('inputFiles[]')         
            
            images  = files            
            
            
            data = Asana.objects.all().filter(asana_name=yoga_name).filter(created_by = request.session.get("useremail"))
            
            
            if data:
                messages.error(request,"Yoga Asana already existed in system...!!")
                return redirect('/teacher/yogadictionary/addyogaasana')
            else:
                
                lev_obj= YogaDificulty.objects.get(difficulty_name=yoga_lev)
                pos_obj= YogaPosition.objects.get(position_name=yoga_pos)
                typ_obj= YogaType.objects.get(type_name=yoga_typ)
                
                asana_obj = Asana.objects.create(
                    asana_name = yoga_name,
                    asana_sanscrut_name = yoga_sanskrut_name,
                    asana_english_name = yoga_pose_name,
                    asana_position = pos_obj,
                    asana_type = typ_obj,
                    asana_difficulty = lev_obj,
                    how_to_do = yoga_desc,
                    benifit = yoga_benifit,
                    caution = yoga_caution,
                    start_position = yoga_start_pos,
                    concentration = yoga_conc,
                    breath = yoga_breath,
                    repetitions = yoga_rept,
                    image_thumbnail = files[0],
                    created_by = request.session.get("useremail"),
                    slug = yoga_name.replace(" ",'-')
                )
                asana_obj.save()
                
                
                for f in files:
                    y1 = YogaImage.objects.create(asana=asana_obj, images = f)
                    y1.save()
                    
                    
                    
        messages.success(request,"Yoga Asana and Images added to system...!!")
        return redirect('/teacher/yogadictionary')
                    
    else:
        return redirect("/userlogin")
    
def edit_data(request, id):
    if request.session.get("useremail") is not None:        
        if request.method == "POST":
            
            asan = Asana.objects.get(id=id)
            
            yoga_name = request.POST.get("yoga_name")
            yoga_sanskrut_name = request.POST.get("yoga_sanskrut_name")
            yoga_pose_name = request.POST.get("yoga_pose_name")
            yoga_pos = request.POST.get("yoga_pos",asan.asana_position)
            yoga_typ = request.POST.get("yoga_typ",asan.asana_type)
            yoga_lev = request.POST.get("yoga_lev",asan.asana_difficulty)
            yoga_desc = request.POST.get("yoga_desc")
            yoga_benifit = request.POST.get("yoga_benifit")
            yoga_caution = request.POST.get("yoga_caution")
            yoga_start_pos = request.POST.get("yoga_start_pos")
            yoga_conc = request.POST.get("yoga_conc")
            yoga_breath = request.POST.get("yoga_breath")
            yoga_rept = request.POST.get("yoga_rept")
            
            
            if request.FILES:
                yoga_images = YogaImage.objects.filter(asana_id=asan.id) 
                no_img = len(yoga_images)
                inputFiles =[]
                for i in range(1,no_img, 1):
                    if request.FILES.get("inputFile"+str(i)):
                        print(request.FILES.get("inputFile"+str(i)))
                        inputFiles[i] = (request.FILES.get("inputFile"+str(i)))
                        
                print(inputFiles)
            
            else:
                lev_obj= YogaDificulty.objects.get(difficulty_name=yoga_lev)

                typ_obj= YogaType.objects.get(type_name=yoga_typ)

                pos_obj= YogaPosition.objects.get(position_name=yoga_pos)            
                
                if asan.created_by == request.session.get("useremail"):
                    asana_obj = Asana.objects.filter(id=id).update(
                    asana_name = yoga_name,
                    asana_sanscrut_name = yoga_sanskrut_name,
                    asana_english_name = yoga_pose_name,
                    asana_position = pos_obj,
                    asana_type = typ_obj,
                    asana_difficulty = lev_obj,
                    how_to_do = yoga_desc,
                    benifit = yoga_benifit,
                    caution = yoga_caution,
                    start_position = yoga_start_pos,
                    concentration = yoga_conc,
                    breath = yoga_breath,
                    repetitions = yoga_rept,
                    image_thumbnail = asan.image_thumbnail)

                else:
                    asana_obj = Asana(
                    asana_name = yoga_name,
                    asana_sanscrut_name = yoga_sanskrut_name,
                    asana_english_name = yoga_pose_name,
                    asana_position = pos_obj,
                    asana_type = typ_obj,
                    asana_difficulty = lev_obj,
                    how_to_do = yoga_desc,
                    benifit = yoga_benifit,
                    caution = yoga_caution,
                    start_position = yoga_start_pos,
                    concentration = yoga_conc,
                    breath = yoga_breath,
                    repetitions = yoga_rept,
                    created_by = request.session.get("useremail"),
                    image_thumbnail = asan.image_thumbnail)
                    asana_obj.save()
                messages.success(request, 'woahh!! '+yoga_name+' Updated..')
                return redirect("/teacher/yogadictionary")
            
            messages.success(request, 'woahh!! post request getting..')
            return redirect("/teacher/yogadictionary/edit/"+str(id))
        
        asana = Asana.objects.get(id=id)
        yoga_images = YogaImage.objects.filter(asana_id=asana.id) 
        lev = YogaDificulty.objects.all()
        pos = YogaPosition.objects.all()
        typ = YogaType.objects.all()
        
        context = {'asana':asana, 'yoga_images':yoga_images, 'image_count' : len(yoga_images), 'position': pos, 'type':typ, 'level':lev} 
        return render(request,"tedityogaasana.html", context)
        
    else:
        return redirect("/userlogin")
    
def tyogasequences_detail(request):
    if request.session.get("useremail") is not None:        
        if request.method == "GET":
            lev = request.GET.get('level')
            pos = request.GET.get('position')
            typ = request.GET.get('type')
            mus = request.GET.get('muscle')
        
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        lev = YogaDificulty.objects.all()
        pos = YogaPosition.objects.all()
        typ = YogaType.objects.all()  
        data = YogaClass.objects.filter(owner = user, start_time__gte=datetime.datetime.now()).order_by('start_time')
        print(data)
        context = {'level':lev,'pos':pos,'type':typ , 'yogaclass' : data}
        return render(request,"tyogasequencesques.html", context)
        
    else:
        return redirect("/userlogin")
    
    
def tyogasequences(request):
    if request.session.get("useremail") is not None:
        asanas = Asana.objects.all()
        asanas_sys = Asana.objects.filter(created_by = "system")
        asanas_usr = Asana.objects.filter(created_by = request.session.get("useremail"))
        
        asanas_final =  []
        users_asan_Set = set()
        sys_asan_Set = set()
        for asanausr in asanas_usr:
            users_asan_Set.add(asanausr.asana_name)
        for asnaaa_ in asanas_sys:
            sys_asan_Set.add(asnaaa_.asana_name)
        for asnaaa in asanas_sys:
            if asnaaa.asana_name in users_asan_Set:
                # print("is innnn ")
                for asanausrr in asanas_usr:
                    if asnaaa.asana_name == asanausrr.asana_name:
                        asanas_final.append(asanausrr)
            else:
                # print("is ")
                asanas_final.append(asnaaa)
        
        for asnaaa_u in asanas_usr:
            if asnaaa_u.asana_name not in sys_asan_Set:
                # print("No in")
                asanas_final.append(asnaaa_u)   

        print(len(asanas_final))
        
        level = YogaDificulty.objects.all()
        position = YogaPosition.objects.all()
        type_ = YogaType.objects.all()
        context = {'asanas':asanas}
        return render(request,"tyogasequences.html", context)
    else:
        return redirect("/userlogin")
    
    
def fav_asan(request,id):
    if request.session.get("useremail") is not None:
        fav_asan = get_object_or_404(Asana, id=id)
        check = favouriteAsana.objects.filter(asan = fav_asan)
        if check :
            messages.info(request, fav_asan.asana_name + "is already your favourites....")
            return redirect("/teacher/yogadictionary")
        else:
            user = WebsiteUser.objects.get(email=request.session.get("useremail"))
            fav = favouriteAsana(asan=fav_asan, user= user)
            fav.save()
        messages.success(request, "'"+ fav_asan.asana_name + "' added to favourite....")
        return redirect("/teacher/yogadictionary")
    else:
        return redirect("/userlogin")
    
def fav_asan_display(request):
    if request.session.get("useremail") is not None:
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        asan = favouriteAsana.objects.all().filter(user=user)
        context = { 'asanas': asan }
        return render(request,"tfav_asan_display.html", context)
        # return redirect("/teacher/yogadictionary")
    else:
        return redirect("/userlogin")


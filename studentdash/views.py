from cmath import inf
from datetime import datetime
import imp
import json
import re
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from yogas.models import Asana, AsanaImages, YogaImage, YogaDificulty, YogaPosition, YogaType
from users.models import WebsiteUser, MedicalInformation
from django.core.paginator import Paginator
from django.contrib import messages
from classcalendar.models import YogaClass, ClassMember

# Create your views here.

def studentdash(request):
    if request.session.get("useremail") is not None:
        return render(request,"studentdash.html")
    else:
        return redirect("/userlogin")

def studentprofile(request):
    if request.session.get("useremail") is not None:
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        context = {'user':user}
        return render(request,"studentprofile.html", context)
    
    else:
        return redirect("/userlogin")
    
def editprofile(request):
    if request.session.get("useremail") is not None:
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        postcode = user.address[-7:]       
        context = {'user':user, 'postcode':postcode}
        return render(request,"studenteditprofile.html", context)
    else:
        return redirect("/userlogin")
    
def save_profile(request):
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
            request.session["username"] = app.fullname.title()
            messages.success(request,"User Profile updated")
            return redirect('bypass')
        else:
            return render(request,"studentprofile.html")
        
        
def bypass(request):
    if request.session.get("useremail") is not None:
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        context = {'user':user}
        return render(request,"studentprofile.html",context)
    else:
        return redirect("/userlogin")
    
def studenthealth(request):
    if request.session.get("useremail") is not None:
        print(request.method)   
        if request.method == "GET":
            medsinfo = MedicalInformation.objects.filter(user_email__email=request.session.get("useremail"))
            if medsinfo:
                messages.error(request,"User Medical Information already existed")
                user = MedicalInformation.objects.get(user_email__email=request.session.get("useremail"))
                context = {'medsinfo':user}
                print(medsinfo)
                return render(request,"studenthealth.html",context)
            else:
                return render(request,"studenthealth.html")
        elif request.method == "POST":
            list_h_cond =request.POST.getlist("h_cond")
            o_h_cond_text=request.POST["o_h_cond_text"]
            old_h_cond=request.POST["old_h_cond"]
            old_h_cond_text=request.POST["old_h_cond_text"]
            yoga_exp=request.POST["yoga_exp"]
            yoga_exp_level=request.POST["yoga_exp_level"]
            
            print(list_h_cond, o_h_cond_text,old_h_cond,old_h_cond_text, yoga_exp, yoga_exp_level)
            
            abdominal = False
            back_pain = False
            neck = False
            hip = False
            heart = False
            low_blood_pressure = False
            arthritis = False
            spine = False
            knee = False
            shoulder = False
            asthma = False
            epilepsy_brain = False
            anxiety_depression = False
            respiratory_issues = False
            eye = False
            kidney = False
            high_blood_pressure = False            
            other_problems = False
            other_information = o_h_cond_text
            
            if old_h_cond == "yes":
                old_h_cond = True
            else:
                old_h_cond = False
                
            any_old_injury = old_h_cond
            
            if old_h_cond_text is not None:
                any_old_injury_info = old_h_cond_text
            else:
                any_old_injury_info = "N/A"
                
            if yoga_exp == "yes":
                yoga_exp = True
            else:
                yoga_exp = False
                
            yoga_exp_level = yoga_exp_level
            
            if "Abdominal problems"in list_h_cond:
                abdominal = True
            
            if "back pain / problems"in list_h_cond:
                back_pain = True
                
            if "Neck problems"in list_h_cond:
                neck = True
                
            if "Hip problems"in list_h_cond:
                hip = True
                
            if "Heart problems"in list_h_cond:
                heart = True
                
            if "Low blood pressure"in list_h_cond:
                low_blood_pressure = True
                
            if "Arthritis"in list_h_cond:
                arthritis = True

            if "Spine problems"in list_h_cond:
                spine = True
                
            if "Knee problems"in list_h_cond:
                knee = True
                
            if "Shoulder problems"in list_h_cond:
                shoulder = True
                
            if "Asthma"in list_h_cond:
                asthma = True
                
            if "Brain function"in list_h_cond:
                epilepsy_brain = True
                
            if "Anxiety / depression"in list_h_cond:
                anxiety_depression = True
                
            if "Respiratory issues"in list_h_cond:
                respiratory_issues = True
                
            if "Eye problems"in list_h_cond:
                eye = True
                
            if "Kidney problems"in list_h_cond:
                kidney = True
                
            if "High blood pressure"in list_h_cond:
                high_blood_pressure = True
            
            if "Other - please specify"in list_h_cond:
                other_problems = True
                
            user = WebsiteUser.objects.get(email=request.session.get("useremail"))
                
            app = MedicalInformation.objects.create(
                user_email= user,
                abdominal = abdominal,
                back_pain = back_pain,
                neck = neck,
                hip = hip,
                heart = heart,
                low_blood_pressure = low_blood_pressure,
                arthritis = arthritis,
                spine = spine,
                knee = knee,
                shoulder = shoulder,
                asthma = asthma,
                epilepsy_brain = epilepsy_brain,
                anxiety_depression = anxiety_depression,
                respiratory_issues = respiratory_issues,
                eye = eye,
                kidney = kidney,
                high_blood_pressure = high_blood_pressure,
                other_problems = other_problems,
                other_information = other_information,
                any_old_injury = any_old_injury,
                any_old_injury_info = any_old_injury_info,
                is_yoga_exp = yoga_exp,
                yoga_exp_level = yoga_exp_level,
            )
            
            app.save()
            messages.success(request,"User Medical Information updated")
            user = WebsiteUser.objects.get(email=request.session.get("useremail"))
            context = {'user':user}
            return render(request,"studentprofile.html",context)
        else:
            messages.error(request,"Some internal error ...")
            user = WebsiteUser.objects.get(email=request.session.get("useremail"))
            context = {'user':user}
            return render(request,"studentprofile.html" ,context)
        

    else:
        return redirect("/studentdash")
    
    
def addpaymentinfo(request):
    if request.session.get("useremail") is not None:
        return render(request,"addpaymentinfo.html")
    
    else:
        return redirect("/userlogin")
    
def resetpwd(request):
    if request.session.get("useremail") is not None:
        return render(request,"resetpwd.html")
    
    else:
        return redirect("/userlogin")
    
def deleteacc(request):
    if request.session.get("useremail") is not None:
        return render(request,"deleteacc.html")
    
    else:
        return redirect("/userlogin")
    
def is_valid_query_param(param):
    return param != '' and param is not None

def yogadictionary(request):
    if request.session.get("useremail") is not None:
        asanas = Asana.objects.filter(created_by = "system")
        print(len(asanas))
        level = YogaDificulty.objects.all()
        position = YogaPosition.objects.all()
        type = YogaType.objects.all()
        
        if request.method == "GET":
            
            lev = request.GET.get('level')
            pos = request.GET.get('position')
            typ = request.GET.get('type')
            mus = request.GET.get('muscle')
            
            # lev = request.POST['level']
            # pos = request.POST['position']
            # typ = request.POST['type']
            # mus = request.POST['muscle']
            
            print(lev, pos, typ, mus)
            
            if is_valid_query_param(lev) and not is_valid_query_param(pos) and not is_valid_query_param(typ) and not is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj)
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
                
            elif not is_valid_query_param(lev) and is_valid_query_param(pos) and not is_valid_query_param(typ) and not is_valid_query_param(mus):
                pos_obj= YogaPosition.objects.get(position_name=pos)
                asanas_search = Asana.objects.filter(asana_position=pos_obj)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and not is_valid_query_param(pos) and is_valid_query_param(typ) and not is_valid_query_param(mus):
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_type=typ_obj)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and is_valid_query_param(pos) and not is_valid_query_param(typ) and is_valid_query_param(mus):
                pos_obj= YogaPosition.objects.get(position_name=pos)
                asanas_search = Asana.objects.filter(asana_position=pos_obj,benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and not is_valid_query_param(pos) and is_valid_query_param(typ) and is_valid_query_param(mus):
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_type=typ_obj,benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            if is_valid_query_param(lev) and not is_valid_query_param(pos) and not is_valid_query_param(typ) and is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,benifit__icontains=mus)
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and not is_valid_query_param(pos) and not is_valid_query_param(typ) and is_valid_query_param(mus):
                asanas_search = Asana.objects.filter(benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and is_valid_query_param(pos) and is_valid_query_param(typ) and not is_valid_query_param(mus):
                pos_obj= YogaPosition.objects.get(position_name=pos)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_position=pos_obj,asana_type=typ_obj)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif not is_valid_query_param(lev) and is_valid_query_param(pos) and is_valid_query_param(typ) and is_valid_query_param(mus):
                pos_obj= YogaPosition.objects.get(position_name=pos)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_position=pos_obj,asana_type=typ_obj,benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif is_valid_query_param(lev) and not is_valid_query_param(pos) and is_valid_query_param(typ) and not is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_type=typ_obj)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif is_valid_query_param(lev) and not is_valid_query_param(pos) and is_valid_query_param(typ) and is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_type=typ_obj,benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif is_valid_query_param(lev) and is_valid_query_param(pos) and not is_valid_query_param(typ) and not is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                pos_obj= YogaPosition.objects.get(position_name=pos)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_position=pos_obj)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif is_valid_query_param(lev) and is_valid_query_param(pos) and not is_valid_query_param(typ) and is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                pos_obj= YogaPosition.objects.get(position_name=pos)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_position=pos_obj,benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif is_valid_query_param(lev) and is_valid_query_param(pos) and is_valid_query_param(typ) and not is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                pos_obj= YogaPosition.objects.get(position_name=pos)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_position=pos_obj, asana_type=typ_obj)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            elif is_valid_query_param(lev) and is_valid_query_param(pos) and is_valid_query_param(typ) and is_valid_query_param(mus):
                lev_obj= YogaDificulty.objects.get(difficulty_name=lev)
                pos_obj= YogaPosition.objects.get(position_name=pos)
                typ_obj= YogaType.objects.get(type_name=typ)
                asanas_search = Asana.objects.filter(asana_difficulty=lev_obj,asana_position=pos_obj, asana_type=typ_obj, benifit__icontains=mus)                
                context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas_search}
                return render(request,"yogadictionary.html", context)
            
            else:
                asanas = Asana.objects.filter(created_by="system")    
        
        paginator = Paginator(asanas, per_page=8)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        # context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':asanas}         
        context = {'level':level,'pos':position,'type':type ,'aname':asanas,'asanas':page_obj.object_list, 'paginator':paginator, 'page_number':int(page_number)}         
        return render(request,"yogadictionary.html", context)     
        
    else:
        return redirect("/userlogin")


def filter(request):
    if request.session.get("useremail") is not None:        
        return render(request,"yogadictionary.html")
    else:
        return redirect("/userlogin")

def studentclasses(request):
    if request.session.get("useremail") is not None:
        
        class_event = []
        class_objs = YogaClass.objects.filter(start_time__gte=datetime.now()).order_by('start_time')
        for cls in class_objs:
            class_event.append(
                {
                "title": cls.title,
                "start": cls.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": cls.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "id": cls.id,
                }
            )
            print(class_event)  
            context = { 'class_event' : class_event }
        
        return render(request,"studentclasses.html", context)
    else:
        return redirect("/userlogin")

def studentbookclass(request):
    if request.session.get("useremail") is not None:
        class_objs = YogaClass.objects.all().filter(start_time__gte=datetime.now()).order_by('start_time')
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        booked = ClassMember.objects.filter(student = user)
        context = { 'class_objs' : class_objs , 'booked':booked,}
        return render(request,"studentbookclass.html", context)
    else:
        return redirect("/userlogin")
    
def class_detail(request, id):
    if request.session.get("useremail") is not None:
        class_obj = YogaClass.objects.get(id = id)
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        booked = ClassMember.objects.filter(yoga_class = class_obj,student = user)
        context = { 'class_obj' : class_obj, 'booked':booked, }
        return render(request,"studentclassdetail.html", context)
    else:
        return redirect("/userlogin")
    
def classbooked(request, id):
    if request.session.get("useremail") is not None:
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        class_obj = YogaClass.objects.get(id = id)
        class_memebr = ClassMember.objects.filter(yoga_class=class_obj, student = user)
        meds_obj = MedicalInformation.objects.filter(user_email = user)
        if meds_obj:
            messages.success(request, "Kindly please fill in medical information before booking")
            return redirect('/studenthealth')        
        if class_memebr:
            ClassMember.objects.filter(yoga_class = class_obj, student = user).delete()
            messages.success(request, user.fullname + "had canceled booking for" + class_obj.title )
            return redirect('/studentbookclass/class_detail/'+str(class_obj.id))
        else:
            ClassMember.objects.get_or_create(yoga_class = class_obj, student = user)
            messages.success(request, user.fullname + "had booked for" + class_obj.title + "sucessfully" )
            context = { 'class_obj' : class_obj, 'booked':"booked" }
            return render(request,"studentclassdetail.html", context)
    else:
        return redirect("/userlogin")  
    
def classbookeddeleted(request,id):
    if request.session.get("useremail") is not None:
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        class_obj = YogaClass.objects.get(id = id)
        class_memebr = ClassMember.objects.get(yoga_class=class_obj, student = user)
        name = class_obj.title.title()
        class_memebr.delete()
        messages.success(request, "Booking of "+ name + " deleted successfully ")
        return redirect("/studentbookclass")
    else:  
        return redirect("/userlogin")
    
def yogaasan_detail(request,id):
    if request.session.get("useremail") is not None:
        asana = Asana.objects.get(id=id)
        yoga_images = YogaImage.objects.filter(asana_id=asana.id)
        
        context = {'asana':asana, 'yoga_images':yoga_images}         
        return render(request,"yogaasan_detail.html", context)
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



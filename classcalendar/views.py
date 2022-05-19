from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from users.models import MedicalInformation, WebsiteUser
from .models import ClassMember, YogaClass
from django.urls import reverse_lazy, reverse
from django.utils import timezone
import datetime
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

datetime.datetime.now(tz=timezone.utc) 


def calendar_view(request):
    if request.session.get("useremail") is not None:
        if request.method == "POST" and request.FILES['class_thumb'] :
            title = request.POST.get("title")
            description = request.POST.get("description")
            start_time = request.POST.get("start_time")
            end_time = request.POST.get("end_time")
            attendee = request.POST.get("attendee")
            file = request.FILES["class_thumb"]
            
            print(title)
            print(description)
            print(start_time)
            print(end_time)
            print(file)
            
            user = WebsiteUser.objects.get(email=request.session.get("useremail"))
            
            data = YogaClass.objects.filter(owner = user, start_time=start_time)
        
            if data :
                class_event = []
                user = WebsiteUser.objects.get(email=request.session.get("useremail"))
                class_objs = YogaClass.objects.all().filter(owner = user)
                for cls in class_objs:
                    class_event.append(
                        {
                        "title": cls.title,
                        "start": cls.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "end": cls.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "id": cls.id,
                        }
                    )
                
                context = { 'class_event' : class_event }
                messages.warning(request, "Yoga Class already existed on this time select different date and time")
                return render(request,"tclasscalendar.html", context )
                
            else:
                YogaClass.objects.get_or_create(
                owner=user,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
                attendee = attendee,
                image_thumbnail = file,
                )
                
                class_event = []
                user = WebsiteUser.objects.get(email=request.session.get("useremail"))
                class_objs = YogaClass.objects.all().filter(owner = user)
                for cls in class_objs:
                    class_event.append(
                        {
                        "title": cls.title,
                        "start": cls.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "end": cls.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "id": cls.id,
                        }
                    )
                
                context = { 'class_event' : class_event }
                messages.success(request, "New Yoga Class Created ...")
                return render(request,"tclasscalendar.html", context )
                # data = {'success':True, }
                # return JsonResponse(data)
        else:
            class_event = []
            user = WebsiteUser.objects.get(email=request.session.get("useremail"))
            class_objs = YogaClass.objects.all().filter(owner = user)
            for cls in class_objs:
                class_event.append(
                    {
                    "title": cls.title,
                    "start": cls.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": cls.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "id": cls.id,
                    }
                )
                
            context = { 'class_event' : class_event }
            
            return render(request,"tclasscalendar.html", context )
    return render(request,"tclasscalendar.html")
    
    

def classlist(request):
    if request.session.get("useremail") is not None:
        
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        
        data = YogaClass.objects.filter(owner = user, start_time__gte=datetime.datetime.now()).order_by('start_time')
        print(data)
        
        context = { 'data' : data }
        
        return render(request, "yogaclass_list.html" , context)
    else:
        return redirect("/userlogin")
    
    
def allclasslist (request):
    if request.session.get("useremail") is not None:
        
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        
        data = YogaClass.objects.filter(owner = user)
        
        context = { 'data' : data }
        
        return render(request, "tallclasslist.html" , context)
    else:
        return redirect("/userlogin")
    
def classeview(request,id):
    if request.session.get("useremail") is not None:
            
        data = YogaClass.objects.get(id = id)
        
        print(data.title)
        
        context = { 'class' : data ,}
        
        return render(request, "tclassview.html", context)
    else:
        return redirect("/userlogin")
    
def class_edit(request,id):
    if request.session.get("useremail") is not None:
            
        data = YogaClass.objects.get(id = id)         
    
        if request.method == "POST" :
                title = request.POST.get("title")
                description = request.POST.get("description")
                start_time = request.POST.get("start_time")
                end_time = request.POST.get("end_time")
                attendee = request.POST.get("attendee")
                file = request.FILES.get("class_thumb")
                
                print(title)
                print(description)
                print(start_time)
                print(end_time)
                print(file)
                
                user = WebsiteUser.objects.get(email=request.session.get("useremail"))
                
                data_obj = YogaClass.objects.get(id=id,owner = user)
                
                
                if file is not None:
                    data_obj.title =title
                    data_obj.description = description
                    data_obj.start_time = start_time
                    data_obj.end_time = end_time
                    data_obj.attendee = attendee
                    data_obj.image_thumbnail = file
                    data_obj.save()
                    
                else:
                    data_obj.title =title
                    data_obj.description = description
                    data_obj.start_time = start_time
                    data_obj.end_time = end_time
                    data_obj.attendee = attendee
                    data_obj.save()
                
                
                print(data)
                
                user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        
                data = YogaClass.objects.filter(owner = user)
                
                context = { 'data' : data }
                    
                messages.success(request, "Yoga Class updated ...")
                
                return redirect("/teachcer/calendar/classlist")
                
                
        context = { 'class' : data ,}
        
        return render(request, "tclassedit.html", context)
    else:
        return redirect("/userlogin")
    
def classdelete(request,id):
    if request.session.get("useremail") is not None:
    
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        data = YogaClass.objects.get(id = id, owner = user)
        
        if data:
            data.delete()
            messages.info(request, "Yoga Class deleted ...")
            return redirect("/teachcer/calendar/classlist")
        else:
            return render(request,"yogadictionary.html")
    else:
        return redirect("/userlogin")
    
def classattendee(request,id):
    if request.session.get("useremail") is not None:
        user = WebsiteUser.objects.get(email=request.session.get("useremail"))
        data = YogaClass.objects.get(id = id, owner = user)

        attendee = ClassMember.objects.filter(yoga_class = data)
        
        context = { 'attendee' : attendee ,'data' : data}
        return render(request,"tclassattendee.html", context)
    else:
        return redirect("/userlogin")
    
def studentmedsinfo(request,id):
    if request.session.get("useremail") is not None:
            user = WebsiteUser.objects.get(id=id)
            medsinfo = MedicalInformation.objects.get(user_email = user)
            context = { 'medsinfo' : medsinfo ,}
            return render(request,"tstudentmedsinfo.html", context)
    else:
        return redirect("/userlogin")
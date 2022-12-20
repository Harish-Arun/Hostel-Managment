
from audioop import reverse
from unicodedata import name
from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse

from .models import Admin_Outpass_Details, Outpass_Details,Complaint_Details, Student_Details
from django.views.decorators.csrf import csrf_exempt
from .forms import Admin_Complaint_detail_form, Admin_Outpass_detail_form, Outpass_detail_form,Complaint_detail_form
from .models import Outpass_Details
from django.contrib import messages
def home(request):
    return render(request,"Home.html")
def index(request):
    return render(request,'index.html')
def outpasslist (request):
    admin_outpass_list=Outpass_Details.objects.all()
    return render(request,'Outpass-List.html',{'admin_outpass_list':admin_outpass_list})
def reportlist (request):
    report_list=Complaint_Details.objects.all()
    return render(request,'Report-List.html',{'report_list':report_list})
def reportform(request,oid):
    object = Complaint_Details.objects.filter(id=oid).first()
    return render(request, "Report-Form.html", {'object':object})
def adminoutpassform(request,oid):
    object = Admin_Outpass_Details.objects.filter(id=oid).first()
    return render(request, "Admin_Approve_Outpass.html", {'object':object})
def approvaloutpassform(request,oid):
    object = Outpass_Details.objects.filter(id=oid).first()
    return render(request, "Outpass-Form.html", {'object':object})
def outpassapproval (request,regno):
    stu=Student_Details.objects.filter(regno=regno).first()
    outpass_list=Outpass_Details.objects.filter(regno=regno) 

    context={'outpass_list':outpass_list,'stu':stu}
    return render(request,'Outpass-Approval.html',context)
def outpass (request,regno):
    stu=Student_Details.objects.filter(regno=regno).first()
    return render(request,'Outpass.html',{'stu':stu})

def report(request,regno):
    stu=Student_Details.objects.filter(regno=regno).first()
    return render(request,'Report.html',{'stu':stu})

@csrf_exempt
def outpassupload(request):
    if (request.method=='POST'):
        print(request.POST)
        form=Outpass_detail_form(request.POST,request.FILES)
        admin_form=Admin_Outpass_detail_form(request.POST,request.FILES)   
        form.save()         
        admin_form.save()        
    return render(request,'Outpass-Form.html')

def outpassdetailsget(request):
    outpass_list=Outpass_Details.objects.all()
    
    return render(request,'Outpass-List.html',{'outpass_list':outpass_list})

@csrf_exempt
def complaintupload(request):
    if (request.method=='POST'):
        form=Complaint_detail_form(request.POST,request.FILES)
        admin_form=Admin_Complaint_detail_form(request.POST,request.FILES)
        form.save() 
        admin_form.save() 
    return render(request,'Outpass-Form.html')

@csrf_exempt
def statusupload(request,aid):
    if (request.method=='POST'):
        object = Admin_Outpass_Details.objects.filter(id=aid).first()
        upobj=Outpass_Details.objects.get(id=object.id)
        if(request.POST['submitclicked']=="Decline"):
            upobj.status="Decline"
        elif(request.POST['submitclicked']=="Approve"):
            upobj.status="Approve"
        upobj.save() 
    return render(request,"Outpass-List.html")

@csrf_exempt
def login(request):
    # return HttpResponseRedirect('outpasslist')
    if (request.method=='POST'):
 
        
        stu_check=Student_Details.objects.filter(email=request.POST['email'])
        if(stu_check):
            stu=Student_Details.objects.get(email=request.POST['email'])
            if(request.POST['password']==stu.password):
                if(request.POST['email']=="admin@ssn.edu.in"):
                    admin_outpass_list=Outpass_Details.objects.all()
                    return render(request,'Outpass-List.html',{'admin_outpass_list':admin_outpass_list})
                    
                else:
                    return render(request,'Outpass.html',{'stu':stu})
            else:
                messages.error(request,'Login Failed !!')
                return redirect('home')
        else:
            messages.error(request,'Login Failed !!')
            return redirect('home')

        
    

# @csrf_exempt
# class OutpassCreateview(generics.ListCreateAPIView):
#     queryset=Outpass_Details.objects.all()
#     serializer_class=OutpassSerailizer
# @csrf_exempt
# class ComplainCreateview(generics.ListCreateAPIView):
#     queryset=Complaint_Details.objects.all()
#     serializer_class=ComplaintSerailizer
# @csrf_exempt
# class OutpassDetailsView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'Outpass.html'
#     def get(self,request):
#         outpass_list=Outpass_Details.objects.all()
#         serializer=OutpassSerailizer(outpass_list)
#         return Response(serializer.data)
    # def post(self, request):
       
    #     serializer = 
    #     if not serializer.is_valid():
    #         return Response({'serializer': serializer, 'profile': profile})
    #     serializer.save()
    #     return redirect('profile-list')
# class ComplainDetailsView(APIView):
#     def get(self,request):
#         complain_list=Complaint_Details.objects.all()
#         serializer=ComplaintSerailizer(complain_list)
#         return Response(serializer.data)

# class ComplainDetailsView(APIView):
#     def get(self,request):
#         complain_list=Complaint_Details.objects.all()
#         serializer=ComplaintSerailizer(complain_list)
#         return Response(serializer.data)


# def view_users_list(request):
#     user_data=User.objects.all()
#     user_template=loader.get_template("UserDetails.html")
#     context={"books_users_data":user_data}
#     html_data=user_template.render(context)
#     return HttpResponse(html_data)


# class UserListview(generics.ListCreateAPIView):
#     queryset=User.objects.all()
#     serializer_class=UserSerailizer
# class UserDetailview(generics.RetrieveUpdateDestroyAPIView):
#     queryset=User.objects.all()
#     serializer_class=UserSerailizer
# class Bookview(APIView):
#     def get(self,request):
#         book_list=Book.objects.all()
#         serializer=BookSerailizer(book_list,many=True)
#         return Response(serializer.data)
# class BookDetailview(APIView):
#     def get(self,request,pk):
#         book_list=Book.objects.get(pk=pk)
#         serializer=BookSerailizer(book_list)
#         return Response(serializer.data)


# @csrf_exempt
# def OutpassApi(request,id=0):
#     if request.method=='GET':
#         complain_list = Outpass_Details.objects.all()
#         complaint_serializer=OutpassSerailizer(complain_list,many=True)
#         return JsonResponse(complaint_serializer.data,safe=False)
#     elif request.method=='POST':
#         complain_list=JSONParser().parse(request)
#         complaint_serializer=OutpassSerailizer(data=complain_list)
#         if complaint_serializer.is_valid():
#             complaint_serializer.save()
#             return JsonResponse("Added Successfully",safe=False)
#         return JsonResponse("Failed to Add",safe=False)
#     elif request.method=='PUT':
#         complain_list=JSONParser().parse(request)
#         complaint=Outpass_Details.objects.get(DepartmentId=complain_list['DepartmentId'])
#         complaint_serializer=OutpassSerailizer(complaint,data=complain_list)
#         if complaint_serializer.is_valid():
#             complaint_serializer.save()
#             return JsonResponse("Updated Successfully",safe=False)
#         return JsonResponse("Failed to Update")
#     elif request.method=='DELETE':
#         complain_list=Outpass_Details.objects.get(DepartmentId=id)
#         complain_list.delete()
#         return JsonResponse("Deleted Successfully",safe=False)

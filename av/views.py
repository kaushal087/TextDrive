from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from drive.drive_helpers import DriveHelper


# Home View
def index(request):
    template = loader.get_template('av/home.html')
    context = {}
    return HttpResponse(template.render(context, request))


# Note list view
@login_required
def list(request):
    template = loader.get_template('av/list.html')
    drive_helper = DriveHelper(request=request)
    context = drive_helper.get_list()
    return HttpResponse(template.render(context, request))

#Editor View
@login_required
def editor(request, file_id=None):
    template = loader.get_template('av/editor.html')
    context = {}
    if file_id:
        context['file_id'] = file_id
        drive_helper = DriveHelper(request=request)
        file_data = drive_helper.get_file_content(file_id=file_id)
        if file_data:
            context['file_data'] = file_data
    return HttpResponse(template.render(context, request))

#Update Notes view
@login_required
def save(request, file_id=None):
    if request.method == "POST":
        data = {}
        data['file_id'] = file_id
        data['content'] = request.POST.get("content", "")
        data['file_name'] = request.POST.get("file_name", "Untitled.txt")
        drive_helper = DriveHelper(request=request)
        drive_helper.update_file(file_id=file_id, data=data)
        return redirect('/list/')
    else:
        return HttpResponse(status=404)

#Create notes view
@login_required
def create(request):
    if request.method == 'GET':
        template = loader.get_template('av/create_file.html')
        drive_helper = DriveHelper(request=request)
        context = drive_helper.get_list()
        return HttpResponse(template.render(context, request))

    if request.method == "POST":
        data = {}
        data['file_name'] = request.POST.get("file_name", "Untitled.txt")
        data['content'] = " "
        drive_helper = DriveHelper(request=request)
        drive_helper.create_file(data=data)
        return redirect('/list/')
    else:
        return HttpResponse(status=404)

# Logout View
@login_required
def logout_user(request):
    logout(request)
    return redirect('/')

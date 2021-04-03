from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse
from .models import Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required

# from .forms import MessageModelForm
# Create your views here.

def bad_view(request,*args,**kwds):
    print(dict(request.GET))
    return HttpResponse('Do not use this bad view!')


def home_view(request,*args,**kwds):
    # return HttpResponse('<h1>HelloWorld!</h1>')
    content = {
        'name':'zrz'
    }
    return render(request,'home.html',content)

def read_notebook(request,*args,**kwds):
    try:
        return render(request,'notebook.html',{})
    except :
        return JsonResponse({'Error':'Http error!'})

def search_message(request,pk,*args,**kwds):
    try:
        obj = Message.objects.get(id=pk)
        return HttpResponse(f'id is {obj.id} and title is {obj.title}')
    except Message.DoesNotExist:
        raise Http404

def details(request,pk,*args,**kwds):
    try:
        obj = Message.objects.get(id=pk)
        return render(request,'chat/detail.html',{'obj':obj})
    except Message.DoesNotExist:
        return JsonResponse({'message': f'Message {pk} does exist'})

def try_json_search(request,pk):
    try:
        obj = Message.objects.get(id=pk)
        return HttpResponse(f'This is message {obj.id} and content is {obj.content}')
    except Message.DoesNotExist:
        return JsonResponse({'Error':f'The message {pk} does not exist'})

def show_all_message(request,*args,**kwds):
    qs = Message.objects.all()
    try:
        return render(request,'chat/showall.html',{'mess_list':qs})
    except:
        return Http404

@login_required
def create_message_view(request,*args,**kwds):
    # 这里要记得加None
    context = MessageForm(request.POST or None)

    if context.is_valid():
        # cleaned_data应该是可以去掉csrf的验证
        # 然后拿到一个字典
        print(context.cleaned_data.get('title'))
        Message.objects.create(**context.cleaned_data)
    # 把这个MessageForm作为字典的value传给html进行渲染

    # 加上这个可以清空表格
    context = MessageForm()
    # return render(request,'chat/create_view.html',{'context':context})
    return render(request,'forms.html',{'context':context})

@login_required
def create_message_view_2(request,*args,**kwds):
    post_data = None
    if request.method == "POST":
        post_data = MessageForm(request.POST)
        if post_data.is_valid():
            # print(post_data.cleaned_data)
            new_message = Message(**post_data.cleaned_data)
            new_message.save()
    post_data = MessageForm()
    return render(request,'chat/create_view.html',{'context':post_data})
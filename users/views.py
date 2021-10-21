from blog.models import Blog, Hashtags
from django.shortcuts import render, redirect
from .forms import CreateUserForm, AddUserInfoForm, MakePostForm, SetPhotoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View, generic
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from slugify import slugify
from pprint import pprint



class SetPhotoView(LoginRequiredMixin, generic.UpdateView):
    login_url='login'
    redirect_field_name='redirect_to'
    form_class=SetPhotoForm
    template_name='set_photo.html'


    def get_object(self):
        p=Profile.objects.get(user=self.request.user)
        return p

class UpdateProfileView(LoginRequiredMixin,generic.UpdateView):
    login_url='login'
    redirect_field_name='redirect_to'
    form_class=AddUserInfoForm
    template_name='profile_update_form.html'
    
    def form_valid(self, form):
        pprint(form)
        return super().form_valid(form)

    def get_object(self):
        p=Profile.objects.get(user=self.request.user)
        return p
        
class EditPostView(LoginRequiredMixin,generic.UpdateView):
    login_url='login'
    redirect_field_name='redirect_to'
    form_class=MakePostForm
    template_name='post_update_form.html'
    
    def get_object(self):
        p = Blog.objects.get(slug=self.kwargs.get('slug'))
        return p
    

    
class MakePostView(LoginRequiredMixin,View):
    login_url='login'
    redirect_field_name='redirect_to'

    def get(self,request,*args,**kwargs):
        context={'form':MakePostForm()}
        return render(request, 'make_post.html', context)

    def post(self,request,*args,**kwargs):
        form = MakePostForm(request.POST, request.FILES)
        if form.is_valid():
            user=request.user
            title=form.cleaned_data.get("title")
            description=form.cleaned_data.get("description")
            image=form.cleaned_data.get("image")
            slug=slugify(title)
            category=form.cleaned_data.get("category")
            b=Blog(user=user,title=title,description=description,slug=slug,image=image,category=category)
            b.save()
           
            return redirect("my_posts")

# class MakePostView(LoginRequiredMixin, generic.CreateView):
#     login_url='login'
#     redirect_field_name='redirect_to'
#     template_name="make_post.html"
#     form_class=MakePostForm

#     def get_object(self):
#         b=Blog.objects.get(user=self.request.user)
#         return b 

#     def get_form_kwargs(self):
#         kwargs=super(MakePostView, self).get_form_kwargs()
#         if kwargs['instance'] is None:
#             kwargs['instance']=Blog()
#         kwargs['instance'].user=self.request.user
#         return kwargs


class UserPostsView(LoginRequiredMixin,generic.ListView):
    login_url='login'
    redirect_field_name='redirect_to'
    template_name="post_list.html"
    model = Blog
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset


class PasswordsChangeView(LoginRequiredMixin,PasswordChangeView):
    login_url='login'
    redirect_field_name='redirect_to'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('my_profile')




class ProfileView(LoginRequiredMixin,View):
    login_url='login'
    redirect_field_name='redirect_to'

    def get(self, request, *args, **kwargs):
        if request.user.profile.first_name and request.user.profile.last_name:
            context={'form':AddUserInfoForm()}
            return render(request,'profile.html', context)    
        context={'form':AddUserInfoForm()}
        return render(request,'addinfo.html', context)
    
    def post(self, request, *args, **kwargs):
        form = AddUserInfoForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            p =Profile.objects.get(user=user)
            firstn=form.cleaned_data.get('first_name')
            lastn=form.cleaned_data.get('last_name') 
            profile_photo=form.cleaned_data.get('profile_photo')
            background_photo = form.cleaned_data.get('background_photo')
            bio = form.cleaned_data.get('bio')
            p.first_name = firstn
            p.last_name = lastn
            p.profile_photo = profile_photo
            p.background_photo = background_photo
            p.bio = bio
            p.save()
            return redirect('my_profile')

def registerPage(request):
    form = CreateUserForm()
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,"Account was created for " + username + " successfully!")
            return redirect("login")
    context={'form':form}
    return render(request,'registration.html',context)

def loginPage(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password = request.POST.get("password")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.info(request,"Username or password is incorrect")
    return render(request,"login.html")


def logoutPage(request):
    logout(request)
    return redirect("home")
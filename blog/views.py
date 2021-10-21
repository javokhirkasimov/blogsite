from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView
from .models import Blog,Hashtags, Comment
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from slugify import slugify
import telegram


class CategoryPageView(ListView):
    template_name = 'category.html'
    model = Blog
    context_object_name = 'info'

    def get_queryset(self):
        queryset = self.model.objects.filter(category__slug=self.kwargs.get('slug'))
        return queryset


class HomePageView(ListView):
    template_name = 'layouts.html'
    queryset = Blog.objects.all()
    context_object_name = 'info'


class HashtagPageView(ListView):
    template_name = 'hashtag.html'
    model = Blog
    context_object_name = 'info'

    def get_queryset(self):
        queryset = self.model.objects.filter(hashtags__slug=self.kwargs.get('slug'))
        return queryset


class AboutPageView(TemplateView):
    template_name='about.html'


class ContactPageView(View):

    def get(self, request, *args, **kwargs):
        return render(request,'contact.html')

    def post(self, request, *args, **kwargs):
        name=request.POST['cName']
        email=request.POST['cEmail']
        website=request.POST['cWebsite']
        message=request.POST['cMessage']

        token="1944201525:AAEhGpgcYmOUFemi_1WHn-UxjI5CDgHAbGQ"
        user_id='402136343'

        bot=telegram.Bot(token=token)

        bot.send_message(chat_id=user_id,text=f"Name: {name}\n"
                                              f"Email: {email}\n"
                                              f"Website: {website}\n\n"
                                              f"Message: \n{message}"
                         )
        return redirect("contact")


class PostDetailView(View):

    def get(self,request,*args, **kwargs):
        post=get_object_or_404(Blog, slug=kwargs['slug'])
        comments=post.comments.all()
        context={'infos':post, 'comments':comments}
        return render(request,'detail.html',context)

    def post(self,request,*args,**kwargs):
        print(kwargs)
        post=get_object_or_404(Blog, slug=kwargs['slug'])
        name=request.POST['cName']
        message=request.POST["cMessage"]
        parent_obj=None
        try:
            parent_id = int(request.POST['parent_id'])
        except:
            parent_id=None
        if parent_id:
            parent_obj= Comment.objects.get(id=parent_id)
            if parent_obj:
                reply_comment = Comment(post=post,name=name,body=message,reply=parent_obj)
                reply_comment.save()
                return HttpResponseRedirect(f"/detail/{post.slug}")
        else:
            new_comment=Comment(post=post,name=name,body=message)
            new_comment.save()
            return HttpResponseRedirect(f"/detail/{post.slug}")


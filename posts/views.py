from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Post, Like, Comment
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required#middle ware to protect our view so that unauthorized users cannot access them.
def post_comment_create_list_view(request):
    qs = Post.objects.all() #Querying all the objects from the post model
    profile = Profile.objects.get(user=request.user) #Querying the user profile from the Profile model

    # initials
    p_form = PostModelForm() #calling the postmodelform and creating an instance
    c_form = CommentModelForm() #calling the commentmodelform and creating an instance
    post_added = False #this is a boolean 

    # profile = Profile.objects.get(user=request.user)

    if 'submit_p_form' in request.POST: #if the user submit the post form do the internal logic
        print(request.POST)
        p_form = PostModelForm(request.POST, request.FILES)#Passing the user data as a parameters
        if p_form.is_valid():#if the form is valid do the internal logic
            instance = p_form.save(commit=False) #create an instance variable but we are not saving the form since we do not know who the author is 
            instance.author = profile#assigning the author as the owner of this profile 
            instance.save()#Saving the form
            p_form = PostModelForm()#Calling the postmodel form so that our post form is empty again
            post_added = True#setting our boolean to true

            return redirect("posts:main-post-view")#redirecting the user to the main-post-view

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

            return redirect("posts:main-post-view")


    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
    }#passing a dictionary to the template so that we can access the data later, using their keys

    return render(request, 'posts/main.html', context)#render the main.html template

@login_required
def like_unlike_post(request):
    user = request.user#storing the user as the user who is using the browser now 
    if request.method == 'POST':
        post_id = request.POST.get('post_id')#this gets or identifies which post is being liked 
        post_obj = Post.objects.get(id=post_id)#this gets the post 
        profile = Profile.objects.get(user=user)#this gets the profile of the user who liked the post

        if profile in post_obj.liked.all():#check whether this profile exists in the liked column 
            post_obj.liked.remove(profile)
        else:#else add the profile in the liked column
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value=='Like':#if the user gave like then change the text to unlike 
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()

    return redirect('posts:main-post-view')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post#this implies that we are working with the post model
    template_name = 'posts/confirm_del.html'#the template is confirm_del.html
    success_url = reverse_lazy('posts:main-post-view')#if the logic is successful take the user to this url
    # success_url = '/posts/'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')#we are getting the primary key of the post which the user wants to delete
        obj = Post.objects.get(pk=pk)#we are getting the post by using the pk
        if not obj.author.user == self.request.user:#if the user that is requesting to delete this post is not the author of this post then show him a warning
            messages.warning(self.request, 'You need to be the author of the post in order to delete it')
        return obj#return the post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main-post-view')
    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Comment.objects.get(pk=pk)
        if not obj.user.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the comment in order to delete it')
        return obj
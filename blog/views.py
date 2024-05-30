from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Paragraph

from django.contrib.auth.decorators import login_required
from .forms import PostForm, ParagraphFormSet
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm, ProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from .forms import UserForm, ProfileForm
from .models import Profile

def news_detail(request, news_id):
    return render(request, "Hello World", {"news_id": news_id})

class HomeView(ListView):
    model = Post
    template_name = "blog/blog_home.html"
    context_object_name = "posts"
    ordering = ["-id"]
    paginate_by = 9  
    
def your_view(request):
    objects = Post.objects.all()
    paginator = Paginator(objects, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog_home.html', {'page_obj': page_obj})

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_details.html"
    context_object_name = "post"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post_id = self.object.id
    
        # Filter the posts with IDs less than the current post's ID
        context['last_three_posts'] = Post.objects.filter(id__lt=current_post_id).order_by('-id')[:3]
    
        return context

   
# class UpdatePostView(UpdateView):
#     model = Post
#     form_class = PostForm
#     template_name = "blog/update_post.html"
    #fields = ["title", "title_tag", "body"]
    
    
class DeletePostView(DeleteView):
    model = Post
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy("home")
    
    


# class PostCreateView(CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'blog/create_post.html'
#     success_url = reverse_lazy('post_list')

#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         if self.request.POST:
#             data['paragraph_formset'] = ParagraphFormSet(self.request.POST, self.request.FILES)
#         else:
#             data['paragraph_formset'] = ParagraphFormSet()
#         return data

#     def form_valid(self, form):
#         context = self.get_context_data()
#         paragraph_formset = context['paragraph_formset']
#         if paragraph_formset.is_valid():
#             self.object = form.save()
#             paragraph_formset.instance = self.object
#             paragraph_formset.save()
#             return redirect(self.get_success_url())
#         else:
#             return self.form_invalid(form)
        
# def create_post(request):
#     if request.method == 'POST':
#         post_form = PostForm(request.POST, request.FILES)
#         if post_form.is_valid():
#             created_post = post_form.save()
#             paragraph_formset = ParagraphFormSet(request.POST, request.FILES, instance=created_post)
#             if paragraph_formset.is_valid():
#                 paragraph_formset.save()
#                 return redirect('home')  # Redirect to a desired URL
#     else:
#         post_form = PostForm()
#         paragraph_formset = ParagraphFormSet()

#     return render(request, 'blog/create_post.html', {
#         'post_form': post_form,
#         'paragraph_formset': paragraph_formset
#     })

@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            created_post = post_form.save(commit=False)
            created_post.author = request.user  # Set the author to the logged-in user
            created_post.save()
            
            paragraph_formset = ParagraphFormSet(request.POST, request.FILES, instance=created_post)
            if paragraph_formset.is_valid():
                paragraph_formset.save()
                return redirect('home')
            else:
                print(paragraph_formset.errors)  # Debugging: Print formset errors
        else:
            print(post_form.errors)  # Debugging: Print form errors
    else:
        post_form = PostForm()
        paragraph_formset = ParagraphFormSet()

    return render(request, 'blog/create_post.html', {
        'post_form': post_form,
        'paragraph_formset': paragraph_formset
    })



def edit_post_and_paragraphs(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        formset = ParagraphFormSet(request.POST, request.FILES, instance=post)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("/", pk=post.pk)  # Redirect to the post detail view
    else:
        form = PostForm(instance=post)
        formset = ParagraphFormSet(instance=post)

    return render(request, 'blog/update_post.html', {
        'form': form,
        'formset': formset,
        'post': post 
    })
    
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password'])
                    user.save()

                    if not hasattr(user, 'profile'):
                        profile = Profile(user=user)
                    else:
                        profile = user.profile

                    profile.profile_image = profile_form.cleaned_data.get('profile_image')
                    profile.save()
                
                return redirect('login')
            except Exception as e:
                print(f"Error: {e}")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    
    return render(request, 'blog/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/blog_login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')
    
def test_post_view(request):
    return render(request, 'blog/post_page.html')

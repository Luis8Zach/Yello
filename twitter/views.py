from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Post, Relationship, Comment
from .forms import UserRegisterForm, PostForm, ProfileUpdateForm, UserUpdateForm, CommentForm
from django.http import JsonResponse
from django.db.models import Count

@login_required
def home(request):
    posts = Post.objects.all()
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')

    comments = Comment.objects.filter(post__in=posts).order_by('-created_at')
    post_likes = [post.Cantidad_likes() for post in posts]

    context = {
        'posts': posts,
        'form': form,
        'post_likes': post_likes,
        'comments': comments,
    }

    return render(request, 'twitter/newsfeed.html', context)


from django.db import IntegrityError

from django.contrib import messages

from django.db import IntegrityError
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib import messages
from .models import Profile  # Asegúrate de importar el modelo Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()

                # Crea un perfil asociado al usuario recién registrado
                Profile.objects.create(user=user)

                messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')

                # Autentica al usuario y realiza el inicio de sesión
                authenticated_user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                login(request, authenticated_user)

                return redirect('login')
            except IntegrityError:
                messages.error(request, 'Ya existe un usuario con ese nombre o correo electrónico. Por favor, elige otro.')
        else:
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    if 'unique' in error.lower():
                        messages.error(request, f'Ya existe un usuario con ese {field}. Por favor, elige otro.')
                    elif 'password' in error.lower():
                        messages.error(request, 'Las contraseñas no coinciden. Por favor, verifica e inténtalo de nuevo.')
                    else:
                        messages.error(request, f'Error en el formulario ({field}): {error}')
    
    form = UserRegisterForm()
    return render(request, 'twitter/register.html', {'form': form})



def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('home')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    return render(request, 'twitter/profile.html', {'user': user, 'posts': posts})


@login_required
def editar(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '¡Tus datos se han editado correctamente!')
            return redirect('home')
        else:
            messages.error(request, 'Error: Por favor, verifica los datos e inténtalo de nuevo.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'twitter/editar.html', context)


@login_required
def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    return redirect('home')


@login_required
def top_creators(request):
    creators = Profile.objects.annotate(follower_count=Count('followers')).order_by('-follower_count')
    context = {'creators': creators}
    return render(request, 'twitter/newsfeed.html', context)


@login_required
def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationship.objects.get(from_user=current_user.id, to_user=to_user_id)
    rel.delete()
    return redirect('home')


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    referer = request.META.get('HTTP_REFERER', '/')
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    post.save()
    
    return redirect(referer)


@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.dislikes += 1
    post.save()


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        comment_form = CommentForm()

    return render(request, 'your_template.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)

    else:
        form = CommentForm()

    return render(request, 'twitter/add_comment.html', {'form': form, 'post': post})

def your_view(request):
    # Obtener la lista de usuarios más recientes
    recent_users = Profile.get_recent_users()

    context = {'recent_users': recent_users}
    return render(request, 'twitter/newsfeed.html', context)






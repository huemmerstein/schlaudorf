"""Views for handling chat interactions."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.db.models import Q

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .forms import ChatForm, DirectMessageForm, ProfileForm
from .models import ChatMessage, DirectMessage, Profile


@login_required
def index(request):
    """Display the global chat room and handle new messages."""
    if request.method == 'POST':
        if not request.user.profile.is_approved:
            messages.error(request, 'Account awaiting approval.')
            return redirect('chat:index')
        form = ChatForm(request.POST)
        if form.is_valid():
            msg = ChatMessage.objects.create(user=request.user, content=form.cleaned_data['content'])
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'chat',
                {
                    'type': 'chat.message',
                    'message': {'user': msg.user.username, 'content': msg.content},
                },
            )
            return redirect('chat:index')
    else:
        form = ChatForm()

    q = request.GET.get('q')
    messages_qs = ChatMessage.objects.select_related('user','offer')
    if q:
        messages_qs = messages_qs.filter(Q(content__icontains=q) | Q(user__username__icontains=q))
    messages_qs = messages_qs.order_by('-created_at')[:50]
    return render(request, 'chat/index.html', {'form': form, 'messages': messages_qs, 'query': q})


@login_required
def direct(request):
    """Handle direct messages between users."""
    DirectMessage.prune_old()  # Remove expired messages on each request

    if request.method == 'POST':
        if not request.user.profile.is_approved:
            messages.error(request, 'Account awaiting approval.')
            return redirect('chat:direct')
        form = DirectMessageForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient']
            try:
                recipient = User.objects.get(username=recipient_username)
            except User.DoesNotExist:
                form.add_error('recipient', 'User not found.')
            else:
                dm = DirectMessage.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    content=form.cleaned_data['content'],
                )
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'user_{recipient.id}',
                    {
                        'type': 'dm.message',
                        'message': {
                            'user': request.user.username,
                            'content': dm.content_plain,
                        },
                    },
                )
                messages.success(request, 'Message sent!')
                return redirect('chat:direct')
    else:
        form = DirectMessageForm()

    q = request.GET.get('q')
    messages_qs = DirectMessage.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).select_related('sender', 'recipient').order_by('-created_at')[:50]
    if q:
        messages_qs = [m for m in messages_qs if q.lower() in m.content_plain.lower()]

    return render(request, 'chat/dm.html', {'form': form, 'messages': messages_qs, 'query': q})


def register(request):
    """Register a new user account."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """Allow the user to update their profile."""
    profile_obj = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('chat:profile')
    else:
        form = ProfileForm(instance=profile_obj)

    return render(request, 'chat/profile.html', {'form': form})


@login_required
def profile_detail(request, username):
    """Display another user's profile."""
    from django.shortcuts import get_object_or_404
    user = get_object_or_404(User, username=username)
    profile_obj = get_object_or_404(Profile, user=user)
    return render(request, 'chat/profile_detail.html', {'profile': profile_obj})

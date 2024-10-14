from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat
from .forms import ChatForm, MessageForm

@login_required
def chat_home(request):
    chats = request.user.chats.all()  # Отображение всех чатов, в которых пользователь является участником
    return render(request, 'chat/chat_home.html', {'chats': chats})

@login_required
def chat_detail(request, pk):
    chat = get_object_or_404(Chat, pk=pk)
    messages = chat.messages.all().order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.author = request.user
            message.is_anonymous = form.cleaned_data['is_anonymous']
            message.save()
            return redirect('chat-detail', pk=chat.pk)
    else:
        form = MessageForm()

    context = {
        'chat': chat,
        'messages': messages,
        'form': form
    }
    return render(request, 'chat/chat_detail.html', context)

@login_required
def chat_create(request):
    if request.method == 'POST':
        form = ChatForm(request.POST, user=request.user)  # Передаем текущего пользователя
        if form.is_valid():
            chat = form.save()
            chat.participants.add(request.user)
            chat.participants.add(*form.cleaned_data['participants'])  # Добавляем выбранных участников
            return redirect('chat-detail', pk=chat.pk)
    else:
        form = ChatForm(user=request.user)

    return render(request, 'chat/chat_form.html', {'form': form})

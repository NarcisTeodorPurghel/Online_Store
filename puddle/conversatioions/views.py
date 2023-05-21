from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm

@login_required
def new_converstion(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item = item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversatioions:detail', primary_key=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversations/new.html', {
        'form': form #passing the form
    })

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversations/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, primary_key):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=primary_key)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversatioions:detail', primary_key=primary_key)     
    else:
        form = ConversationMessageForm()

    return render(request, 'conversations/detail.html', {
        'conversation': conversation,
        'form': form,
    })
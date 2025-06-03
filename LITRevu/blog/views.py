from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms, models

@login_required
def home(request):
    ticket = models.Ticket.objects.all()
    return render(request, 'blog/home.html', context={'ticket' : ticket})

@login_required
def publier_ticket(request):
    form = forms.ticketForm()
    if request.method == 'POST':
        form = forms.ticketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.uploader = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'blog/create_ticket_blog.html', context={'form': form})

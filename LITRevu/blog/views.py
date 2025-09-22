from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from . import forms
from .models import Ticket, Review, UserFollows
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string


# Page d'acceuil du flux.
@login_required
def home(request):
    user = request.user
    # Liste les utilisateurs suivis par l'utilisateur actuel.
    followed_user = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

    # Tickets de l'utilisateur et de ceux qu'il suit.
    tickets = Ticket.objects.filter(
        Q(user__in=followed_user) | Q(user=user)
    )
     # Critiques provenant des utilisateurs suivis ou sur leurs tickets.
    reviews_from_followed = Review.objects.select_related('ticket').filter(
        Q(user__in=followed_user)
        | Q(user=user)
        | Q(ticket__user__in=followed_user)
    )

    # Critiques sur les tickets de l'utilisateur actuel.
    reviews_on_own_ticket = Review.objects.filter(ticket__user=user)

    # Combinaison de toutes les critiques pertinentes.
    reviews = (reviews_from_followed | reviews_on_own_ticket).distinct()

    # Ajout d'un attribut pour identifier le type de contenu.
    for t in tickets:
        t.content_type = 'TICKET'
    for r in reviews:
        r.content_type = 'REVIEW'

    # Crée un set d'IDs de tickets qui ont une critique.
    tickets_with_review = set(review.ticket.id for review in reviews)

    # Indique si chaque ticket a une critique.
    for ticket in tickets:
        ticket.has_review = int(ticket.id) in tickets_with_review

    # Mélange tickets et critiques et tri par date de création décroissante.
    flux = sorted(
        list(tickets) + list(reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    # Pagination.
    page = request.GET.get('page', 1)
    paginator = Paginator(flux, 10)
    page_obj = paginator.get_page(page)

    # Gestion de requêtes AJAX pour charger plus de contenu sans recharger la page.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('blog/_flux_items.html', {'flux': page_obj, 'request': request})
        return JsonResponse({'html': html, 'has_next': page_obj.has_next()})

    return render(request, 'blog/home.html', context={'flux': page_obj})


# Page affichant les posts de l'utilisateur connecté.
@login_required
def posts(request):
    user = request.user

    tickets = Ticket.objects.filter(user=user)
    reviews = Review.objects.select_related('ticket').filter(user=user)

    # Mélange et tri tickets + critiques par date décroissante.
    posts = sorted(
        list(tickets) + list(reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    # Ajoute un attribut pour identifier le type de contenu.
    for t in tickets:
        t.content_type = 'TICKET'
    for r in reviews:
        r.content_type = 'REVIEW'

    return render(request, 'blog/posts.html', context={'flux': posts})


# Publication d'un ticket.
@login_required
def publier_ticket(request):
    form = forms.ticketForm()
    if request.method == 'POST':
        form = forms.ticketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'blog/create_ticket_blog.html', context={'form': form})


# Publication d'une critique ou d'un ticket + critique.
@login_required
def publier_critique(request, ticket_id=None):
    if ticket_id:
        ticket = get_object_or_404(Ticket, id=ticket_id)

        if request.method == 'POST':
            review_form = forms.ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.ticket = ticket
                review.user = request.user
                review.save()
                return redirect('home')
        else:
            review_form = forms.ReviewForm()

        return render(request, 'blog/response_review_blog.html', {
            'review_form': review_form,
            'ticket': ticket
        })

    # Cas où on crée un ticket ET une critique.
    if request.method == 'POST':
        ticket_form = forms.ticketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('home')
    else:
        ticket_form = forms.ticketForm()
        review_form = forms.ReviewForm()

    return render(request, 'blog/create_review_blog.html', {
        'ticket_form': ticket_form,
        'review_form': review_form
    })


# Edition d'un ticket existant.
@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    form = forms.ticketForm(request.POST or None, request.FILES or None, instance=ticket)
    if form.is_valid():
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect('posts')
    return render(request, 'blog/edit_ticket.html', context={'form': form})


# Suppression d'un ticket.
@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, 'blog/delete_ticket.html', context={'ticket': ticket})


# Edition d'une critique.
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    form = forms.ReviewForm(request.POST or None, request.FILES or None, instance=review)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.save()
        return redirect('posts')
    return render(request, 'blog/edit_review.html', context={'form': form})


# Suppression d'une critique.
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    return render(request, 'blog/delete_review.html', context={'review': review})


# Récupération du modèle utilisateur.
User = get_user_model()


# Page d'abonnement / recherche d'utilisateurs.
@login_required
def subscribe(request):
    search_form = forms.search_user(request.GET)
    results = None
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        abonnements_ids = UserFollows.objects.filter(user=request.user).values_list('followed_user_id', flat=True)
        # Exclut l'utilisateur actuel et les utilisateurs déjà suivis.
        results = User.objects.filter(username__icontains=query).exclude(id=request.user.id).exclude(id__in=abonnements_ids)

    abonnements = UserFollows.objects.filter(user=request.user)
    abonnes = UserFollows.objects.filter(followed_user=request.user)

    context = {
        'search_form': search_form,
        'results': results,
        'abonnements': abonnements,
        'abonnes': abonnes,
    }
    return render(request, 'blog/subscribe.html', context)


# Suivre un utilisateur.
@login_required
def follow_user(request, user_id):
    followed = get_object_or_404(User, id=user_id)
    if not UserFollows.objects.filter(user=request.user, followed_user=followed).exists():
        UserFollows.objects.create(user=request.user, followed_user=followed)
    return redirect('subscribe')


# Ne plus suivre un utilisateur.
@login_required
def unfollow_user(request, user_id):
    followed = get_object_or_404(User, id=user_id)
    UserFollows.objects.filter(user=request.user, followed_user=followed).delete()
    return redirect('subscribe')

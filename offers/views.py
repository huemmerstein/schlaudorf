"""Views for help offers and map."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.template.loader import render_to_string

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .forms import OfferForm
from .models import Offer
from chat.models import ChatMessage


@login_required
def offer_map(request):
    """Display all offers on a Leaflet map."""
    offers_qs = Offer.objects.all()
    offer_data = list(offers_qs.values("title","description","category","latitude","longitude"))
    return render(request, "offers/map.html", {"offers": offers_qs, "offer_data": offer_data})


@login_required
def offer_create(request):
    """Create a new offer."""
    if not request.user.profile.is_approved:
        messages.error(request, "Account awaiting approval.")
        return redirect("offers:map")
    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()
            messages.success(request, "Offer created.")
            return redirect("offers:detail", offer.id)
    else:
        form = OfferForm()
    return render(request, "offers/form.html", {"form": form})


@login_required
def offer_detail(request, pk):
    """Show a single offer with share option."""
    offer = get_object_or_404(Offer, pk=pk)
    return render(request, "offers/detail.html", {"offer": offer})


@login_required
def share_offer(request, pk):
    """Share an offer to the village chat."""
    offer = get_object_or_404(Offer, pk=pk)
    msg = ChatMessage.objects.create(user=request.user, content="", offer=offer)
    channel_layer = get_channel_layer()
    offer_html = render_to_string("offers/_card.html", {"offer": offer})
    async_to_sync(channel_layer.group_send)(
        "chat",
        {
            "type": "chat.message",
            "message": {
                "user": request.user.username,
                "offer_html": offer_html,
            },
        },
    )
    messages.success(request, "Offer shared in chat.")
    return redirect("chat:index")

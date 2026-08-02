from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TrustedContactForm
from .models import TrustedContact

MAX_CONTACTS = 10


@login_required
def contact_list(request):
    contacts = TrustedContact.objects.filter(user=request.user)
    return render(request, "contacts/list.html", {"contacts": contacts, "max": MAX_CONTACTS})


@login_required
def contact_add(request):
    current_count = TrustedContact.objects.filter(user=request.user).count()
    if current_count >= MAX_CONTACTS:
        messages.error(request, f"You can add a maximum of {MAX_CONTACTS} trusted contacts.")
        return redirect("contacts:list")
    if request.method == "POST":
        form = TrustedContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, "Trusted contact added.")
            return redirect("contacts:list")
    else:
        form = TrustedContactForm()
    return render(request, "contacts/form.html", {"form": form, "title": "Add Trusted Contact"})


@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(TrustedContact, pk=pk, user=request.user)
    if request.method == "POST":
        form = TrustedContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Trusted contact updated.")
            return redirect("contacts:list")
    else:
        form = TrustedContactForm(instance=contact)
    return render(request, "contacts/form.html", {"form": form, "title": "Edit Trusted Contact"})


@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(TrustedContact, pk=pk, user=request.user)
    if request.method == "POST":
        contact.delete()
        messages.success(request, "Trusted contact removed.")
        return redirect("contacts:list")
    return render(request, "contacts/confirm_delete.html", {"contact": contact})

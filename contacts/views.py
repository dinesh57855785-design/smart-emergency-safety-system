from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EmergencyContact
from .forms import EmergencyContactForm


@login_required
def contact_list(request):
    contacts = EmergencyContact.objects.filter(user=request.user)
    return render(request, 'contacts/list.html', {'contacts': contacts})


@login_required
def contact_create(request):
    form = EmergencyContactForm(request.POST or None)
    form.user = request.user
    if request.method == 'POST' and form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        return redirect('contacts:contact_list')
    return render(request, 'contacts/form.html', {'form': form})


@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(EmergencyContact, pk=pk, user=request.user)
    form = EmergencyContactForm(request.POST or None, instance=contact)
    form.user = request.user
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('contacts:contact_list')
    return render(request, 'contacts/form.html', {'form': form})


@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(EmergencyContact, pk=pk, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('contacts:contact_list')
    return render(request, 'contacts/confirm_delete.html', {'contact': contact})

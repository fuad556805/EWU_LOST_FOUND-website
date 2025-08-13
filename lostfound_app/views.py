# lostfound_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import FoundItem, LostItem, FoundItemImage, LostItemImage
from django.conf import settings

# -------------------- Home Page --------------------
@login_required
def home(request):
    found_items = FoundItem.objects.all().order_by('-date_reported')
    lost_items = LostItem.objects.all().order_by('-date_reported')
    return render(request, 'lostfound_app/home.html', {
        'found_items': found_items,
        'lost_items': lost_items,
        'MEDIA_URL': settings.MEDIA_URL
    })

# -------------------- Add Items --------------------
@login_required
def add_found_item(request):
    if request.method == 'POST':
        item = FoundItem.objects.create(
            user=request.user,
            item_name=request.POST.get('item_name',''),
            category=request.POST.get('category',''),
            location=request.POST.get('location',''),
            description=request.POST.get('description',''),
            contact_info=request.POST.get('contact_info','')
        )
        for f in request.FILES.getlist('images'):
            FoundItemImage.objects.create(found_item=item, image=f)
        messages.success(request, 'Found item added.')
        return redirect('home')
    return render(request, 'lostfound_app/add_item.html', {'type': 'Found'})

@login_required
def add_lost_item(request):
    if request.method == 'POST':
        item = LostItem.objects.create(
            user=request.user,
            item_name=request.POST.get('item_name',''),
            category=request.POST.get('category',''),
            location=request.POST.get('location',''),
            description=request.POST.get('description',''),
            contact_info=request.POST.get('contact_info','')
        )
        for f in request.FILES.getlist('images'):
            LostItemImage.objects.create(lost_item=item, image=f)
        messages.success(request, 'Lost item added.')
        return redirect('home')
    return render(request, 'lostfound_app/add_item.html', {'type': 'Lost'})

# -------------------- Edit/Delete Items --------------------
@login_required
def edit_found_item(request, item_id):
    item = get_object_or_404(FoundItem, id=item_id)
    if request.user != item.user and not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit this item.")
        return redirect('home')
    if request.method == 'POST':
        item.item_name = request.POST.get('item_name','')
        item.category = request.POST.get('category','')
        item.location = request.POST.get('location','')
        item.description = request.POST.get('description','')
        item.contact_info = request.POST.get('contact_info','')
        item.save()
        messages.success(request, 'Found item updated.')
        return redirect('home')
    return render(request, 'lostfound_app/edit_item.html', {'item': item, 'type':'Found'})

@login_required
def delete_found_item(request, item_id):
    item = get_object_or_404(FoundItem, id=item_id)
    if request.user != item.user and not request.user.is_superuser:
        messages.error(request, "You don't have permission to delete this item.")
        return redirect('home')
    item.delete()
    messages.success(request, 'Found item deleted.')
    return redirect('home')

@login_required
def edit_lost_item(request, item_id):
    item = get_object_or_404(LostItem, id=item_id)
    if request.user != item.user and not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit this item.")
        return redirect('home')
    if request.method == 'POST':
        item.item_name = request.POST.get('item_name','')
        item.category = request.POST.get('category','')
        item.location = request.POST.get('location','')
        item.description = request.POST.get('description','')
        item.contact_info = request.POST.get('contact_info','')
        item.save()
        messages.success(request, 'Lost item updated.')
        return redirect('home')
    return render(request, 'lostfound_app/edit_item.html', {'item': item, 'type':'Lost'})

@login_required
def delete_lost_item(request, item_id):
    item = get_object_or_404(LostItem, id=item_id)
    if request.user != item.user and not request.user.is_superuser:
        messages.error(request, "You don't have permission to delete this item.")
        return redirect('home')
    item.delete()
    messages.success(request, 'Lost item deleted.')
    return redirect('home')

# -------------------- User Authentication --------------------
def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','')
        confirm_password = request.POST.get('confirm_password','')
        
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('signup')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')
    
    return render(request, 'lostfound_app/signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'lostfound_app/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

# -------------------- Item Detail Page --------------------
@login_required
def item_detail(request, item_type, item_id):
    if item_type == 'found':
        item = get_object_or_404(FoundItem, id=item_id)
    elif item_type == 'lost':
        item = get_object_or_404(LostItem, id=item_id)
    else:
        messages.error(request, 'Invalid item type.')
        return redirect('home')

    context = {
        'item': item,
        'item_type': item_type,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'lostfound_app/item_detail.html', context)

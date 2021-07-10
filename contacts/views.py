from django.shortcuts import redirect, render
from . models import Contact
from django.contrib import messages
from django.core.mail import send_mail
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        #Check if user has made an inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id , user_id=user_id)
            if has_contacted:
                messages.error(request , 'You have already inquired about this listing!')
                return redirect('/listings/'+listing_id)
        contact = Contact(listing=listing , listing_id=listing_id , name=name , email=email , phone=phone,message=message, user_id=user_id)
        contact.save()
        #Sending mail to realtor
        send_mail(
            'Property listing inquiry alert',
            'Greetings.\n There has been an inquiry for '+listing+' . Sign into the admin panel for more info.',
            'arnavawasthy61@gmail.com',
            [ realtor_email , 'arnavawasthy60@gmail.com'],
            fail_silently=False
        )   

        messages.success(request , 'Your request has been successfully submitted! A realtor will get back to you shortly')

        return redirect('/listings/'+listing_id)
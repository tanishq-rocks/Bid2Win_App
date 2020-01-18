from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Winners, LiveSession, Placed_bids, Available_bids
from django.db.models import Q
from django.http import Http404

#Added for Paytm API
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from . import Checksum
from biddd.models import PaytmHistory


#imports for validation
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

#Time permission
from datetime import datetime
from django.utils import timezone

def signup_page(request):
    if request.method == 'POST':
        #check if the email already exist or not in the database
        form_email = request.POST['email']
        username = form_email
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #check for error data
        exist_user = User.objects.filter(email=form_email)
        if pass2 != pass1:
            return render(request,"registration/signup.html", {'msg': "Password didn't Match"})

        if "@gmail.com" not in form_email:
            return render(request,"registration/signup.html", {'msg': "Please signup using Gmail"})

        if len(exist_user) == 0 and pass1 == pass2:
            myuser = User.objects.create_user(username, form_email, pass1)
            myuser.is_active = False
            myuser.save()

            available_bid_value = Available_bids(available_bid=0, user_id=myuser.pk)
            available_bid_value.save()
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your Bid2Win account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': myuser,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token':account_activation_token.make_token(myuser),
            })
            to_email = form_email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/confirm_mail.html', {})
        else:
            if exist_user[0].is_active == False:
                current_site = get_current_site(request)
                mail_subject = 'Activate your Bid2Win account.'
                message = render_to_string('registration/acc_active_email.html', {
                    'user': exist_user[0].email,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(exist_user[0].pk)),
                    'token':account_activation_token.make_token(exist_user[0]),
                })
                to_email = form_email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                return render(request, 'registration/confirm_mail.html', {})
            else:
                return render(request, 'registration/acc_already_exist.html', {'email': form_email})

    else:
        return render(request,"registration/signup.html",{})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('index_page')
        # messages.success("your account successful is successfully created")
        return HttpResponse('<h1 style="text-align: center;">Thank you for your email confirmation. Now you can login your account.</h1>')
    else:
        return HttpResponse('Activation link is invalid!')


class WinnersListView(LoginRequiredMixin, ListView):
    model = Winners
    template_name = "winner.html"
    context_object_name = "winners"


class LivebidListView(LoginRequiredMixin, ListView):
    model = LiveSession
    template_name = "livebid.html"
    context_object_name = "products"

@login_required
def selection_get(request, p_id):                   
    #d1 = datetime(year, month, date, h, m, s, millisecond)
    #time setting for bidding session
    Exist = LiveSession.objects.filter(id=p_id).exists()
    if Exist:
        now = datetime.now().replace(tzinfo=None)
        d2 = timezone.localtime(LiveSession.objects.filter(id=p_id).values("end_time")[0]["end_time"]).replace(tzinfo=None)
        if now >= d2:
            # print(str(now) + "is less than " + str(d2))
            return render(request, './session_end.html', {})
            # return render(request, 'livebid.html', {'msg':"Session time over, You can't place bid now"})
    selected_bids = ""
    user_id = request.user.username
    print(user_id)
    print(request.user.id)
    a_bids = list(Available_bids.objects.filter(user=User.objects.get(username=user_id)).values("available_bid"))
    # print('outer')
    if request.method == 'POST':
        # print('inner')
        POST = request.POST.copy()
        selected_bids = POST.pop('check_box')
        updt_a_bids = int(a_bids[0]["available_bid"])
        if updt_a_bids >= len(selected_bids):
            for i in selected_bids:
                p_bid = Placed_bids.objects.create(bid_value=i, product_id=p_id, user_id=request.user.id)
                # p_bid = Placed_bids(bid_value=i, product_id=p_id)
                # p_bid.save(force_insert=True)
                updt_a_bids = updt_a_bids - 1
            Available_bids.objects.filter(user=User.objects.get(username=user_id)).update(available_bid=updt_a_bids)
            return render(request, "inter_selection.html", {'data': p_id})
    a_bids = list(Available_bids.objects.filter(user=User.objects.get(username=user_id)).values("available_bid"))

    Exist = LiveSession.objects.filter(id=p_id).exists()
    if Exist:
        try:
            product = list(Placed_bids.objects.filter(product_id=p_id).values("bid_value", "product_id"))
            user_product = list(Placed_bids.objects.filter(product_id=p_id, user_id=request.user.id).values("bid_value", "product_id"))
            not_user_product = list(Placed_bids.objects.filter(product_id=p_id).exclude(user_id=request.user.id).values("bid_value", "product_id"))
            if len(product) == 0:
                product = [{'bid_value': '1000', 'product_id': p_id}]
            user_bids = []
            other_users_bids = []
            repeated_bids = []
            unique_bids = []
            for k in user_product:
                user_bids.append(k["bid_value"])
            for k in not_user_product:
                other_users_bids.append(k["bid_value"])
            repeated_bids = list(set(user_bids) & set(other_users_bids)) 
            unique_bids = list(set(user_bids) - set(other_users_bids))
            # print(repeated_bids)
            # print(unique_bids)


        except Placed_bids.DoesNotExist:
            raise Http404("Page not found")

        # return render(request,"selection.html", {'product' : product, 'a': selected_bids, 'a_bids': a_bids,})
        return render(request,"selection.html", {'p_id': int(p_id), 'a_bids': a_bids, 'unique_bids': unique_bids, 'repeated_bids': repeated_bids})
    else:
        return redirect('/livebid/')

@login_required
def redirect_view_to_selection(request, data):
    p_id = int(data)
    return redirect('/selection/'+data, p_id=p_id)


@login_required
def payment(request, amount):
    if amount in [10, 35, 80, 120, 145, 260, 450]:
        user = request.user
        settings.USER = user
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        MERCHANT_ID = settings.PAYTM_MERCHANT_ID
        # REPLACE USERNAME WITH PRIMARY KEY OF YOUR USER MODEL
        CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL + request.user.username + '/'
        # Generating unique temporary ids
        order_id = Checksum.__id_generator__()
        bill_amount = amount
        # CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL + '/'

        if bill_amount:
            data_dict = {
                'MID': MERCHANT_ID,
                'ORDER_ID': order_id,
                'TXN_AMOUNT': bill_amount,
                'CUST_ID': user.email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': settings.PAYTM_WEBSITE,
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': CALLBACK_URL,
            }
            # print(data_dict)
            param_dict = data_dict
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
            return render(request, "paytm_html/payment.html", {'paytmdict': param_dict, 'user': user})
        return HttpResponse("Bill Amount Could not find.")
    return render(request, "buybid.html", {})


# @login_required
@csrf_exempt
def response(request, user_id):
    # return HttpResponse("<h1>"+user_id+"</h1>")
    # user_id
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        if data_dict.get('CHECKSUMHASH', False):
            verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        else:
            verify = False
        if verify:
            for key in request.POST:
                if key == "BANKTXNID" or key == "RESPCODE":
                    if request.POST[key]:
                        data_dict[key] = int(request.POST[key])
                    else:
                        data_dict[key] = 0
                elif key == "TXNAMOUNT":
                    data_dict[key] = float(request.POST[key])            
            if data_dict['RESPCODE'] == 1:
                # print('Order Successful')
                for i, j in [(10,2),(35,10),(80,25),(120,40),(145,50),(260,100),(450,200)]:
                    if i == int(data_dict['TXNAMOUNT']):
                        # print(i, j, type(i), type(j))
                        # a_bids = list(Available_bids.objects.filter(id=1).values("available_bid"))
                        a_bids = list(Available_bids.objects.filter(user=User.objects.get(username=user_id)).values("available_bid"))     
                        old_user_id = User.objects.filter(username=user_id).values("id")[0]["id"]
                        old_user = PaytmHistory.objects.filter(user_id=old_user_id, STATUS='TXN_SUCCESS').exists()
                        if not old_user:
                            if i == 10:
                                updt_a_bids = int(a_bids[0]["available_bid"]) + j + 1
                            if i == 35:
                                updt_a_bids = int(a_bids[0]["available_bid"]) + j + 2
                        else:
                            updt_a_bids = int(a_bids[0]["available_bid"]) + j
                            
                        Available_bids.objects.filter(user=User.objects.get(username=user_id)).update(available_bid=updt_a_bids)
                             
            PaytmHistory.objects.create(user=User.objects.get(username=user_id), **data_dict) 
                       
    return render(request, "paytm_html/recipt.html", {"paytm": data_dict, "status": data_dict['STATUS']})
    #     else:
    #         # return HttpResponse("<h1>checksum verify failed</h1>")
    #         return render(request, "paytm_html/recipt.html", {"paytm": data_dict, "status": data_dict['STATUS']})
    # else:
    #     # return HttpResponse("<h1>Method \"GET\" not allowed</h1>")
    #     return render(request, "paytm_html/recipt.html", {"paytm": data_dict, "status": data_dict['STATUS']})
    #
    # return HttpResponse(status=200)

@login_required
def redirect_view_to_buyBid(request, status):
    user_id = request.user.username
    a_bids = list(Available_bids.objects.filter(user=User.objects.get(username=user_id)).values("available_bid"))
    return render(request, "buybid.html", {'msg': status, 'a_bids': a_bids })

# Create your views here.

def index(request):
    return render(request,"index.html", {})


def about(request):
    return render(request,"about.html", {})

def terms_n_conditions(request):
    return render(request, "terms_n_conditions.html", {'email': settings.EMAIL_HOST_USER})

def faq(request):
    return render(request, "faq.html", {})

@login_required
def buybid(request):
    user_id = request.user.username
    a_bids = list(Available_bids.objects.filter(user=User.objects.get(username=user_id)).values("available_bid"))
    return render(request, "buybid.html", {'a_bids': a_bids})

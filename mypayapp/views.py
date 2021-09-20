from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from Paytm import Checksum


def home(request):
    return render(request,'index.html')

def check(request):
    if request.method=="POST":
        orderId=request.POST['orderId']
        price=request.POST['price']
        param_dict = {
                'MID': 'Sydgkg00038305629252',
                'ORDER_ID': str(orderId),
                'TXN_AMOUNT': str(price),
                'CUST_ID': 'cust_id',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, 'EImRkUr9CGly9KXB')
        return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'index.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, "EImRkUr9CGly9KXB", checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because ' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})
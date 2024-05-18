import json
import string
import xlwt # type: ignore
import datetime

from django.shortcuts import render # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.http import HttpResponse, JsonResponse # type: ignore
from django.views import View # type: ignore

chars = tuple(string.punctuation + string.digits + "¨" + "´" + "`")

# name validation
class UsernameValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        firstname = data['first_name']
        if any((c in chars) for c in firstname):
            return JsonResponse({'username_error': True}, status=400)

        return JsonResponse({'username_valid': True})


# lastname validation
class LastnameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        lastname = data['last_name']
        if any((c in chars) for c in lastname):
            return JsonResponse({'lastname_error': True}, status=400)

        return JsonResponse({'lastname_valid': True})

# validation and registration of the user in the DB
class RegistrationView(View):
    
    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        
        first_name = request.POST.get('first_name').title()
        last_name = request.POST.get('last_name').title()
        menu = request.POST.get('menu')

        # context = {
        #     'fieldValues': request.POST
        # }

        complete_name = last_name + " " + first_name

        if len(first_name) == 0 or len(last_name) == 0 or menu == 'none':
            return JsonResponse({'username_error': 'FILL BLANK FIELDS!'}, status=400)
        elif User.objects.filter(username=complete_name).exists():
            return JsonResponse({'username_error': 'A GUEST WITH THAT NAME ALREADY EXISTS'}, status=400)
        else:
            data = {'first_name': first_name, 'last_name': last_name, 'menu':menu, 'username_success': 'CONFIRMED SUCCESSFULLY'}
            user = User.objects.create_user(username=complete_name, first_name=first_name, last_name=last_name, email=menu)
    
            user.set_unusable_password()
            user.is_active = False
            user.save()

            return JsonResponse(data, safe=False)

class PasswordView(View):
    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        passwd = "xyzboda"

        password = request.POST.get('password')
        
        # context = {
        #     'fieldValues': request.POST
        # }

        if password == passwd:

            guest_count = User.objects.all().count() -1
            nocondition_guests = User.objects.filter(email="No Condition").count()
            vegetarian_guests = User.objects.filter(email="Vegetarian").count()
            vegan_guests = User.objects.filter(email="Vegan").count()
            celiac_guests = User.objects.filter(email="Celiac").count()


            response = HttpResponse(content_type="application/ms-excel")

            response['Content-Disposition'] = 'attachment; filename=MenuInvitados' + \
                                            str(datetime.datetime.now()) + '.xls'

            wb = xlwt.Workbook(encoding='utf-8')

            ws = wb.add_sheet('Invitados')

            row_num = 8

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            ws.write(0, 0, "Total guests = " + str(guest_count), font_style)
            ws.write(1, 0, "No Condition guests = " + str(nocondition_guests), font_style)
            ws.write(2, 0, "Vegetarian guests = " + str(vegetarian_guests), font_style)
            ws.write(3, 0, "Vegan Guests = " + str(vegan_guests), font_style)
            ws.write(4, 0, "Celiac guests = " + str(celiac_guests), font_style)


            columns = ['Name', 'Menu']


            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            font_style = xlwt.XFStyle()

            #sorted_table = User.objects.order_by('username')
            rows = User.objects.all().order_by('last_name').values_list('username', 'email')

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response
        return render(request, 'main/index.html')
    
class PasswordValidation(View):
    def post(self, request):
        passwd = "xyzboda"
        data = json.loads(request.body)
        password = data['password']
        if not str(password) == passwd:
            return JsonResponse({'password_error': True}, status=400)

        return JsonResponse({'password_valid': True})
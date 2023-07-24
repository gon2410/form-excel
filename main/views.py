import json
import string
import xlwt
import datetime

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views import View

chars = tuple(string.punctuation + string.digits + "¨" + "´" + "`")

# validacion del nombre
class UsernameValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        firstname = data['first_name']
        if any((c in chars) for c in firstname):
            return JsonResponse({'username_error': True}, status=400)

        return JsonResponse({'username_valid': True})


# validacion del apellido
class LastnameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        lastname = data['last_name']
        if any((c in chars) for c in lastname):
            return JsonResponse({'lastname_error': True}, status=400)

        return JsonResponse({'lastname_valid': True})

# validacion y registro de usuario en la base de datos
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

        nombre_completo = last_name + " " + first_name

        if len(first_name) == 0 or len(last_name) == 0 or menu == 'none':
            return JsonResponse({'username_error': 'FILL BLANK FIELDS!'}, status=400)
        elif User.objects.filter(username=nombre_completo).exists():
            return JsonResponse({'username_error': 'A GUEST WITH THAT NAME ALREADY EXISTS'}, status=400)
        else:
            data = {'first_name': first_name, 'last_name': last_name, 'menu':menu, 'username_success': 'CONFIRMED SUCCESSFULLY'}
            user = User.objects.create_user(username=nombre_completo, first_name=first_name, last_name=last_name, email=menu)
    
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

            invitados_count = User.objects.all().count() -1
            invitados_sincondicion = User.objects.filter(email="Sin Condicion").count()
            invitados_vegetarianos = User.objects.filter(email="Vegetariano").count()
            invitados_veganos = User.objects.filter(email="Vegano").count()
            invitados_celiacos = User.objects.filter(email="Celiaco").count()


            response = HttpResponse(content_type="application/ms-excel")

            response['Content-Disposition'] = 'attachment; filename=MenuInvitados' + \
                                            str(datetime.datetime.now()) + '.xls'

            wb = xlwt.Workbook(encoding='utf-8')

            ws = wb.add_sheet('Invitados')

            row_num = 8

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            ws.write(0, 0, "Total de invitados = " + str(invitados_count), font_style)
            ws.write(1, 0, "Total de invitados sin condicion = " + str(invitados_sincondicion), font_style)
            ws.write(2, 0, "Total de invitados vegetarianos = " + str(invitados_vegetarianos), font_style)
            ws.write(3, 0, "Total de invitados veganos = " + str(invitados_veganos), font_style)
            ws.write(4, 0, "Total de invitados celiacos = " + str(invitados_celiacos), font_style)


            ws.write(6, 0, "Lista de Invitados", font_style)
            columns = ['Nombre', 'Menu']


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
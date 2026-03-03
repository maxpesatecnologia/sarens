from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Lead

@csrf_exempt
def receber_contato(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            Lead.objects.create(
                nome=data.get('nome', ''),
                email=data.get('email', ''),
                telefone=data.get('telefone', ''),
                categoria=data.get('categoria', 'outro'),
                subcategoria=data.get('subcategoria', 'outro'),
                mensagem=data.get('mensagem', ''),
            )

            return JsonResponse({'status': 'sucesso', 'mensagem': 'Lead salvo com sucesso!'}, status=201)

        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)

    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)
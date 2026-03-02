from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Solicitacao

@csrf_exempt
def receber_contato(request):
    if request.method == 'POST':
        try:
            # Pega os dados enviados pelo seu JavaScript (JSON)
            data = json.loads(request.body)
            
            # Cria o registro no banco de dados baseado no seu model
            Solicitacao.objects.create(
                nome=data.get('nome'),
                email=data.get('email'),
                telefone=data.get('telefone'),
                assunto=data.get('assunto'),
                mensagem=data.get('mensagem')
            )
            
            return JsonResponse({'status': 'sucesso', 'mensagem': 'Solicitação salva!'}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)
    
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def process_matrix(request):
    if request.method == 'POST':
        print('request_body: ', "'", request.body.decode('utf-8'), "'")
        if request.body:
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                matrix_data = json_data.get('matrix')
                print(matrix_data)
                matrix_out = process_matrix_function(matrix_data)
                return JsonResponse({'status': 'success', 'matrix': matrix_out})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        else:
            return JsonResponse({'error': 'Body is empty'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def process_matrix_function(matrix_data):
    return matrix_data
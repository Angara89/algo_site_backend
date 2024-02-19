from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def process_matrix(request):
    if request.method == 'POST':
        #print('request_body: ', "'", request.body.decode('utf-8'), "'")
        if request.body:
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                matrix_data = json_data.get('matrix')
                print(matrix_data)
                matrix_out = process_matrix_function(matrix_data)
                print(matrix_out)
                return JsonResponse({'status': 'success', 'matrix': matrix_out})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        else:
            return JsonResponse({'error': 'Body is empty'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# 0 - empty cell
# 1 - occupied cell
# 3 - path cell
# 5 - start cell
# 6 - end cell

def process_matrix_function(matrix):
    EMPTY_CELL = 0
    OCCUPIED_CELL = 1
    PAHT_CELL = 3
    START_CELL = 5
    END_CELL = 6
    def bfs(matrix, start: tuple, end: tuple):
        pass
        

    start_row, start_col = None, None
    end_row, end_col = None, None
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == START_CELL:
                start_row, start_col = i, j
            elif matrix[i][j] == END_CELL:
                end_row, end_col = i, j

    if start_row is None or start_col is None or end_row is None or end_col is None:
        return matrix

    path = build_path(start_row, start_col)
    for row, col in path:
        matrix[row][col] = 3
    return matrix
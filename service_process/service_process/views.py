from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import copy

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
# o - occupied cell
# p - path cell
# s - start cell
# e - end cell

def process_matrix_function(matrix):
    EMPTY_CELL = 0
    OCCUPIED_CELL = 1
    PAHT_CELL = 'P'
    START_CELL = 'S'
    END_CELL = 'E'
    def bfs(matrix_main, start: tuple, end: tuple):
        def build_path(matrix, prev_cell, end: tuple, start: tuple):
            if matrix[end[0]][end[1]] == 0:
                return -1
            path = []
            lastCell = prev_cell[end]
            while lastCell != start:
                path.append(lastCell)
                lastCell = prev_cell[lastCell]
            return path
                

        matrix_temp = copy.deepcopy(matrix_main)
        matrix_temp[start[0]][start[1]] = 1
        matrix_temp[end[0]][end[1]] = 0
        queue = [start]
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        prev_cell = {}
        
        while len(queue) > 0:
            row, col = queue.pop(0)
            if matrix_temp[row][col] == END_CELL:
                break
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < len(matrix_temp) and 0 <= new_col < len(matrix_temp[0]) and matrix_temp[new_row][new_col] == EMPTY_CELL:
                    matrix_temp[new_row][new_col] = matrix_temp[row][col] + 1
                    prev_cell[(new_row, new_col)] = (row, col)
                    queue.append((new_row, new_col))
        for row_debug in matrix_temp:
            print(row_debug)
        path_start_to_end = build_path(matrix_temp, prev_cell, end, start)
        print("path_start_to_end ", path_start_to_end)
        return matrix_temp, path_start_to_end

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

    matrix_with_path, path = bfs(matrix, (start_row, start_col), (end_row, end_col))
    
    if path == -1:
        return matrix
    else:
        for row, col in path:
            matrix[row][col] = 3
        
    return matrix
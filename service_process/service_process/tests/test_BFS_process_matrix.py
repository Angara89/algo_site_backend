from django.test import TestCase, Client
import json

class ProcessMatrixTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_process_matrix(self):
        # Создаем матрицу для тестирования
        test_matrix = [
            [0, 0, 0],
            [0, 5, 1],
            [0, 1, 6]
        ]        
        # Отправляем POST-запрос на представление
        response = self.client.post('/process_matrix/', json.dumps({'matrix': test_matrix}), content_type='application/json')
        # Проверяем, что ответ успешный (HTTP-статус 200)
        self.assertEqual(response.status_code, 200)
        
        # Проверяем формат ответа
        response_data = response.json()
        self.assertIn('status', response_data)
        self.assertEqual(response_data['status'], 'success')
        self.assertIn('matrix', response_data)
                
        # Проверяем, что матрица в ответе имеет тот же формат, что и ожидаемый результат
        result_matrix = response_data['matrix']
        self.assertEqual(len(result_matrix), len(test_matrix))
        for i in range(len(test_matrix)):
            self.assertEqual(len(result_matrix[i]), len(test_matrix[i]))
            for j in range(len(test_matrix[i])):
                self.assertEqual(result_matrix[i][j], test_matrix[i][j])

    def test_process_matrix_invalid_json(self):
        # Отправляем POST-запрос с неверным JSON
        response = self.client.post('process_matrix/', 'invalid json', content_type='application/json')

        # Проверяем, что ответ содержит ошибку (HTTP-статус 400)
        self.assertEqual(response.status_code, 400)

        # Проверяем, что ответ содержит сообщение об ошибке
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Invalid JSON data')

    def test_process_matrix_empty_body(self):
        # Отправляем POST-запрос с пустым телом запроса
        response = self.client.post('process_matrix/', '', content_type='application/json')

        # Проверяем, что ответ содержит ошибку (HTTP-статус 400)
        self.assertEqual(response.status_code, 400)

        # Проверяем, что ответ содержит сообщение об ошибке
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Body is empty')

  
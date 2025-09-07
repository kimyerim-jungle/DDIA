from flask import Flask, jsonify, request

app = Flask(__name__)

# 임시 데이터베이스 역할
todos = {
    1: {'task': 'Flask 서버 개발', 'done': False},
    2: {'task': 'RESTful API 학습', 'done': True}
}
next_id = 3

# 모든 할 일 목록 가져오기
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# 새로운 할 일 추가하기
@app.route('/todos', methods=['POST'])
def add_todo():
    global next_id
    # JSON 형식의 요청 데이터를 받음
    new_todo = request.json
    if not new_todo or 'task' not in new_todo:
        return jsonify({'error': 'Task is required'}), 400

    todos[next_id] = {'task': new_todo['task'], 'done': False}
    next_id += 1
    return jsonify({'message': 'Todo added successfully'}), 201

# 특정 할 일 가져오기
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = todos.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify(todo)

if __name__ == '__main__':
    # 디버그 모드로 서버 실행
    app.run(debug=True, port=5000)
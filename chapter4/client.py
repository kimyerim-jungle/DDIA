import requests
import json

BASE_URL = 'http://127.0.0.1:5000/todos'

def get_all_todos():
    """모든 할 일 목록을 가져오는 함수"""
    print(">>> GET 요청: 모든 할 일 목록 가져오기")
    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        print("성공적으로 가져옴:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"오류 발생: 상태 코드 {response.status_code}")

def add_new_todo(task):
    """새로운 할 일을 추가하는 함수"""
    print(f"\n>>> POST 요청: '{task}' 추가")
    data = {'task': task}
    response = requests.post(BASE_URL, json=data)

    if response.status_code == 201:
        print("성공적으로 추가됨.")
    else:
        print(f"오류 발생: 상태 코드 {response.status_code}, 메시지: {response.json().get('error', '없음')}")

def get_specific_todo(todo_id):
    """특정 할 일을 가져오는 함수"""
    print(f"\n>>> GET 요청: ID {todo_id}의 할 일 가져오기")
    response = requests.get(f"{BASE_URL}/{todo_id}")

    if response.status_code == 200:
        print(f"ID {todo_id}의 할 일:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"오류 발생: 상태 코드 {response.status_code}, 메시지: {response.json().get('error', '없음')}")

if __name__ == '__main__':
    # 모든 할 일 가져오기
    get_all_todos()

    # 새로운 할 일 추가하기
    add_new_todo("파이썬 RESTful API 예제 작성")
    add_new_todo("저녁 식사 준비하기")

    # 추가 후 모든 할 일 다시 가져오기
    get_all_todos()

    # 특정 할 일 가져오기
    get_specific_todo(1)
    get_specific_todo(99) # 없는 ID
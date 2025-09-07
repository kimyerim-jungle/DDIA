import threading
import time
import datetime
import random

class FencingTokenManager:
    """
    고유 ID를 가진 Fencing Token을 발급, 검증, 관리하는 중앙 관리자.
    """
    def __init__(self, expiry_duration_seconds=5):
        self._lock = threading.Lock()
        self._expiry_duration = datetime.timedelta(seconds=expiry_duration_seconds)
        
        # --- 변경점: 토큰 상태를 더 상세히 관리 ---
        self._current_token_id = 0  # 증가하는 고유 토큰 ID
        self._current_holder = None
        self._issue_time = None
        
        print(f"--- Fencing Token 관리자 시작 (토큰 유효 시간: {expiry_duration_seconds}초) ---")

    def acquire_token(self, node_id):
        with self._lock:
            now = datetime.datetime.now()
            
            # 토큰 소유자가 있더라도 만료되었다면 없는 것으로 간주
            if self._current_holder is not None and (now - self._issue_time) > self._expiry_duration:
                print(f"\n[관리자] 토큰 ID {self._current_token_id} 만료! (이전 소유자: {self._current_holder})")
                self._current_holder = None

            # 토큰을 아무도 소유하고 있지 않을 때만 발급
            if self._current_holder is None:
                self._current_token_id += 1
                self._current_holder = node_id
                self._issue_time = now
                print(f"\n[관리자] '{node_id}'에게 새로운 토큰 (ID: {self._current_token_id})을 발급합니다.")
                return self._current_token_id
            
            return None # 획득 실패

    def release_token(self, node_id, token_id):
        with self._lock:
            # 본인이 소유한 바로 그 토큰을 반환하는지 ID까지 확인
            if self._current_holder == node_id and self._current_token_id == token_id:
                print(f"\n[관리자] '{node_id}'로부터 토큰 ID {token_id}를 반환받았습니다.")
                self._current_holder = None
                self._issue_time = None
                #self._current_token_id = 0 # 의미 없는 값으로 초기화
                return True
            return False

    # --- 추가된 핵심 메서드 ---
    def validate_token(self, node_id, token_id):
        """
        작업 수행 직전에 토큰의 유효성을 검증합니다.
        """
        with self._lock:
            now = datetime.datetime.now()
            
            # 1. 토큰 ID가 유효한지?
            if self._current_token_id != token_id:
                return False
            # 2. 토큰 소유자가 일치하는지?
            if self._current_holder != node_id:
                return False
            # 3. 토큰이 만료되지 않았는지?
            if (now - self._issue_time) > self._expiry_duration:
                return False
            
            # 모든 조건을 통과하면 유효한 토큰임
            return True

class SharedResource:
    """
    Fencing Token으로 보호되는 공유 리소스.
    """
    def __init__(self, token_manager):
        self._token_manager = token_manager
        self._data = "Initial Data"
        print("--- 공유 리소스 생성 완료 ---")

    def perform_critical_work(self, node_id, token_id):
        print(f"-> [{node_id}]가 공유 리소스에 작업 요청 (토큰 ID: {token_id})")
        
        # --- 작업 수행 전, 반드시 토큰을 검증 ---
        if self._token_manager.validate_token(node_id, token_id):
            print(f"[{node_id}] 토큰 ID {token_id} 검증 성공. 2초간 데이터 쓰기 작업 수행...")
            self._data = f"Written by {node_id} with token {token_id} at {datetime.datetime.now()}"
            time.sleep(2) # 실제 I/O 작업 시뮬레이션
            print(f"[{node_id}] 작업 완료. 현재 데이터: \"{self._data}\"")
            return True
        else:
            print(f"[{node_id}] 작업 거부! 제시한 토큰 (ID: {token_id})은 유효하지 않거나 만료되었습니다.")
            return False

def node_worker(node_id, token_manager, shared_resource, stop_event):
    while not stop_event.is_set():
        if node_id == "노드 B":
            my_token = token_manager.acquire_token(node_id)
            if my_token:
                # 1. 처음에는 유효한 토큰으로 작업 성공
                shared_resource.perform_critical_work(node_id, my_token)
                
                # 2. 토큰을 반환하지 않고 7초간 대기 (토큰은 5초 후에 만료될 것임)
                print(f"[{node_id}] 토큰을 반환하지 않고 7초간 응답 없음 상태에 빠집니다...")
                time.sleep(7)
                
                # 3. 만료된 토큰으로 다시 작업 요청 (실패해야 함)
                print(f"[{node_id}] 7초 경과. 만료된 토큰(ID: {my_token})으로 다시 작업을 요청합니다.")
                shared_resource.perform_critical_work(node_id, my_token)
        
        else:
            my_token = token_manager.acquire_token(node_id)
            if my_token:
                shared_resource.perform_critical_work(node_id, my_token)
                token_manager.release_token(node_id, my_token)
        
        time.sleep(random.uniform(2, 4))


if __name__ == "__main__":
    manager = FencingTokenManager(expiry_duration_seconds=5)
    resource = SharedResource(manager)

    nodes = ["노드 A", "노드 B", "노드 C", "노드 D", "노드 E"]
    threads = []
    stop_event = threading.Event()

    for node_name in nodes:
        thread = threading.Thread(target=node_worker, args=(node_name, manager, resource, stop_event), daemon=True)
        thread.start()
        threads.append(thread)
        time.sleep(0.2)
        
    try:
        # '노드 B'의 시나리오가 충분히 실행될 시간을 줌
        time.sleep(60) 
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()  # 모든 스레드에게 종료 요청

        #for t in threads:
        #    t.join()  # 모든 스레드가 종료될 때까지 대기

        print("--- 모든 스레드가 종료되었습니다 ---")
        input("종료...")
        
    
        
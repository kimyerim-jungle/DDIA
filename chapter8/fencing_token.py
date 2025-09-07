import time
import threading

class FencingService:
    """
    펜싱 토큰을 발급하는 분산 잠금 서비스 역할 (시뮬레이션)
    """
    def __init__(self):
        # 펜싱 토큰은 항상 증가하는 숫자여야 함
        self.fencing_token = 1
        self.lock = threading.Lock()

    def get_fencing_token(self):
        with self.lock:
            self.fencing_token += 1
            print(f"[Fencing Service] 새로운 펜싱 토큰 발급: {self.fencing_token}")
            return self.fencing_token

class SharedResource:
    """
    펜싱 토큰을 검증하는 공유 자원 역할 (예: 데이터베이스)
    """
    def __init__(self):
        self.data = None
        self.last_fencing_token = -1

    def update_data(self, new_data, token):
        print(f"[Shared Resource] 요청 수신 - 데이터: '{new_data}', 토큰: {token}")
        
        # 핵심 로직: 받은 토큰이 마지막으로 본 토큰보다 큰지 확인
        if token > self.last_fencing_token:
            print(f" -> 성공: 토큰 {token}은 유효합니다. 데이터 업데이트.")
            self.data = new_data
            self.last_fencing_token = token
            return True
        else:
            print(f" -> 실패: 토큰 {token}은 낡은(stale) 토큰입니다. 거부됨. (현재 토큰: {self.last_fencing_token})")
            return False

def main():
    fencing_service = FencingService()
    shared_resource = SharedResource()

    # --- 1. 클라이언트 A가 리더가 됨 (토큰 101 획득) ---
    print("\n[시나리오 1] 클라이언트 A가 잠금을 획득하고 작업 시작.")
    client_a_token = fencing_service.get_fencing_token()
    
    # 작업 수행 전 네트워크 단절을 시뮬레이션
    print(" -> 클라이언트 A와 네트워크 단절 발생...")
    time.sleep(1) 

    # --- 2. 클라이언트 B가 새로운 리더가 됨 (토큰 102 획득) ---
    print("\n[시나리오 2] 클라이언트 B가 새로운 리더로 선출되어 잠금 획득.")
    client_b_token = fencing_service.get_fencing_token()
    
    # B는 성공적으로 자원에 데이터를 쓴다.
    print(" -> 클라이언트 B, 토큰 102로 공유 자원에 쓰기 시도.")
    shared_resource.update_data("리더 B가 쓴 데이터", client_b_token)
    
    # --- 3. 스플릿 브레인 시나리오: A의 낡은 요청이 도착함 ---
    print("\n[시나리오 3] 클라이언트 A의 네트워크가 복구되고, 낡은 요청을 보냄.")
    print(" -> 클라이언트 A, 낡은 토큰 101로 공유 자원에 쓰기 시도.")
    shared_resource.update_data("리더 A가 쓴 데이터 (낡은)", client_a_token)
    
    print("\n[결과]")
    print(f" 최종 데이터: '{shared_resource.data}'")
    print(f" 마지막으로 유효했던 토큰: {shared_resource.last_fencing_token}")

if __name__ == "__main__":
    main()
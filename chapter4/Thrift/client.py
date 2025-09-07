import sys
# gen-py 디렉토리를 파이썬 모듈 검색 경로에 추가합니다.
sys.path.insert(0, 'gen-py')

from Calculator.Calculator import Client
from Calculator.ttypes import Operation, Work

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import time

def run_client():
    try:
        # 서버 소켓에 연결
        transport = TSocket.TSocket('localhost', 9090)
        
        # 전송 계층 버퍼링
        transport = TTransport.TBufferedTransport(transport)
        
        # 프로토콜 (인코딩) 설정
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        
        # 자동 생성된 Client 클래스 사용
        client = Client(protocol)

        # 전송 열기
        transport.open()
        print("서버에 연결되었습니다.")
        
        # RPC 호출 예시 1: ping
        print("\n[ping 호출]")
        client.ping()
        print("서버로부터 응답 받음: 'ping() 호출됨'")

        # RPC 호출 예시 2: calculate (덧셈)
        print("\n[calculate 호출 - 덧셈]")
        work_add = Work(num1=10, num2=20, op=Operation.ADD)
        sum_result = client.calculate(work_add)
        print(f"10 + 20 = {sum_result}")

        # RPC 호출 예시 3: calculate (나눗셈)
        print("\n[calculate 호출 - 나눗셈]")
        work_div = Work(num1=100, num2=4, op=Operation.DIVIDE)
        div_result = client.calculate(work_div)
        print(f"100 / 4 = {div_result}")

        # RPC 호출 예시 4: calculate (0으로 나누기)
        '''
        print("\n[calculate 호출 - 0으로 나누기]")
        work_div_by_zero = Work(num1=100, num2=0, op=Operation.DIVIDE)
        div_by_zero_result = client.calculate(work_div_by_zero)
        print(f"100 / 0 = {div_by_zero_result} (서버에서 0을 반환)")
        '''
        start_time = time.time()
        for i in range(10000):
            work_square = Work(num1=33, num2=0, op=Operation.SQUARE)
            square_result = client.calculate(work_square)
        end_time = time.time()
        print(f"소요 시간: {end_time - start_time}초")
        # 약 263초
        input("엔터를 누르면 종료합니다...")

    except Thrift.TException as tx:
        print(f"Thrift 예외 발생: {tx}")
    finally:
        # 전송 닫기
        if 'transport' in locals() and transport.isOpen():
            transport.close()
            print("연결이 종료되었습니다.")

if __name__ == '__main__':
    run_client()
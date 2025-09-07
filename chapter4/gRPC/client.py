from time import time
import grpc

# 생성된 코드 import
import calculator_pb2
import calculator_pb2_grpc

# Protobuf Empty 메시지 임포트
from google.protobuf import empty_pb2

def run_client():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        
        # RPC 호출 예시 1: Ping
        print("[Ping 호출]")
        stub.Ping(empty_pb2.Empty())
        print("서버로부터 응답 받음")

        # RPC 호출 예시 2: Calculate (덧셈)
        print("\n[Calculate 호출 - 덧셈]")
        request = calculator_pb2.Work(num1=10, num2=20, op=calculator_pb2.Operation.ADD)
        # 반환된 Int32Value 메시지에서 .value 속성으로 실제 값 추출
        sum_result = stub.Calculate(request).value
        print(f"10 + 20 = {sum_result}")

        # RPC 호출 예시 3: Calculate (나눗셈)
        print("\n[Calculate 호출 - 나눗셈]")
        request = calculator_pb2.Work(num1=100, num2=4, op=calculator_pb2.Operation.DIVIDE)
        div_result = stub.Calculate(request).value
        print(f"100 / 4 = {div_result}")

        # RPC 호출 예시 4: Calculate (0으로 나누기)
        '''
        print("\n[Calculate 호출 - 0으로 나누기]")
        request = calculator_pb2.Work(num1=100, num2=0, op=calculator_pb2.Operation.DIVIDE)
        div_by_zero_result = stub.Calculate(request).value
        print(f"100 / 0 = {div_by_zero_result} (서버에서 0을 반환)")
        '''
        start_time = time.time()
        for i in range(1000000):
            work_multiply = calculator_pb2.Work(num1=33, num2=3, op=calculator_pb2.Operation.MULTIPLY)
            multiply_result = stub.Calculate(work_multiply).value
        end_time = time.time()
        print(f"소요 시간: {end_time - start_time}초")
        # 약 초
        input("엔터를 누르면 종료합니다...")

if __name__ == '__main__':
    run_client()
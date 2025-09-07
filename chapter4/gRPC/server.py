from concurrent import futures
import time
import grpc

# 생성된 코드 import
import calculator_pb2
import calculator_pb2_grpc

# Protobuf 래퍼 메시지를 사용하기 위해 임포트
from google.protobuf import empty_pb2
from google.protobuf.wrappers_pb2 import Int32Value

# 서비스의 메서드를 구현하는 핸들러 클래스
class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Ping(self, request, context):
        print("Ping() 호출됨")
        return empty_pb2.Empty()

    def Calculate(self, request, context):
        #print(f"Calculate() 호출됨: num1={request.num1}, num2={request.num2}, op={calculator_pb2.Operation.Name(request.op)}")
        
        result = 0
        if request.op == calculator_pb2.Operation.ADD:
            result = request.num1 + request.num2
        elif request.op == calculator_pb2.Operation.SUBTRACT:
            result = request.num1 - request.num2
        elif request.op == calculator_pb2.Operation.MULTIPLY:
            result = request.num1 * request.num2
        elif request.op == calculator_pb2.Operation.DIVIDE:
            if request.num2 == 0:
                print("0으로 나눌 수 없습니다! 0을 반환합니다.")
                result = 0
            else:
                result = request.num1 // request.num2
        
        # 반환값을 Protobuf의 Int32Value 메시지로 감싸서 반환
        return Int32Value(value=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Calculator Server 시작... (포트 50051)")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
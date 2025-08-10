import sys
# gen-py 디렉토리를 파이썬 모듈 검색 경로에 추가합니다.
# 이 코드가 Thrift/ 디렉토리 내에 있다고 가정합니다.
sys.path.insert(0, 'gen-py')

from Calculator.Calculator import Processor
from Calculator.ttypes import Operation, Work

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class CalculatorHandler:
    def __init__(self):
        self.log = {}

    def ping(self):
        print("ping() 호출됨")

    def calculate(self, w):
        #print(f"calculate() 호출됨: num1={w.num1}, num2={w.num2}, op={Operation._VALUES_TO_NAMES[w.op]}")
        
        result = 0
        if w.op == Operation.ADD:
            result = w.num1 + w.num2
        elif w.op == Operation.SUBTRACT:
            result = w.num1 - w.num2
        elif w.op == Operation.MULTIPLY:
            result = w.num1 * w.num2
        elif w.op == Operation.DIVIDE:
            if w.num2 == 0:
                print("0으로 나눌 수 없습니다! 0을 반환합니다.")
                return 0
            result = w.num1 // w.num2
        elif w.op == Operation.SQUARE:
            result = w.num1 * w.num1
        
        return result

if __name__ == '__main__':
    handler = CalculatorHandler()
    # 자동 생성된 Processor 클래스 사용
    processor = Processor(handler)
    
    # 서버 소켓 생성 (localhost:9090)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9090)
    
    # 전송 계층 버퍼링
    tfactory = TTransport.TBufferedTransportFactory()
    
    # 프로토콜 (인코딩) 계층 설정
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # 단일 스레드 서버 (간단한 예제용)
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print("Calculator Server 시작...")
    try:
        server.serve()
    except KeyboardInterrupt:
        print("\n서버 종료.")
    except Exception as e:
        print(f"서버 오류 발생: {e}")
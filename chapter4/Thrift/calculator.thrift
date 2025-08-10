namespace py Calculator

// 간단한 열거형 (enum) 정의
enum Operation {
  ADD = 1,
  SUBTRACT = 2,
  MULTIPLY = 3,
  DIVIDE = 4,
  SQUARE = 5
}

// 작업 요청에 사용될 데이터 구조체 (struct)
struct Work {
  1: i32 num1,
  2: i32 num2,
  3: Operation op
}

// 서비스 인터페이스 정의
service Calculator {
  // 간단한 "ping" 메서드
  void ping(),

  // 두 숫자를 더하는 메서드
  //i32 add(1: i32 num1, 2: i32 num2),

  // 곱셈 메서드, 문자열은 string으로 표현하며 char는 없음
  //i32 multiply(1 : i32 num1, 2: i32 num2, 3: string name),

  // 복잡한 연산을 수행하는 메서드
  i32 calculate(1: Work w)
}

typedef i32 MyInteger
const i32 INT32CONSTANT = 9853
enum Operation {
    ADD = 1,
    SUBTRACT = 2,
    MULTIPLY = 3,
    DIVIDE = 4
}
struct Work {
    1: i32 num1 = 0,
    2: i32 num2,
    3: Operation op,
    4: optional string comment,
}
struct SharedStruct {
    1: i32 key,
    2: string value,
}
exception InvalidOperation {
    1: i32 what,
    2: string why,
}


service Calculator {
    SharedStruct getStruct(1: i32 key),
     void ping(),
     i32 add(1:i32 num1, 2:i32 num2),
     i32 calculate(1:i32 logid, 2:Work work) throws (1:InvalidOperation ouch),
     oneway void zip()
}

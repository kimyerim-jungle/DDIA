from . import common

def read_data_from_txt(key: str) -> str:
    if key in common.memory:
        position = common.memory[key]

        with open(common.file, 'r', encoding='utf-8') as f:
            f.seek(position)
            line = f.readline()
            return line.strip().split(',', 1)[1]
    
    return "데이터가 존재하지 않습니다."
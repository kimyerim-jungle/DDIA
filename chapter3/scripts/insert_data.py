from . import common

def reset_data() -> None:
    with open(common.file, 'w', encoding='utf-8') as f:
        f.write('')  # Clear the file content

def write_data_to_txt(key: str, value:str) -> None:
    data = f"{key},{value}\n"
    
    with open(common.file, 'a', encoding='utf-8') as f:
        common.memory[key] = f.tell()
        
        f.write(data)
        

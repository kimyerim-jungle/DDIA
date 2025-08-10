import scripts

def data_set():
    scripts.insert_data.write_data_to_txt('apple', '{"color": "red", "price": "1000 KRW"}')
    scripts.insert_data.write_data_to_txt('banana', '{"color": "yellow", "price": "500 KRW"}')
    scripts.insert_data.write_data_to_txt('kiwi', '{"color": "green", "price": "1500 KRW"}')
    scripts.insert_data.write_data_to_txt('peach', '{"color": "pink", "price": "3000 KRW"}')
    scripts.insert_data.write_data_to_txt('grape', '{"color": "purple", "price": "2000 KRW"}')
    scripts.insert_data.write_data_to_txt('orange', '{"color": "orange", "price": "1200 KRW"}')
    scripts.insert_data.write_data_to_txt('melon', '{"color": "green", "price": "3500 KRW"}')
    scripts.insert_data.write_data_to_txt('strawberry', '{"color": "red", "price": "2500 KRW"}')
    scripts.insert_data.write_data_to_txt('watermelon', '{"color": "green", "price": "5000 KRW"}')
    
def wait_for_key_input():
    while True:
        key = input("Enter a key (or type 'exit' to quit): ")
        if key.lower() == 'exit':
            break
        
        if key.lower() == 'write':
            k = input("Enter key to write: ")
            v = input("Enter value to write: ")
            scripts.insert_data.write_data_to_txt(k, v)
        elif key.lower() == 'read':
            k = input("Enter key to read: ")
            value = scripts.read_data.read_data_from_txt(k)
            print(value)
        else:
            print("Unknown command. Please enter 'write', 'read', or 'exit'.")

if __name__ == "__main__":
    scripts.insert_data.reset_data()
    
    data_set()
    
    wait_for_key_input()
    
    
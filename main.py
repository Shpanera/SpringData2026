from core.processing import process_data, reverse_string, count_characters

def main():  
    test_data = "Hello, World!"
    
    print(f"Исходная строка: {test_data}")
    print(f"После process_data(): {process_data(test_data)}")
    print(f"После reverse_string(): {reverse_string(test_data)}")
    print(f"Количество символов: {count_characters(test_data)}")
    
if __name__ == "__main__":
    main()


import time


def counter():
    is_counter = input("Do you want to count the tickets (Y/N): ")
    while is_counter == '' or is_counter.upper() not in ['Y', 'N']:
        print('This is not a valid answer')
        is_counter = input("Do you want to count the tickets (Y/N): ")
    if is_counter.upper() == "Y":
        x = input('Enter the text x-access: ')
        while x == "" or x.isnumeric() == False:
            print('This x-access is not a valid number')
            x = input('Enter the text x-access: ')
        y = input('Enter the text y-access: ')
        while y == "" or y.isnumeric() == False:
            print('This y-access is not a valid number')
            y = input('Enter the text y-access: ')
        return {"x": x, "y": y}
    else:
        return False


c = counter()

print(c['x'])

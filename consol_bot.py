from collections import UserDict
from datetime import datetime
import pickle


class AddressBook(UserDict):
    def __init__(self, data):
        self.count = -1
        self.list_keys = []
        self.data = data
        for k in self.data.keys():
            self.list_keys.append(k)

    def __iter__(self):
        return self

    def __next__(self):
        if self.count + 1 >= len(self.list_keys):
            raise StopIteration
        self.count += 1
        return self.list_keys[self.count], self.data[self.list_keys[self.count]]

    def add_record(self, key, value):
        self.data[key] = value
        self.list_keys.append(key)


class Field:
    def __init__(self, phone=None, birthday=None):
        self.__phone = None
        self.__birthday = None
        if phone:
            self.phone = phone
        if birthday:
            self.birthday = birthday

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        if phone.startswith("+") and len(phone) == 13:
            self.__phone = phone
        else:
            print("Number must be started from '+' and must have 12 digits")

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        birthday = birthday.split(".")
        if int(birthday[0]) > (datetime.now().year - 100) and int(birthday[0]) < (datetime.now().year):
            self.__birthday = birthday
        else:
            print("Human can`t live that long or be born in the future -__-")


class Name:
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, value):
        super().__init__(phone=value)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(birthday=value)


class Record:

    def __init__(self, name, phone=None, birthday=""):
        self.name = name
        self.phone = phone
        if birthday:
            self.birthday = birthday.birthday
        else:
            self.birthday = ""

    def add_change(self):
        if self.birthday:
            return self.phone, self.days_to_birthday()
        else:
            return self.phone

    def delete(self):
        return []

    def days_to_birthday(self):
        self.birthday = datetime(int(self.birthday[0]), int(
            self.birthday[1]), int(self.birthday[2]))
        date_now = datetime.now().date()
        self.birthday = self.birthday.replace(year=date_now.year)

        if self.birthday.date() > date_now:
            return f"days to birthday: {(self.birthday.date() - date_now).days}"
        elif self.birthday.date() == date_now:
            return "Today is birthday :)"
        else:
            return f"days to birthday: {((self.birthday.replace(year=date_now.year+1)).date() - date_now).days}"


number_dict = AddressBook({
    "Name": "+380000000000"
})


with open("number_dict.bin", "rb") as f:
    number_dict = pickle.load(f)


CYCLE = True

list_command = ("show all", "good bye")
list_user_input = []


def input_error(func):
    def inner():

        if list_user_input[0] == "add" or list_user_input[0] == "change":
            try:
                if list_user_input[1].isalpha() and len(list_user_input) >= 2:
                    date_check = list_user_input[-1].split(".")
                    if len(list_user_input[-1]) == 10 and len(date_check) == 3:
                        if 0 < int(date_check[1]) <= 12 and int(date_check[2]) > 0:
                            birthday = list_user_input[-1]
                        else:
                            raise KeyError
                    else:
                        birthday = ""
                    return func(birthday)
                else:
                    raise KeyError
            except:
                return "Give me first - name, then - number phones. In the end, if you want, give me date of birthday, like 'yyyy.mm.dd'!"

        elif list_user_input[0] == "phone":
            try:
                if list_user_input[1].isalpha() and list_user_input[1] in number_dict:
                    return func()
                else:
                    raise KeyError
            except:
                return "Enter another user name. This user name isn`t in the address book"

        elif list_user_input[0] == "delete":
            try:
                if list_user_input[1].isalpha() and list_user_input[1] in number_dict and len(list_user_input) == 2:
                    return func()
                else:
                    raise KeyError
            except:
                return "Enter user name you want to delete, this user name isn`t in the address book"

        elif list_user_input[0] == "show":
            try:
                if int(list_user_input[1]) <= len(number_dict) and int(list_user_input[1]) > 0:
                    return func()
                raise KeyError
            except:
                return "You don`t have as many contacts as you printed!"

        elif list_user_input[0] == "show all":
            return func()

        else:
            return func()

    return inner


@input_error
def hello():
    return "How can I help you?"


@input_error
def add_change(birthday):
    phones = []

    if len(list_user_input) != 2:
        for phone in list_user_input[2:-1]:
            phone = Phone(phone)
            if phone.phone:
                phones.append(phone.phone)

        if not birthday:
            phone = Phone(list_user_input[-1])
            if phone.phone:
                phones.append(phone.phone)
        else:
            birthday = Birthday(birthday)

    if phone and birthday:
        record = Record(Name(list_user_input[1]), phones, birthday)
        number_dict.add_record(record.name.value, record.add_change())
    elif phone:
        record = Record(Name(list_user_input[1]), phones)
        number_dict.add_record(record.name.value, record.add_change())


@input_error
def phone():
    name = list_user_input[1]
    return number_dict.get(name)


@input_error
def show_all():
    global number_dict
    number_dict = AddressBook(number_dict.data)
    res_show_all = ("")
    for k, v in number_dict:
        res_show_all += f"{k}: {v}\n"
    res_show_all = res_show_all.strip()
    return res_show_all


@input_error  # За допомогою цієї команди виводимо стільки контактів скільки хочемо. Треба писати, як приклад "show 3", тоді виведе перші 3 контакти
def show():
    global number_dict
    number_dict = AddressBook(number_dict.data)
    res_show_all = ("")
    for _ in range(int(list_user_input[1])):
        x = next(number_dict)
        res_show_all += f"{str(x)}\n"
    res_show_all = res_show_all.strip()
    return res_show_all


@input_error
def exit():
    global CYCLE
    CYCLE = False
    return "Good bye!"


@input_error
def delete():
    global number_dict
    record = Record(Name(list_user_input[1]))
    number_dict.add_record(record.name.value, record.delete())
    number_dict = AddressBook(number_dict.data)


operations = {
    "hello": hello,
    "add": add_change,
    "change": add_change,
    "phone": phone,
    "show all": show_all,
    "show": show,
    "good bye": exit,
    "close": exit,
    "exit": exit,
    "delete": delete
}


def get_handler(operator):
    try:
        return operations[operator[0]]
    except:
        return "This function is not exists. Try again!"


def main():

    global list_user_input

    user_input = input("Please enter command: ")
    list_user_input = []

    if user_input.lower() in list_command:
        list_user_input.append(user_input)
    else:
        list_user_input = user_input.split()

    if user_input:

        registr = list_user_input[0].lower()
        list_user_input[0] = registr

        handler = get_handler(list_user_input)

        if type(handler) == str:
            print(handler)
        else:
            result_print = handler()
            if result_print:
                print(result_print)


if __name__ == "__main__":
    while CYCLE:
        main()

        with open("number_dict.bin", "wb") as f:
            pickle.dump(number_dict, f)

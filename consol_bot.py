number_dict = {
    "Andrii": "380671125330",
    "Oksana": "380675069283",
    "Oleksandr": "380677384098",
    "Valeriya": "380934267600"
}

CYCLE = True

list_command = ("show all", "good bye")
list_user_input = []


def input_error(func):
    def inner():

        if list_user_input[0] == "add" or list_user_input[0] == "change":
            try:
                if list_user_input[1].isalpha() and list_user_input[2].isnumeric():
                    return func()
                else:
                    raise KeyError
            except:
                return "Give me name and phone please"

        elif list_user_input[0] == "phone":
            try:
                if list_user_input[1].isalpha():
                    return func()
                else:
                    raise KeyError
            except:
                return "Enter user name"

        else:
            return func()

    return inner


@input_error
def hello():
    return "How can I help you?"


@input_error
def add_change():
    name = list_user_input[1]
    phone_num = list_user_input[2]
    number_dict[name] = phone_num


@input_error
def phone():
    name = list_user_input[1]
    return number_dict.get(name)


@input_error
def show_all():
    res_show_all = ("")
    for k, v in number_dict.items():
        res_show_all += f"{k}: {v}\n"
    res_show_all = res_show_all.strip()
    return res_show_all


@input_error
def exit():
    global CYCLE
    CYCLE = False
    return "Good bye!"


operations = {
    "hello": hello,
    "add": add_change,
    "change": add_change,
    "phone": phone,
    "show all": show_all,
    "good bye": exit,
    "close": exit,
    "exit": exit
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

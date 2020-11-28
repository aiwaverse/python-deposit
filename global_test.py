global_create_user = 1


def create_user():
    global global_create_user
    if global_create_user == 3:
        global_create_user = 0
        return True
    global_create_user += 1
    return False


def retry(operation, attempts):
    for n in range(attempts):
        if operation():
            print("Attempt " + str(n) + " succeeded")
            break
        else:
            print("Attempt " + str(n) + " failed")


print("Attempting to create_user with 3:")
retry(create_user, 5)


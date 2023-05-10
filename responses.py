
 #Not using yet
def handle_response(message):

    p_message = message.lower()

    if p_message == 'hello':
        return 'Hey there'

    else:
        print(f'{message}')
        return 'I dont know what that is'


    #return 'I dont know what that is'
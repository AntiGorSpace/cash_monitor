
from datetime import datetime


def write_log(name:str, text:str):
    date = datetime.now()
    str_date = date.strftime('%Y-%m-%d  %H:%M:%S')
    text = f'''

        {str_date}

        {text}
    '''
    with open(f'./logs/{name}.log', "a") as log_file:
        log_file.write(text)
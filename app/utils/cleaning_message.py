import re
import time
import random

def clean_text(user, supporter=None, message=None):
    global latest_message, last_update_time

    if user.clean_option == 'random':
        message = re.sub(r'[^\w\s]', '', message)
        bad_words = [bw.word for bw in user.bad_words]
        good_words = [gw.word for gw in user.good_words]

        for bad_word in bad_words:
            if re.search(rf'\b{bad_word}\b', message, flags=re.IGNORECASE):
                replacement = random.choice(good_words) if good_words else bad_word
                message = re.sub(rf'\b{bad_word}\b', replacement, message, flags=re.IGNORECASE)
                
    elif user.clean_option == 'fixed':
        fixed_message = user.fixed_message
        fixed_supporter = user.fixed_supporter

        if message:
            message = re.sub(r'[^\w\s]', '', message)
            bad_words = [bw.word for bw in user.bad_words]

            for bad_word in bad_words:
                if re.search(rf'\b{bad_word}\b', message, flags=re.IGNORECASE):
                    message = fixed_message

        if supporter:
            supporter = re.sub(r'[^\w\s]', '', supporter)
            bad_words = [bw.word for bw in user.bad_words]

            for bad_word in bad_words:
                if re.search(rf'\b{bad_word}\b', supporter, flags=re.IGNORECASE):
                    message = fixed_supporter

    latest_message = message
    last_update_time = time.time()  
    return message


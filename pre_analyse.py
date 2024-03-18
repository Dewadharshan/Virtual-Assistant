import time

def pre_analyse_command(sentence):
    sentence = sentence.lower()
    if "open" in sentence:
        index = sentence.find('open')
        application = sentence[index+4:]
        if len(application) < 4:
            return None
        else:
            return 'open_application("'+application+'")'
    
    elif ("click on" in sentence or "clickon" in sentence) and 'video' not in sentence:
        index = sentence.find('on')
        click_word = sentence[index+2:]
        if len(click_word) < 3:
            return None
        else:
            return 'find_text_on_screen("'+click_word+'")'
        
    elif ("select" in sentence) and 'video' not in sentence:
        index = sentence.find('select')
        click_word = sentence[index+6:]
        if len(click_word) < 3:
            return None
        else:
            return 'find_text_on_screen("'+click_word+'")'
        
    elif 'search' in sentence:
        index = sentence.find('search')
        search_text = sentence[index+6:]
        if len(search_text) < 4:
            return None
        else:
            return 'search_google("'+search_text+'")'
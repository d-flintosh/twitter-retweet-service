from typing import Union

from src.events.college_map import college_map


def decipher_school(tweet_text: str) -> Union[None, str]:
    for school, word_list in college_map.items():
        for word in word_list:
            if word.lower() in tweet_text.lower():
                return school

    return None

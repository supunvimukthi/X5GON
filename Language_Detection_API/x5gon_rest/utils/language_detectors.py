import cld2
import string

from x5gon_rest.models.fasttext_model import get_or_create_fasttext_model


def fasttext_detector(text):
    """
    fastText library functionality implementation for the language detection API
    this library is used for prominent language detection
    Args:
        text: (string) text value sent for language detection

    Returns: (dict) detected language with its confidence value or (boolean) if error returns false
    """
    try:
        text = ''.join(x for x in text if x in string.printable)
        sentence = text.split("\n")[0]
        result = get_or_create_fasttext_model().predict([sentence])
        return result[0][0][0].split("_label__")[1], result[1][0][0]
    except Exception as e:
        return str(e)


def cld2_detector(text):
    """
    cld2 library functionality implementation for the language detection API
    this library is used for multiple language detection
    Args:
        text: (string) text value sent for language detection

    Returns: (dict) detected languages with its confidence values or (boolean) if error returns false

    """
    try:
        text = ''.join(x for x in text if x in string.printable)
        result = cld2.detect(text.strip())
        if result[2][1].language_code != "un":
            return [(result[2][0].language_code, result[2][0].percent),
                    (result[2][1].language_code, result[2][1].percent)]
        else:
            return [(result[2][0].language_code, result[2][0].percent)]

    except Exception as e:
        return str(e)

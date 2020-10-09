from x5gon_rest.utils.language_detectors import fasttext_detector, cld2_detector
from x5gon_rest.fieldnames import DETECTED_LANGUAGE, CONFIDENCE, ERROR


def detect_language(text):
    """
    send the text string through fastText and cld2 language detection libraries to detect language
    FastText is used to detect the prominent language
    Cld2 is used to check whether multple languages are present
    :param text: (string) text that is sent for language detection
    :return: (JSON) detected results with confidence values or (string) error output
    """
    fastText_detection = fasttext_detector(text)
    cld2_detection = cld2_detector(text)

    """ check for error outputs from the libraries """
    if type(fastText_detection) != tuple:
        response = {ERROR: fastText_detection}
        return response
    elif type(cld2_detection) != list:
        response = {ERROR: cld2_detection}
        return response

    """ check whether multiple language were detected """
    if len(cld2_detection) > 1:
        response = {DETECTED_LANGUAGE: [cld2_detection[0][0], cld2_detection[1][0]],
                    CONFIDENCE: [str(cld2_detection[0][1]),
                                 str(cld2_detection[1][1])]}
    else:
        if cld2_detection[0][1] < fastText_detection[1]:
            response = {DETECTED_LANGUAGE: [fastText_detection[0]],
                        CONFIDENCE: [str(fastText_detection[1])]}
        else:
            response = {DETECTED_LANGUAGE: [cld2_detection[0][0]],
                        CONFIDENCE: [str(cld2_detection[0][1])]}

    return response

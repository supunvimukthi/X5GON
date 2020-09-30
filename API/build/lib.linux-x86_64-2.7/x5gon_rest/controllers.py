from x5gon_rest.utils.language_detectors import fasttext_detector, cld2_detector
from x5gon_rest.fieldnames import DETECTED_LANGUAGE, CONFIDENCE


def detect_language(text):
    fastText_detection = fasttext_detector(text)
    cld2_detection = cld2_detector(text)

    if len(cld2_detection) > 1:
        response = {DETECTED_LANGUAGE: [cld2_detection[0][0], cld2_detection[1][0]],
                    CONFIDENCE: [str(cld2_detection[0][1]),
                                 str(cld2_detection[1][1])]}
    else:
        if cld2_detection[0][1] > fastText_detection[1]:
            response = {DETECTED_LANGUAGE: [fastText_detection[0]],
                        CONFIDENCE: [str(fastText_detection[1])]}
        else:
            response = {DETECTED_LANGUAGE: [cld2_detection[0][0]],
                        CONFIDENCE: [str(cld2_detection[0][1])]}

    return response

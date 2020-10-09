from x5gon_rest.models.fasttext_model import get_or_create_fasttext_model, FastTextModel


def test_loading_quality_classifier():
    q_clf = get_or_create_fasttext_model()
    assert type(q_clf) == FastTextModel

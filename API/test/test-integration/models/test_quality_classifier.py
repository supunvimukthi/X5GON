from x5gon_quality.models.quality_classifier import get_or_create_quality_classifier, QualityModel


def test_loading_quality_classifier():
    q_clf = get_or_create_quality_classifier()
    assert type(q_clf) == QualityModel

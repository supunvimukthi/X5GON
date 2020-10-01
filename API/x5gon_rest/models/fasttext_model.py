from os.path import join
import fasttext

from x5gon_rest._configs import FASTTEXT_MODEL_DIR_PATH


class FastTextModel():
    def __init__(self, model):
        self.fastText_model = model

    @classmethod
    def create_from_dir(cls, dir_path):
        """instantiate a FastText model from available trained file

        Args:
            dir_path (str): directory path to where the FastText data model is stored

        Returns:
            (FastText Model): a FastText language Model object
        """

        # load the fasttext language model
        model_path = join(dir_path, "lid.176.ftz")
        model = fasttext.load_model(model_path)

        return cls(model)

    def predict(self, text):
        return self.fastText_model.predict(text)


#  =============== instantiate the global FastText model ====================

# global singleton FastText language model object that will be consumed by all requests
fasttext_model = None


def get_or_create_fasttext_model():
    """Gets an existing instance of new version of the fasttext model

    Returns:
        (FastText Model): singleton FastText language model

    """
    global fasttext_model

    if fasttext_model is None:
        fasttext_model = FastTextModel.create_from_dir(FASTTEXT_MODEL_DIR_PATH)

    return fasttext_model

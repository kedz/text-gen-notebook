import ipywidgets as widgets


class TargetEmbeddingContextWidget(object):
    def __init__(self, vocabs):
        self._vocabs = vocabs
        self._w_vocabs = widgets.Dropdown(options=vocabs.keys(),
                                          description="Vocab:")
        self._vocabs.link_dropdown(self._w_vocabs)

        self._w_ftr_name = widgets.Text(description="Feature:")
        self._w_emb_dim = widgets.IntText(value=512,
                                          min=1, max=9999,
                                          description="Emb. Dim.")

        self._w_emb_dropout = widgets.FloatText(value=0,
                                                min=0, max=1,
                                                description="Emb. Dropout")

        self._w_main = widgets.VBox([
            widgets.HBox([self._w_ftr_name, self._w_vocabs]),
            widgets.HBox([self._w_emb_dim, self._w_emb_dropout]),
        ])

    def __call__(self):
        return self._w_main

    @property
    def params(self):
        return {
            "feature": self._w_ftr_name.value,
            "embedding_dim": self._w_emb_dim.value,
            "embedding_dropout": self._w_emb_dropout.value,
            "vocab": self._w_vocabs.value,
        }

    @params.setter
    def params(self, new_params):
        self._w_emb_dim.value = new_params["embedding_dim"]
        self._w_emb_dropout.value = new_params["embedding_dropout"]
        self._w_ftr_name.value = new_params["feature"]
        self._w_vocabs.value = new_params["vocab"]

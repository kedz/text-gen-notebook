import ipywidgets as widgets
from tgnb.canonical_dict import CanonicalDict


class SourceEmbeddingContextWidget(object):
    def __init__(self, vocabs):
        self._vocabs = vocabs
        self._w_vocabs = widgets.Dropdown(options=vocabs.keys(),
                                          description="Vocab:")
        self._vocabs.link_dropdown(self._w_vocabs)

        self._emb_ctxs = CanonicalDict()
        self._w_emb_ctxs = widgets.Dropdown(options=[],
                                            description="Emb. Ctx.")
        self._emb_ctxs.link_dropdown(self._w_emb_ctxs)
        self._w_emb_ctxs.observe(self._selector_handler, names=["value"])

        self._w_ftr_name = widgets.Text(description="Feature:")
        self._w_emb_dim = widgets.IntText(value=512,
                                          min=1, max=9999,
                                          description="Emb. Dim.")

        self._w_emb_dropout = widgets.FloatText(value=0,
                                                min=0, max=1,
                                                description="Emb. Dropout")
        self._w_add_ctx_button = widgets.Button(description="Add Emb. Ctx.")
        self._w_del_ctx_button = widgets.Button(description="Del. Emb. Ctx.")
        self._w_add_ctx_button.on_click(self._add_ctx_handler)
        self._w_del_ctx_button.on_click(self._del_ctx_handler)

        self._w_main = widgets.VBox([
            self._w_emb_ctxs,
            widgets.HBox([self._w_ftr_name, self._w_vocabs]),
            widgets.HBox([self._w_emb_dim, self._w_emb_dropout]),
            widgets.HBox([self._w_add_ctx_button, self._w_del_ctx_button]),
        ])

    def __call__(self):
        return self._w_main

    def _add_ctx_handler(self, button):
        ftr = self._w_ftr_name.value.strip()
        if ftr == "":
            return
        params = {"embedding_dim": self._w_emb_dim.value,
                  "embedding_dropout": self._w_emb_dropout.value,
                  "feature": ftr,
                  "vocab": self._w_vocabs.value}
        self._emb_ctxs[ftr] = params
        self._w_emb_ctxs.value = ftr

    def _del_ctx_handler(self, button):
        ftr = self._w_emb_ctxs.value
        if ftr is None:
            return
        del self._emb_ctxs[ftr]

    def _selector_handler(self, change):
        ftr = change["new"]
        if ftr is None:
            return 
        params = self._emb_ctxs[ftr]
        self._w_emb_dim.value = params["embedding_dim"]
        self._w_emb_dropout.value = params["embedding_dropout"]
        self._w_ftr_name.value = ftr
        self._w_vocabs.value = params["vocab"]

    @property
    def params(self):
        return {
            "embedding_contexts": {ftr: dict(vals) 
                                   for ftr, vals in self._emb_ctxs.items()}
        }

    @params.setter
    def params(self, new_params):
        self._emb_ctxs.clear()
        self._emb_ctxs.update(new_params["embedding_contexts"])

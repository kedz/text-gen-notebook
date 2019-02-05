import ipywidgets as widgets
from .source_embedding_context import SourceEmbeddingContextWidget
from tgnb.canonical_dict import CanonicalDict


class SourceEmbeddingContextCreatorWidget(object):
    def __init__(self, vocabs):

        self._ecs = CanonicalDict()
        self._w_ecs = widgets.Dropdown(options=[],
                                       description="Emb. Ctxs.")
        self._ecs.link_dropdown(self._w_ecs)
        self._w_ecs.observe(self._selector_handler, names=["value"])
        self._w_ec = SourceEmbeddingContextWidget(vocabs)

        self._w_create = widgets.Button(description="Create")
        self._w_create.on_click(self._create_handler)
        self._w_delete = widgets.Button(description="Delete")
        self._w_delete.on_click(self._delete_handler)
        self._w_ec_name = widgets.Text(
            value="src-ec-{}".format(len(self._ecs)),
            description="Name:")

        self._w_main = widgets.VBox([
            self._w_ecs,
            self._w_ec(),
            self._w_ec_name,
            widgets.HBox([self._w_create, self._w_delete]),

        ])

    def __call__(self):
        return self._w_main

    def _create_handler(self, button):
        name = self._w_ec_name.value.strip()
        if name == "":
            return
        params = self._w_ec.params 
        self._ecs[name] = params
        self._w_ecs.value = name

    def _delete_handler(self, button):
        name = self._w_ecs.value
        if name is not None:
            del self._ecs[name]

    def _selector_handler(self, change):
        name = change["new"]
        if name is not None:
            self._w_ec.params = self._ecs[name]
            self._w_ec_name.value = name

    @property
    def params(self):
        return {
            "__type__": "SourceEmbeddingContextCreatorWidget",
            "embedding_contexts": self._ecs,
        }

    @params.setter
    def params(self, new_params):
        self._ecs.clear()
        self._ecs.update(new_params["embedding_contexts"])

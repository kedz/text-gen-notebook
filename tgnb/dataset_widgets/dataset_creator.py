import ipywidgets as widgets
from .seq2seq_file_dataset import Seq2SeqFileDatasetWidget
from tgnb.canonical_dict import CanonicalDict


class DatasetCreatorWidget(object):
    def __init__(self, params=None):

        self._w_datasets = widgets.Dropdown(options=[], description="Dataset:")
        self._w_dataset = Seq2SeqFileDatasetWidget()
        self._w_save = widgets.Button(description="Save")
        self._w_delete = widgets.Button(description="Delete")
        self._datasets = CanonicalDict()
        self._datasets.link_dropdown(self._w_datasets)

        self._w_main = widgets.VBox([
            self._w_datasets,
            self._w_dataset(),
            widgets.HBox([self._w_save, self._w_delete]),
        ])
        
        self._w_datasets.observe(self._selector_change, names=["value"])
        self._w_save.on_click(self._save_callback)
        self._w_delete.on_click(self._delete_callback)

    def __call__(self):
        return self._w_main

    def _selector_change(self, change):
        name = change["new"]
        if name is not None:
            self._w_dataset.params = self._datasets[name]

    def _save_callback(self, button):
        params = self._w_dataset.params
        self._datasets[params["__name__"]] = params
        self._w_datasets.value = params["__name__"]

    def _delete_callback(self, button):
        if self._w_datasets.value is not None:
            del self._datasets[self._w_datasets.value]

    @property
    def params(self):
        return {
            "__type__": "DatasetCreatorWidget",
            "datasets": self._datasets
        }

    @params.setter
    def params(self, new_params):
        self._datasets.clear()
        self._datasets.update(new_params["datasets"])

    @property
    def link(self):
        return self._datasets

import ipywidgets as widgets
from tgnb.canonical_dict import CanonicalDict
from nnsum.data import RAMDataset


class WordListCreatorWidget(object):
    def __init__(self, datasets, params=None):
        self._datasets = datasets
        self._word_lists = CanonicalDict()
        self._w_word_lists = widgets.Dropdown(options=[],
                                              description="Word Lists:")
        self._word_lists.link_dropdown(self._w_word_lists)
        #self._w_word_lists.observe(self._selector_change, names=["value"])

        self._w_datasets = widgets.Dropdown(options=datasets.keys(),
                                            description="Dataset:")
        self._datasets.link_dropdown(self._w_datasets)
        self._w_part = widgets.Dropdown(options=["source", "target"],
                                            description="Part")

        self._w_create = widgets.Button(description="Create")
        self._w_delete = widgets.Button(description="Delete")
        self._w_create.on_click(self._create_callback)
         
        self._w_main = widgets.VBox([
            self._w_word_lists,
            widgets.HBox([self._w_datasets, self._w_part]),
            widgets.HBox([self._w_create, self._w_delete]),
            widgets.Label(),
        ])            

    def __call__(self):
        return self._w_main

    def _create_callback(self, button):
        ds_name = self._w_datasets.value
        ds_part = self._w_part.value
        dataset = RAMDataset(self._datasets[ds_name][ds_part])
        word_counts = dataset.word_counts()
        names = []
        for ftr, counts in word_counts.items():
            wl_name = ds_name + ":" + ds_part + ":" + ftr
            self._word_lists[wl_name] = counts
            names.append(wl_name)
            self._w_word_lists.value = wl_name
        self._w_main.children[-1].value = "Created: {}".format(
            ", ".join(names))
        
    def _delete_callback(self, button):
        wl_name = self._w_word_lists.value
        if wl_name is not None:
            del self._word_lists[wl_name]

    @property
    def params(self):
        return {"__type__": "WordListCreatorWidget",
                "word_lists": self._word_lists}

    @params.setter
    def params(self, new_params):
        self._word_lists.clear()
        self._word_lists.update(new_params["word_lists"])

    @property
    def link(self):
        return self._word_lists

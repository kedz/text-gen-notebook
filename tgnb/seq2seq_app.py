import ipywidgets as widgets
from .dataset_widgets import DatasetCreatorWidget, DatasetExplorerWidget
from .vocab_widgets import WordListCreatorWidget, Seq2SeqVocabWidget
from .embedding_context_widgets import (
    SourceEmbeddingContextCreatorWidget, TargetEmbeddingContextCreatorWidget)

import os
import json


class Seq2SeqApp(object):
    
    def __init__(self, save_path=None):
        self._save_path = save_path
        self._w_datasets = DatasetCreatorWidget()
        self._w_dataset_explorer = DatasetExplorerWidget(self._w_datasets.link)
        self._w_word_lists = WordListCreatorWidget(self._w_datasets.link)

        self._w_vocabs = Seq2SeqVocabWidget(self._w_word_lists.link)
        self._w_src_ec = SourceEmbeddingContextCreatorWidget(
            self._w_vocabs.source_vocabs)
        self._w_tgt_ec = TargetEmbeddingContextCreatorWidget(
            self._w_vocabs.target_vocabs)

        self._w_save = widgets.Button(description="Save")
        self._w_save.on_click(self._save_callback)     
   
        self._w_main = widgets.VBox([
            widgets.Label("Dataset Creator"),
            self._w_datasets(),
            #widgets.Label(),
            #widgets.Label("Dataset Explorer"),
            #self._w_dataset_explorer(),
            widgets.Label(),
            widgets.Label("Word List Creator"),
            self._w_word_lists(),
            widgets.Label(),
            self._w_vocabs(),
            widgets.Label(),
            widgets.Label("Source Embedding Context"),
            self._w_src_ec(),
            widgets.Label(),
            widgets.Label("Target Embedding Context"),
            self._w_tgt_ec(),
            self._w_save,
        ])

        self._stateful_w = [self._w_datasets, self._w_word_lists,
                            self._w_vocabs, self._w_src_ec, self._w_tgt_ec]

        self._load_params()

    def __call__(self):
        return self._w_main

    def _save_callback(self, button):
        if self._save_path is None:
            return
        with open(self._save_path, "w") as fp:
            params = {}
            for w in self._stateful_w:
                params[type(w).__name__] = w.params
            fp.write(json.dumps(params))

    def _load_params(self):
        if self._save_path and os.path.exists(self._save_path):
            with open(self._save_path, "r") as fp:
                params = json.loads(fp.read())
                for w in self._stateful_w:
                    name = type(w).__name__
                    if name in params:
                        print(name, "OK")
                        w.params = params[name]
                    else:
                        print(name, "MISS")

import ipywidgets as widgets
from .vocab_creator import SourceVocabCreatorWidget, TargetVocabCreatorWidget


class Seq2SeqVocabWidget(object):
    def __init__(self, word_lists):
        self._w_src_vocabs = SourceVocabCreatorWidget(word_lists)
        self._w_tgt_vocabs = TargetVocabCreatorWidget(word_lists)

        self._w_main = widgets.VBox([
            widgets.Label("Source Vocab Creator"),
            self._w_src_vocabs(),
            widgets.Label("Target Vocab Creator"),
            self._w_tgt_vocabs(),
        ])

    def __call__(self):
        return self._w_main

    @property
    def params(self):
        return {
            "__type__": "Seq2SeqVocabWidget",
            "source_vocab": self._w_src_vocabs.link,
            "target_vocab": self._w_tgt_vocabs.link
        }

    @params.setter
    def params(self, new_params):
        self._w_src_vocabs.link = new_params["source_vocab"]
        self._w_tgt_vocabs.link = new_params["target_vocab"]

    @property
    def source_vocabs(self):
        return self._w_src_vocabs.link

    @property
    def target_vocabs(self):
        return self._w_tgt_vocabs.link



import ipywidgets as widgets
from tgnb.canonical_dict import CanonicalDict

class SourceVocabCreatorWidget(object):
    def __init__(self, word_lists, params=None):

        self._vocabs = CanonicalDict()
        self._w_vocabs = widgets.Dropdown(options=[],
                                          description="Vocabs:")
        self._vocabs.link_dropdown(self._w_vocabs)
        self._w_vocabs.observe(self._selector_change, names=["value"])

        self._word_lists = word_lists
        self._w_word_lists = widgets.Dropdown(options=word_lists.keys(),
                                              description="Word Lists:")
        self._w_word_lists.observe(lambda x: self._select_word_list_callback(),
                                   names=["value"])
        self._word_lists.link_dropdown(self._w_word_lists)
        self._w_vocab_size = widgets.IntSlider(min=1, max=1, value=1,
                                               description="Max V. Size:")
        self._w_vocab_size.observe(lambda x: self._calculate_vocab_size(),
                                   names=["value"])
        self._w_min_count = widgets.IntSlider(min=1, max=1, value=1,
                                              description="Min Freq.:")
        self._w_min_count.observe(lambda x: self._calculate_vocab_size(),
                                  names=["value"])
        self._w_actual_vocab_size = widgets.Label(
            description="Actual V. Size:")
        self._w_unk_rate = widgets.Label()

        self._w_start_token = widgets.Text(value="<sos>",
                                           description="Start Tkn:")
        self._w_pad_token = widgets.Text(value="<pad>",
                                         description="Pad Tkn:")
        self._w_unk_token = widgets.Text(value="<unk>",
                                         description="Unk Tkn:")
        self._w_name = widgets.Text(
            value="target_vocab-{}".format(len(self._vocabs)),
            description="Name:")

        self._w_create = widgets.Button(description="Create")
        self._w_create.on_click(self._create_callback)

        self._w_delete = widgets.Button(description="Delete")
        self._w_delete.on_click(self._delete_callback)

        self._w_main = widgets.VBox([
            self._w_vocabs,
            widgets.HBox([self._w_word_lists, self._w_name]),
            widgets.HBox([self._w_min_count, self._w_vocab_size,]),
            widgets.HBox([self._w_start_token]),
            widgets.HBox([self._w_pad_token, self._w_unk_token]),
            widgets.VBox([self._w_actual_vocab_size, 
                          self._w_unk_rate]),
            widgets.HBox([self._w_create, self._w_delete]),
        ])

        self._select_word_list_callback()


    def __call__(self):
        return self._w_main

    def _select_word_list_callback(self):
        wl_name = self._w_word_lists.value
        if wl_name is None:
            return
        wl = self._word_lists[wl_name]
        self._sorted_word_list = sorted(wl.items(), 
                                        key=lambda x: x[0], reverse=True)
        self._sorted_word_list.sort(key=lambda x: x[1], reverse=True)
        
        self._w_vocab_size.min = 1 
        self._w_vocab_size.value = 1 
        self._w_vocab_size.max = len(wl)
        self._w_vocab_size.value = len(wl)

        self._w_min_count.min = 0
        self._w_min_count.value = 0
        self._w_min_count.max = max(wl.values())

        self._calculate_vocab_size()

    def _calculate_vocab_size(self):
        counts = self._sorted_word_list[:self._w_vocab_size.value]
        counts = [wc for wc in counts if wc[1] >= self._w_min_count.value]
        self._actual_vsize = len(counts)
        self._w_actual_vocab_size.value = "Actual Vocab Size: {}".format(
            self._actual_vsize)

        total_freq = sum([wc[1] for wc in self._sorted_word_list])
        self._unk_rate = 100 * (1 - sum([wc[1] for wc in counts]) / total_freq)
        self._w_unk_rate.value = "Unknown Word Rate: {:5.3f}%".format(
            self._unk_rate)
        
    @property
    def params(self):
        return {
            "__type__": "SourceVocabCreatorWidget",
            "word_list": self._w_word_lists.value,
            "max_size": self._w_vocab_size.value,
            "min_count": self._w_min_count.value,
            "start_token": self._w_start_token.value,
            "unk_token": self._w_unk_token.value,
            "pad_token": self._w_pad_token.value,
            "actual_vocab_size": self._actual_vsize,
            "unknown_word_rate": self._unk_rate,
            "name": self._w_name.value.strip(),
        }

    @params.setter
    def params(self, new_params):
        self._w_word_lists.value = new_params["word_list"]
        self._w_vocab_size.value = new_params["max_size"]
        self._w_min_count.value = new_params["min_count"]
        self._w_start_token.value = new_params["start_token"]
        self._w_pad_token.value = new_params["pad_token"]
        self._w_unk_token.value = new_params["unk_token"]
        self._actual_vsize = new_params["actual_vocab_size"]
        self._unk_rate = new_params["unknown_word_rate"]
        self._w_name.value = new_params["name"]
            
    def _create_callback(self, button):
        params = self.params
        if params["name"] == "":
            return
        self._vocabs[params["name"]] = params
        self._w_vocabs.value = params["name"]
        self._w_name.value = "source-vocab-{}".format(len(self._vocabs))
        
    def _delete_callback(self, button):
        if self._w_vocabs.value is not None:
            del self._vocabs[self._w_vocabs["name"]]

    def _selector_change(self, change):
        if change["new"] is not None:
            self.params = self._vocabs[change["new"]]

    @property
    def link(self):
        return self._vocabs

    @link.setter
    def link(self, new_link):
        self._vocabs.clear()
        self._vocabs.update(new_link)

class TargetVocabCreatorWidget(object):
    def __init__(self, word_lists, params=None):

        self._vocabs = CanonicalDict()
        self._w_vocabs = widgets.Dropdown(options=[],
                                          description="Vocabs:")
        self._vocabs.link_dropdown(self._w_vocabs)
        self._w_vocabs.observe(self._selector_change, names=["value"])

        self._word_lists = word_lists
        self._w_word_lists = widgets.Dropdown(options=word_lists.keys(),
                                              description="Word Lists:")
        self._w_word_lists.observe(lambda x: self._select_word_list_callback(),
                                   names=["value"])
        self._word_lists.link_dropdown(self._w_word_lists)
        self._w_vocab_size = widgets.IntSlider(min=1, max=1, value=1,
                                               description="Max V. Size:")
        self._w_vocab_size.observe(lambda x: self._calculate_vocab_size(),
                                   names=["value"])
        self._w_min_count = widgets.IntSlider(min=1, max=1, value=1,
                                              description="Min Freq.:")
        self._w_min_count.observe(lambda x: self._calculate_vocab_size(),
                                  names=["value"])
        self._w_actual_vocab_size = widgets.Label(
            description="Actual V. Size:")
        self._w_unk_rate = widgets.Label()

        self._w_start_token = widgets.Text(value="<sos>",
                                           description="Start Tkn:")
        self._w_stop_token = widgets.Text(value="<eos>",
                                           description="Stop Tkn:")
        self._w_pad_token = widgets.Text(value="<pad>",
                                         description="Pad Tkn:")
        self._w_unk_token = widgets.Text(value="<unk>",
                                         description="Unk Tkn:")
        self._w_name = widgets.Text(
            value="target_vocab-{}".format(len(self._vocabs)),
            description="Name:")

        self._w_create = widgets.Button(description="Create")
        self._w_create.on_click(self._create_callback)

        self._w_delete = widgets.Button(description="Delete")
        self._w_delete.on_click(self._delete_callback)

        self._w_main = widgets.VBox([
            self._w_vocabs,
            widgets.HBox([self._w_word_lists, self._w_name]),
            widgets.HBox([self._w_min_count, self._w_vocab_size,]),
            widgets.HBox([self._w_start_token, self._w_stop_token]),
            widgets.HBox([self._w_pad_token, self._w_unk_token]),
            widgets.VBox([self._w_actual_vocab_size, 
                          self._w_unk_rate]),
            widgets.HBox([self._w_create, self._w_delete]),
        ])

        self._select_word_list_callback()


    def __call__(self):
        return self._w_main

    def _select_word_list_callback(self):
        wl_name = self._w_word_lists.value
        if wl_name is None:
            return
        wl = self._word_lists[wl_name]
        self._sorted_word_list = sorted(wl.items(), 
                                        key=lambda x: x[0], reverse=True)
        self._sorted_word_list.sort(key=lambda x: x[1], reverse=True)
        
        self._w_vocab_size.min = 1 
        self._w_vocab_size.value = 1 
        self._w_vocab_size.max = len(wl)
        self._w_vocab_size.value = len(wl)

        self._w_min_count.min = 0
        self._w_min_count.value = 0
        self._w_min_count.max = max(wl.values())

        self._calculate_vocab_size()

    def _calculate_vocab_size(self):
        counts = self._sorted_word_list[:self._w_vocab_size.value]
        counts = [wc for wc in counts if wc[1] >= self._w_min_count.value]
        self._actual_vsize = len(counts)
        self._w_actual_vocab_size.value = "Actual Vocab Size: {}".format(
            self._actual_vsize)

        total_freq = sum([wc[1] for wc in self._sorted_word_list])
        self._unk_rate = 100 * (1 - sum([wc[1] for wc in counts]) / total_freq)
        self._w_unk_rate.value = "Unknown Word Rate: {:5.3f}%".format(
            self._unk_rate)
        
    @property
    def params(self):
        return {
            "__type__": "TargetVocabCreatorWidget",
            "word_list": self._w_word_lists.value,
            "max_size": self._w_vocab_size.value,
            "min_count": self._w_min_count.value,
            "start_token": self._w_start_token.value,
            "stop_token": self._w_stop_token.value,
            "unk_token": self._w_unk_token.value,
            "pad_token": self._w_pad_token.value,
            "actual_vocab_size": self._actual_vsize,
            "unknown_word_rate": self._unk_rate,
            "name": self._w_name.value.strip(),
        }

    @params.setter
    def params(self, new_params):
        self._w_word_lists.value = new_params["word_list"]
        self._w_vocab_size.value = new_params["max_size"]
        self._w_min_count.value = new_params["min_count"]
        self._w_start_token.value = new_params["start_token"]
        self._w_stop_token.value = new_params["stop_token"]
        self._w_pad_token.value = new_params["pad_token"]
        self._w_unk_token.value = new_params["unk_token"]
        self._actual_vsize = new_params["actual_vocab_size"]
        self._unk_rate = new_params["unknown_word_rate"]
        self._w_name.value = new_params["name"]
            
    def _create_callback(self, button):
        params = self.params
        if params["name"] == "":
            return
        self._vocabs[params["name"]] = params
        self._w_vocabs.value = params["name"]
        self._w_name.value = "target-vocab-{}".format(len(self._vocabs))
        
    def _delete_callback(self, button):
        if self._w_vocabs.value is not None:
            del self._vocabs[self._w_vocabs["name"]]

    def _selector_change(self, change):
        if change["new"] is not None:
            self.params = self._vocabs[change["new"]]

    @property
    def link(self):
        return self._vocabs

    @link.setter
    def link(self, new_link):
        self._vocabs.clear()
        self._vocabs.update(new_link)


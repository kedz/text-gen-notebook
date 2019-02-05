import ipywidgets as widgets


class Seq2SeqFileDatasetWidget(object):
    def __init__(self, params=None):
        
        self._w_source = widgets.Text(
            value="", description="Source:")
        self._w_target = widgets.Text(
            value="", description="Target:")
        self._w_name = widgets.Text(description="Name:")

        self._w_main = widgets.VBox([
            widgets.HBox([self._w_source, self._w_target,]),
            self._w_name,
        ])

        if params is not None:
            self.params = params

    def __call__(self):
        return self._w_main

    @property
    def params(self):
        return {
            "__type__": "Seq2SeqFileDatasetWidget",
            "__name__": self._w_name.value,
            "source": self._w_source.value,
            "target": self._w_target.value,
        }

    @params.setter
    def params(self, new_params):
        self._w_source.value = new_params["source"]
        self._w_target.value = new_params["target"]
        self._w_name.value = new_params["__name__"]

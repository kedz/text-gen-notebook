import ipywidgets as widgets

from nnsum.data import RAMDataset, AlignedDataset


class DatasetExplorerWidget(object):
    def __init__(self, datasets):
        
        self._datasets = datasets
        self._w_datasets = widgets.Dropdown(options=datasets.keys())
        self._w_datasets.observe(self._selector_change, names=["value"])
        self._datasets.link_dropdown(self._w_datasets)
        
        self._open_menus = {}

        self._w_example = None # widgets.IntSlider(min=1, max=


        self._w_main = widgets.VBox([
            self._w_datasets,
            widgets.Label(),
        ])

        

    def __call__(self):
        return self._w_main
            
    def _new_menu(self, dataset):
        sel = widgets.IntSlider(min=1, max=len(dataset), value=1,
                                description="Example:")
        src_pad = widgets.HTML()
        tgt_pad = widgets.HTML()
        w = widgets.VBox([
            sel, widgets.Label("Source"), src_pad, widgets.Label("Target"),
            tgt_pad
        ])

        td = '<td style="padding: 15px;">{}</td>'

        def ex(change):
            example = dataset[sel.value - 1]
            src_data = []
            for key, tokens in example["source"].items():
                row = "<td><b>{}</b></td>".format(key) + "\n".join(
                    [td.format(token) for token in tokens])
                src_data.append("<tr>" + row + "</tr>")
            src_pad.value = "<table>" + "".join(src_data) + "</table>"

            tgt_data = []
            for key, tokens in example["target"].items():
                row = "<td><b>{}</b></td>".format(key) + "\n".join(
                    [td.format(token) for token in tokens])
                tgt_data.append("<tr>" + row + "</tr>")
            tgt_pad.value = "<table>" + "".join(tgt_data) + "</table>"



        sel.observe(ex, names=["value"])


        return {"widget": w, "dataset": dataset}    


    def _selector_change(self, change):
        if change["new"] is None:
            return
        name = change["new"]
        dataset_params = self._datasets[name]
        if name not in self._open_menus:
            src = RAMDataset(dataset_params["source"])
            tgt = RAMDataset(dataset_params["target"])
            dataset = AlignedDataset(src, tgt)
            self._open_menus[name] = self._new_menu(dataset)
        self._w_main.children = [self._w_main.children[0]] \
            + [self._open_menus[name]["widget"]]
        

        



class CanonicalDict(dict):
    
    def __init__(self, *args, **kwargs):
        super(CanonicalDict, self).__init__(*args, **kwargs)
        self._dropdowns = []        

    def link_dropdown(self, dropdown):
        dropdown.options = self.keys()
        self._dropdowns.append(dropdown)

    def __setitem__(self, key, val):
        needs_refresh = key not in self

        super(CanonicalDict, self).__setitem__(key, val)
        if needs_refresh:
            for d in self._dropdowns:
                d.options = self.keys()

    def __delitem__(self, key):
        super(CanonicalDict, self).__delitem__(key)
        for d in self._dropdowns:
            d.options = self.keys()

    def update(self, new_dict):
        super(CanonicalDict, self).update(new_dict)
        for d in self._dropdowns:
            d.options = self.keys()

    def clear(self):
        super(CanonicalDict, self).clear()
        for d in self._dropdowns:
            d.options = self.keys()

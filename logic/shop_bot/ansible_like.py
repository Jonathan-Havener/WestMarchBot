from pathlib import Path
import yaml


class AnsibleLike:
    def __init__(self, source: [Path] = None):
        self._load_properties(source)

    def _merge_properties(self, data):
        # This function will merge properties from parents to children
        if isinstance(data, dict):
            for key, value in data.items():
                # Recursively merge properties of subkeys
                data[key] = self._merge_properties(value)
            if "child_key" in data:
                other_data = {key: data[key] for key in data if key != "child_key"}
                data = {
                    child: data["child_key"][child]
                    for child in data["child_key"].keys()
                }
                for key in data:
                    data[key].update(other_data)
        return data

    def _load_properties(self, filename):
        with open(filename, 'r') as file:
            self.data = yaml.safe_load(file)  # Load YAML file
            self.data = self.data[list(self.data.keys())[0]]
            self.data = self._merge_properties(self.data)
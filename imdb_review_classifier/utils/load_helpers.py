from typing import Any, Dict, Text

import yaml


def load_params(path_to_config: Text) -> Dict[Text, Any]:
    with open(path_to_config) as stream:
        config = yaml.safe_load(stream.read())
        return config

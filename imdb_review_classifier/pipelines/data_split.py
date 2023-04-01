from pathlib import Path
from typing import Any, Dict, Text

import click
import pandas as pd
from sklearn import model_selection as ms

from imdb_review_classifier.utils.load_helpers import load_params


def data_split(config: Dict[Text, Any]) -> None:
    dataset_path = config["data_split"]["raw_data"]
    train_dataset_path = config["data_split"]["train_path"]
    test_dataset_path = config["data_split"]["test_path"]
    test_size = config["data_split"]["test_size"]

    dataset = pd.read_csv(dataset_path)

    # Split in train/test
    df_train, df_test = ms.train_test_split(
        dataset, test_size=test_size, **config["base"]["seed"]
    )

    train_dataset_path = Path(train_dataset_path)
    train_dataset_path.parent.mkdir(parents=True, exist_ok=True)

    test_dataset_path = Path(test_dataset_path)
    test_dataset_path.parent.mkdir(parents=True, exist_ok=True)

    df_train.to_csv(train_dataset_path, index=False)
    df_test.to_csv(test_dataset_path, index=False)


@click.command()
@click.option("--path_to_config", help="Path to params.yaml")
def main(path_to_config: Text) -> None:
    data_split(config=load_params(path_to_config))


if __name__ == "__main__":
    main()

from pathlib import Path
from typing import Any, Dict, Text

import click
import pandas as pd
import torch
from sklearn.feature_extraction.text import CountVectorizer

from imdb_review_classifier.utils.load_helpers import load_params


def create_features(config: Dict[Text, Any]) -> None:
    path_to_train_data = config["data_split"]["train_path"]
    data = pd.read_csv(path_to_train_data)

    count_vec = CountVectorizer(**config["features"]["vectorizer"])

    count_vec.fit(data.review.values)

    train_data = count_vec.transform(data.review.values)
    target_train = data.sentiment.apply(
        lambda x: 1 if x == "positive" else 0
    ).values

    model_path = config["features"]["save"]["model_file_name"]
    model_path = Path(model_path)

    data_path = config["features"]["save"]["train_data"]
    data_path = Path(data_path)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.parent.mkdir(parents=True, exist_ok=True)

    torch.save(
        {config["features"]["save"]["model_file_name"]: count_vec}, model_path
    )

    torch.save(
        {
            config["features"]["save"]["train_data_file"]: train_data,
            config["features"]["save"]["target_train_file"]: target_train,
        },
        data_path,
    )


@click.command()
@click.option("--path_to_config", help="Path to path_to_config")
def main(path_to_config: Text) -> None:
    create_features(config=load_params(path_to_config))


if __name__ == "__main__":
    main()

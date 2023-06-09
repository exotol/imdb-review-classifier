from typing import Any, Dict, Text

import click
import torch
from sklearn import linear_model as lm
from sklearn import svm
from sklearn.base import BaseEstimator

from imdb_review_classifier.utils.load_helpers import load_params


def create_model(config: Dict[Text, Any]) -> BaseEstimator:
    if config["train"]["model"]["type"] == "LogisticRegression":
        model = lm.LogisticRegression(random_state=config["base"]["seed"])
    elif config["train"]["model"]["type"] == "LinearSVC":
        model = svm.LinearSVC(random_state=config["base"]["seed"])
    return model


def train_model(config: Dict[Text, Any]) -> None:
    train_data_path = config["features"]["save"]["train_data"]
    loaded_data = torch.load(train_data_path)
    x_train = loaded_data[config["features"]["save"]["train_data_file"]]
    y_train = loaded_data[config["features"]["save"]["target_train_file"]]

    model = create_model(config)

    model.fit(x_train, y_train)

    torch.save(
        {config["train"]["save"]["model_path"]: model},
        config["train"]["save"]["model_path"],
    )


@click.command()
@click.option("--path_to_config", help="Path to config file")
def main(path_to_config: Text) -> None:
    train_model(config=load_params(path_to_config))


if __name__ == "__main__":
    main()

from pathlib import Path

import click
import yaml
import pandas as pd
import torch
from typing import Text

from sklearn.feature_extraction.text import CountVectorizer


@click.command()
@click.option("--path_to_config", help="Path to path_to_config")
def main(path_to_config: Text) -> None:
    with open(path_to_config) as stream:
        config = yaml.safe_load(stream.read())

    path_to_train_data = config['data_split']['train_path']
    data = pd.read_csv(path_to_train_data)

    count_vec = CountVectorizer(
        **config['features']['vectorizer']
    )

    count_vec.fit(data.review.values)

    train_data = count_vec.transform(data.review.values)
    target_train = data.sentiment.values

    model_path = config['features']['save']['model_file_name']
    model_path = Path(model_path)

    data_path = config['features']['save']['train_data']
    data_path = Path(data_path)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.parent.mkdir(parents=True, exist_ok=True)

    torch.save({
        config['features']['save']['model_file_name']: count_vec
    }, model_path)

    torch.save({
        config['features']['save']['train_data_file']: train_data,
        config['features']['save']['target_train_file']: target_train
    }, data_path)


if __name__ == "__main__":
    main()

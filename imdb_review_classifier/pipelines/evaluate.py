import json
from typing import Any, Dict, Text

import click
import pandas as pd
import torch
from sklearn import metrics

from imdb_review_classifier.utils.load_helpers import load_params


def eval_metrics(config: Dict[Text, Any]) -> None:
    path_to_model = config["train"]["save"]["model_path"]
    path_to_vec = config["features"]["save"]["model_file_name"]
    path_to_data = config["data_split"]["test_path"]

    path_to_metrics = config["evaluate"]["save"]["metrics_file"]
    path_to_confusion_matrix = config["evaluate"]["save"]["confusion_matrix"]

    model = torch.load(path_to_model)[path_to_model]
    vectorizer = torch.load(path_to_vec)[path_to_vec]

    data = pd.read_csv(path_to_data)

    x_data = vectorizer.transform(data.review.values)
    target = data.sentiment.apply(lambda x: 1 if x == "positive" else 0).values

    y_prediction = model.predict(x_data)
    acc_score = metrics.accuracy_score(y_true=target, y_pred=y_prediction)

    json.dump(obj={"accuracy": acc_score}, fp=open(path_to_metrics, "w"))

    mapping = {
        i: cls_name for i, cls_name in enumerate(["negative", "positive"])
    }
    cmdf = pd.DataFrame({"actual": target, "predicted": y_prediction}).apply(
        lambda series: series.map(mapping)
    )
    cmdf.to_csv(path_to_confusion_matrix, index=False)


@click.command()
@click.option("--path_to_config", help="Path to config file yaml")
def main(path_to_config: Text) -> None:
    eval_metrics(config=load_params(path_to_config))


if __name__ == "__main__":
    main()

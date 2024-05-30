"""Hypothesis testing module."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, TypeAlias, TypeVar, Union, cast

import numpy as np
import pandas as pd
from scipy import stats

from happydogml.evaluation import evaluate
from happydogml.model import Model

T = TypeVar("T", bound="Dataset")

ArrayLike: TypeAlias = Union[np.ndarray, pd.DataFrame, list[float]]
Metric_T: TypeAlias = Literal["accuracy", "precision", "recall", "f1"]


@dataclass
class Dataset:
    X: ArrayLike
    y: ArrayLike


@dataclass
class HypothesisResult:
    t_statistic: float
    p_value: float
    significant: bool
    metrics_0: list[float]
    metrics_1: list[float]


class BaseHypothesisTester(ABC):
    @abstractmethod
    def test(
        self,
        model_0: Model,
        model_1: Model,
        dataset_0: Dataset,
        dataset_1: Dataset,
        metric: Metric_T = "accuracy",
    ) -> HypothesisResult:
        """Test the hypothesis that two models are equivalent."""


class TTest:
    """Class for conducting T-tests with support for dataset splitting and evaluation."""

    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha

    def test(
        self,
        model_0: Model,
        model_1: Model,
        dataset_0: Dataset,
        dataset_1: Dataset,
        metric: Metric_T = "accuracy",
        n_splits: int = 10,
    ) -> HypothesisResult:
        """
        Compares two models using a T-test based on a chosen metric.

        :param model_0: The first model to compare.
        :type model_0: Model
        :param model_1: The second model to compare.
        :type model_1: Model
        :param dataset_0: Dataset for the first model.
        :type dataset_0: Dataset
        :param dataset_1: Dataset for the second model.
        :type dataset_1: Dataset
        :param metric: The performance metric to test (e.g., 'accuracy', 'precision', 'recall', 'f1'). Default='accuracy'.
        :type metric: str
        :param n_splits: Number of splits for the dataset. Default=10.
        :type n_splits: int
        :return: A structured result of the T-test, including statistics and significance.
        :rtype: HypothesisResult

        Example::
            >>> model_a = SomeModel()
            >>> model_b = SomeModel()
            >>> data_a = Dataset(X=some_features_a, y=some_labels_a)
            >>> data_b = Dataset(X=some_features_b, y=some_labels_b)
            >>> tester = TTest()
            >>> result = tester.test(model_a, model_b, data_a, data_b, metric='f1')
            >>> print(result)
            HypothesisResult(t_statistic=2.345, p_value=0.019, significant=True)
        """
        metrics_0 = self.evaluate_model_on_splits(
            model_0, dataset_0, metric, n_splits
        )
        metrics_1 = self.evaluate_model_on_splits(
            model_1, dataset_1, metric, n_splits
        )

        t_stat, p_value = stats.ttest_ind(
            metrics_0, metrics_1, equal_var=False
        )

        return HypothesisResult(
            t_statistic=t_stat,
            p_value=p_value,
            significant=p_value < self.alpha,
            metrics_0=metrics_0,
            metrics_1=metrics_1,
        )

    def evaluate_model_on_splits(
        self, model: Model, dataset: Dataset, metric: Metric_T, n_splits: int
    ) -> list[float]:
        """Evaluate the model on multiple dataset splits and collect metrics."""
        dataset_splits = self.split_dataset(dataset, n_splits)
        metrics = [
            evaluate(model, X=split.X, y=split.y)[metric]
            for split in dataset_splits
        ]
        return cast(list[float], metrics)

    def split_dataset(self, dataset: Dataset, n: int) -> list[Dataset]:
        """Splits the dataset into `n` contiguous segments."""
        segment_size = len(dataset.X) // n
        return [
            Dataset(
                dataset.X[i * segment_size : (i + 1) * segment_size],
                dataset.y[i * segment_size : (i + 1) * segment_size],
            )
            for i in range(n - 1)
        ] + [
            Dataset(
                dataset.X[(n - 1) * segment_size :],
                dataset.y[(n - 1) * segment_size :],
            )
        ]

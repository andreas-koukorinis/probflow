"""Tests probflow.core.BaseDistribution class"""

import pytest

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions

from probflow import *


def test_BaseDistribution_fit():
    """Tests core.BaseDistribution.fit"""

    # Model = linear regression assuming error = 1
    weight = Parameter(estimator=None)
    bias = Parameter(estimator=None)
    data = Input()
    model = Normal(data*weight + bias, 1.0)

    # Generate data
    N = 10
    true_weight = 0.5
    true_bias = -1
    noise = np.random.randn(N)
    x = np.linspace(-3, 3, N)
    y = true_weight*x + true_bias + noise

    # Should return a RuntimeError
    with pytest.raises(RuntimeError):
        model._ensure_is_fit()

    # Fit the model
    model.fit(x, y, epochs=1)

    # Now should pass
    model._ensure_is_fit()

    # Check model contains data
    assert isinstance(model._train, dict)
    assert isinstance(model._train['x'], np.ndarray)
    assert isinstance(model._train['y'], np.ndarray)
    assert type(model._shuffled_ids) is np.ndarray
    assert isinstance(model._ph, dict)
    assert isinstance(model._ph['batch_size'], tf.Tensor)
    assert isinstance(model._ph['x'], tf.Tensor)
    assert isinstance(model._ph['y'], tf.Tensor)
    assert type(model.log_loss) is tf.Tensor
    assert type(model.mean_log_loss) is tf.Tensor
    assert type(model.kl_loss) is tf.Tensor
    assert type(model._session) is tf.Session
    assert model.is_fit


def test_BaseDistribution_sample_posterior_scalar():
    """Tests core.BaseDistribution.sample_posterior w/ scalar params"""

    # Model = linear regression assuming error = 1
    weight = Parameter(name='weight', estimator=None)
    bias = Parameter(name='bias', estimator=None)
    data = Input()
    model = Normal(data*weight + bias, 1.0)

    # Generate data
    N = 10
    true_weight = 0.5
    true_bias = -1
    noise = np.random.randn(N)
    x = np.linspace(-3, 3, N)
    y = true_weight*x + true_bias + noise

    # Fit the model
    model.fit(x, y, epochs=1)

    # Check output of sample_posterior is correct
    samples = model.sample_posterior(num_samples=3)
    assert isinstance(samples, dict)
    assert len(samples) == 2
    assert 'weight' in samples and 'bias' in samples
    assert type(samples['weight']) is np.ndarray
    assert samples['weight'].ndim == 2
    assert samples['weight'].shape[0] == 3
    assert samples['weight'].shape[1] == 1
    assert type(samples['bias']) is np.ndarray
    assert samples['bias'].ndim == 2
    assert samples['bias'].shape[0] == 3
    assert samples['bias'].shape[1] == 1


def test_BaseDistribution_sample_posterior_vector():
    """Tests core.BaseDistribution.sample_posterior w/ vector params"""

    # Parameters + input data is vector of length 3
    Nd = 3

    # Model = linear regression assuming error = 1
    weight = Parameter(name='vector_weight', shape=Nd, estimator=None)
    bias = Parameter(name='nonvec_bias', estimator=None)
    data = Input()
    model = Normal(Dot(data, weight) + bias, 1.0)

    # Generate data
    N = 10
    true_weight = np.array([0.5, -0.25, 0.0])
    true_bias = -1.0
    noise = np.random.randn(N, 1)
    x = np.random.randn(N, Nd)
    y = np.expand_dims(np.sum(true_weight*x, axis=1) + true_bias, 1) + noise

    # Fit the model
    model.fit(x, y, epochs=1)

    # Check output of sample_posterior is correct
    num_samples = 3
    samples = model.sample_posterior(num_samples=num_samples)
    assert isinstance(samples, dict)
    assert len(samples) == 2
    assert samples['vector_weight'].ndim == 2
    assert samples['vector_weight'].shape[0] == num_samples
    assert samples['vector_weight'].shape[1] == Nd
    assert samples['nonvec_bias'].ndim == 2
    assert samples['nonvec_bias'].shape[0] == num_samples
    assert samples['nonvec_bias'].shape[1] == 1


def test_BaseDistribution_sample_posterior_vector_pandas():
    """Tests core.BaseDistribution.sample_posterior + fit w/ pandas input"""

    # Parameters + input data is vector of length 3
    Nd = 3

    # Model = linear regression assuming error = 1
    weight = Parameter(name='pd_weight', shape=Nd, estimator=None)
    bias = Parameter(name='pd_bias', estimator=None)
    data = Input()
    model = Normal(Dot(data, weight) + bias, 1.0)

    # Generate data
    N = 10
    true_weight = np.array([0.5, -0.25, 0.0])
    true_bias = -1.0
    noise = np.random.randn(N)
    x = np.random.randn(N, Nd+1)
    x[:,0] = np.sum(true_weight*x[:,1:], axis=1) + true_bias + noise
    df = pd.DataFrame(x, columns=['a', 'b', 'c', 'd'])

    # Fit the model
    model.fit(['b', 'c', 'd'], 'a', data=df, epochs=1)

    # Check output of sample_posterior is correct
    num_samples = 3
    samples = model.sample_posterior(num_samples=num_samples)
    assert isinstance(samples, dict)
    assert len(samples) == 2
    assert samples['pd_weight'].ndim == 2
    assert samples['pd_weight'].shape[0] == num_samples
    assert samples['pd_weight'].shape[1] == Nd
    assert samples['pd_bias'].ndim == 2
    assert samples['pd_bias'].shape[0] == num_samples
    assert samples['pd_bias'].shape[1] == 1




# TODO: test 2D X and params


# TODO: test vector Y


# TODO: test 2D Y


# TODO: test the shuffles work _initialize_shuffles


# TODO: test that the flipout estimator works?


# TODO: test the batches are being generated correctly _generate_batch


# TODO: test the validation splitting / shuffling happens correctly


# Tests for plot_posterior and plot_prior are in test_plot_posterior/prior


# TODO: test predictive_distribution, predict, metrics, etc
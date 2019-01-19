"""Common already-made models.

TODO: more info...

* :func:`.LinearRegression`
* :func:`.LogisticRegression`
* :func:`.DenseNet`
* :func:`.DenseRegression`
* :func:`.DenseClassifier`

----------

"""



from .parameters import Parameter, ScaleParameter
from .layers import *
from .distributions import *


__all__ = [
    'LinearRegression',
    'LogisticRegression',
    'DenseNet',
    'DenseRegression',
    'DenseClassifier',
]


def LinearRegression(data=None):
    """Linear regression model.

    TODO: docs...

    """
    
    # Use default input if none specified
    if data is None:
        data = Input()

    # A linear regression
    error = ScaleParameter()
    predictions = Dense(data)
    return Normal(predictions, error)



def LogisticRegression(data=None):
    """Logistic regression model.

    TODO: docs...

    """

    # Use default input if none specified
    if data is None:
        data = Input()

    # A logistic regression
    predictions = Dense(data)
    return Bernoulli(predictions)



def DenseNet(data=None, units=[1]):
    """Multiple dense layers in a row.

    DOES NOT INCLUDE AN OBSERVATION DISTRIBUTION!

    TODO: docs...

    """

    # Use default input if none specified
    if data is None:
        y_out = Input()
    else:
        y_out = data

    # Send output of each layer into the following layer
    for unit in units:
        y_out = Dense(y_out, units=unit)

    return y_out



def DenseRegression(data=None, units=[1]):
    """Regression model using a densely-connected multi-layer neural network.
    """
    error = ScaleParameter()
    predictions = DenseNet(data, units=units)
    return Normal(predictions, error)



def DenseClassifier(data=None, units=[1]):
    """Classifier model using a densely-connected multi-layer neural network.
    """
    predictions = DenseNet(data, units=units)
    return Bernoulli(predictions)



def Conv1dRegression(data=None):
    """TODO
    """
    #TODO    
    pass


def Conv1dClassifier(data=None):
    """TODO
    """
    #TODO    
    pass


def Conv2dRegression(data=None):
    """TODO
    """
    #TODO    
    pass


def Conv2dClassifier(data=None):
    """TODO
    """
    #TODO    
    pass


def DenseAutoencoderRegression(data=None):
    """TODO
    """
    #TODO    
    pass


def DenseAutoencoderClassifier(data=None):
    """TODO
    """
    #TODO    
    pass


def Conv1dAutoencoderRegression(data=None):
    """TODO
    """
    #TODO    
    pass


def Conv1dAutoencoderClassifier(data=None):
    """TODO
    """
    #TODO    
    pass


def Conv2dAutoencoderRegression(data=None):
    """TODO
    """
    #TODO    
    pass


def Conv2dAutoencoderClassifier(data=None):
    """TODO
    """
    #TODO    
    pass


#TODO: NeuralMatrixFactorization

#TODO: BayesianCorrelation
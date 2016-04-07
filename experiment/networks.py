#!/usr/bin/env python

"""
Defines the network architecture, hyper-params, optimizer and cost to be used
in the experiements.
"""

from data import VOCAB_SIZE
from neon.initializers import GlorotUniform, Uniform
from neon.layers.container import Sequential
from neon.optimizers import Adagrad
from neon.layers import (
    LSTM,
    Affine,
    LookupTable,
    RecurrentSum,
    GeneralizedCost,
    Dropout,
)
from neon.transforms import (
    Tanh,
    Logistic,
    Softmax,
    CrossEntropyMulti,
)


def get_cost_opt():
    gradient_clip_value = 15.0
    cost = GeneralizedCost(costfunc=CrossEntropyMulti(usebits=True))
    opt = Adagrad(learning_rate=0.01, gradient_clip_value=gradient_clip_value)
    return cost, opt


def get_core_net(embedding_size=128, nout=10):
    """
    Returns a tuple containing the original encoder and decoder networks.
    embedd_size: size of the output of the encoder
    nout: size of the output of the decoder
    path: filepath from which the weights should be loaded
    """
    embedding_dim = 128
    uni = Uniform(low=-0.1/embedding_dim, high=0.1/embedding_dim)
    glorot = GlorotUniform()

    enc = [
        LookupTable(vocab_size=VOCAB_SIZE, embedding_dim=128, init=uni),
        LSTM(embedding_size, glorot, activation=Tanh(),
             gate_activation=Logistic(), reset_cells=True),
        RecurrentSum(),
    ]

    dec = [
        Dropout(keep=0.5),
        Affine(nout, glorot, bias=glorot, activation=Softmax())
    ]

    cost, opt = get_cost_opt()
    return (enc, dec), cost, opt


def get_title_augmentator(embedding_size=128, path=None):
    """
    Returns the network that will be used to augment the network, to handle
    titles.
    embedd_size: size of the embedding
    path: filepath from which to load the model's weights
    """
    embedding_dim = 128
    uni = Uniform(low=-0.1/embedding_dim, high=0.1/embedding_dim)
    glorot = GlorotUniform()

    aug = [
        LookupTable(vocab_size=VOCAB_SIZE, embedding_dim=128, init=uni),
        LSTM(embedding_size, glorot, activation=Tanh(),
             gate_activation=Logistic(), reset_cells=True),
        RecurrentSum(),
    ]
    cost, opt = get_cost_opt()
    return aug, cost, opt

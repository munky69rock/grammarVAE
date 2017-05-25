from __future__ import division

import equation_vae

from matplotlib import pyplot as plt

import numpy as np


# 1. load grammar VAE
grammar_weights = "pretrained/eq_vae_grammar_h200_c234_L10_E50_BN_val.hdf5"
print(grammar_weights)
grammar_model = equation_vae.EquationGrammarModel(grammar_weights,
                                                  latent_rep_size=10)

# 2. let's encode and decode some example equations
eq = ['3+sin(2+x)',
      'x+exp(x/2)',
      '2*x',
      'exp(2/x)']

# z: encoded latent points
# NOTE: this operation returns the mean of the encoding distribution
# if you would like it to sample from that distribution instead
# replace line 62 in equation_vae.py with:
# return self.vae.encoder.predict(one_hot)
z = grammar_model.encode(eq)

# mol: decoded equations
# NOTE: decoding is stochastic so calling this function many
# times for the same latent point will return different answers
# let's plot how well the true functions match the decoded functions
domain = np.linspace(-10, 10)
for i, s in enumerate(grammar_model.decode(z)):
    print(s)
    plt.figure()
    f = eval("lambda x: "+eq[i])
    f_hat = eval("lambda x: "+s)
    plt.plot(domain, f(domain))
    ty = type(f_hat(domain))
    if (ty is not np.ndarray):
        plt.plot(domain, np.repeat(f_hat(domain), len(domain)))
    else:
        plt.plot(domain, f_hat(domain))
    plt.legend(["function", "reconstruction"])
    plt.title('%15s -> %s' % (eq[i], s))


# 3. the character VAE (https://github.com/maxhodak/keras-molecules)
# works the same way, let's load it
char_weights = "pretrained/eq_vae_str_h200_c234_L10_E50_BN_val.hdf5"
print(char_weights)
char_model = equation_vae.EquationCharacterModel(char_weights,
                                                 latent_rep_size=10)


# 4. encode and decode
domain = np.linspace(-10, 10)
for i, s in enumerate(char_model.decode(z)):
    print(s)
    plt.figure()
    f = eval("lambda x: "+eq[i])
    try:
        f_hat = eval("lambda x: "+s)
        f_hat(domain)
    except:
        print("This equation doesn't decode:")
        print(s)
        continue
    plt.plot(domain, f(domain))
    ty = type(f_hat(domain))
    if (ty is not np.ndarray):
        plt.plot(domain, np.repeat(f_hat(domain), len(domain)))
    else:
        plt.plot(domain, f_hat(domain))
    plt.legend(["function", "reconstruction"])
    plt.title('%15s -> %s' % (eq[i], s))

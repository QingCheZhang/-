
from keras.models import load_model
from pkg_resources import resource_filename
from utils2 import one_hot_encode
import numpy as np

input_sequence = ''
context = 2000
x = one_hot_encode('N'*(context//2) + input_sequence + 'N'*(context//2))[None, :]
model_1 = load_model('./Models/SpliceAI2000_g1.keras')
y1 = model_1.predict(x)
acceptor_prob = y1[0, :, 1]
donor_prob = y1[0, :, 2]

import numpy as np
result = donor_prob[donor_prob > 0.3]
indices = np.where(donor_prob > 0.3)
result1 = acceptor_prob[acceptor_prob > 0.3]
indices1 = np.where(acceptor_prob > 0.3)
print('acceptor_scores:', result1)
print('acceptor_sites:', indices1)
print('donor_scores:', result)
print('donor_sites:', indices)

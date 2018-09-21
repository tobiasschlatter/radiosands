import numpy as np
import keras.backend as K
import librosa as lbr
from keras.models import model_from_yaml

GENRES = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
WINDOW_SIZE = 2048
WINDOW_STRIDE = WINDOW_SIZE // 2
N_MELS = 128
MEL_KWARGS = {
    'n_fft': WINDOW_SIZE,
    'hop_length': WINDOW_STRIDE,
    'n_mels': N_MELS
}

def get_layer_output_function(model, layer_name):
    input = model.get_layer('input').input
    output = model.get_layer(layer_name).output
    f = K.function([input, K.learning_phase()], output)
    return lambda x: f([x, 0])  # learning_phase = 0 means test


def load_track(filename, enforce_shape=None):
    new_input, sample_rate = lbr.load(filename, mono=True)
    features = lbr.feature.melspectrogram(new_input, **MEL_KWARGS).T

    if enforce_shape is not None:
        if features.shape[0] < enforce_shape[0]:
            delta_shape = (enforce_shape[0] - features.shape[0],
                           enforce_shape[1])
            features = np.append(features, np.zeros(delta_shape), axis=0)
        elif features.shape[0] > enforce_shape[0]:
            features = features[: enforce_shape[0], :]

    features[features == 0] = 1e-6
    return (np.log(features), float(new_input.shape[0]) / sample_rate)


class GenreRecognizer():
    def __init__(self, model_path, weights_path):
        with open(model_path, 'r') as f:
            model = model_from_yaml(f.read())
        model.load_weights(weights_path)
        self.pred_fun = get_layer_output_function(model, 'output_realtime')
        print 'Loaded model.'

    def recognize(self, track_path):
        print 'Loading song', track_path
        (features, duration) = load_track(track_path)
        features = np.reshape(features, (1,) + features.shape)
        return (self.pred_fun(features), duration)


def most_common(lst):
    return max(set(lst), key=lst.count)


def get_genre_distribution_over_time(predictions, duration):
    '''
    Turns the matrix of predictions given by a model into a dict mapping
    time in the song to a music genre distribution.
        '''
    predictions = np.reshape(predictions, predictions.shape[1:])
    n_steps = predictions.shape[0]
    delta_t = duration / n_steps

    def get_genre_distribution(step):
        return {genre_name: float(predictions[step, genre_index])
                for (genre_index, genre_name) in enumerate(GENRES)}

    return [((step + 1) * delta_t, get_genre_distribution(step))
            for step in xrange(n_steps)]

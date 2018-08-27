from keras.callbacks import Callback, ModelCheckpoint

class LoadBestWeights(ModelCheckpoint):
    """Saves best weights to filepath via ModelCheckpoint (whose kwargs it accepts)
       and automatically loads them at the end of training"""
    def __init__(self, filepath, **kwargs):
        super().__init__(filepath, save_best_only=True, **kwargs)

    def on_train_end(self, logs):
        print('loading best weights')
        self.model.load_weights(self.filepath)

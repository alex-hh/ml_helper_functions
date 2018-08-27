from keras.callbacks import Callback, ModelCheckpoint

class LoadBestWeights(ModelCheckpoint):
    """Saves best weights to filepath via ModelCheckpoint (whose kwargs it accepts)
       and automatically loads them at the end of training"""
    def __init__(self, filepath, **kwargs):
        super().__init__(filepath, save_best_only=True, **kwargs)

    def on_train_end(self, logs):
        print('loading best weights')
        self.model.load_weights(self.filepath)

# Idea of these is to allow resuming callbacks in mid trainig (if run needs to be split into multiple parts -
# because re-initializing standard callbacks will destroy information about best performance so far that is required
class ResumeReduceLR(ReduceLROnPlateau):

    def __init__(self, best_loss=None, best_epoch=None,
                 last_epoch=None, **kwargs):
        super().__init__(**kwargs)
        self.best_loss = best_loss
        # TODO the assumption here isn't right; 
        # it's not last_epoch - best_epoch but
        # last_epoch - last_lr_reduction
        # to fix maybe save lr with the csv logger.
        self.best_epoch = best_epoch
        self.last_epoch = last_epoch

    def on_train_begin(self, logs=None):
        super().on_train_begin(logs)
        if self.best_loss:
            self.best = self.best_loss
            self.wait = self.last_epoch - self.best_epoch

class ResumeModelCheckpoint(ModelCheckpoint):

    def __init__(self, best_loss=None, **kwargs):
        super().__init__(**kwargs)
        if best_loss:
            self.best = best_loss

class ResumeEarlyStopping(EarlyStopping):

    def __init__(self, best_loss=None, best_epoch=None, last_epoch=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.best_loss = best_loss
        self.best_epoch = best_epoch
        self.last_epoch = last_epoch

    def on_train_begin(self, logs=None):
        super().on_train_begin(logs)
        if self.best_loss:
            self.best = self.best_loss
            self.wait = self.last_epoch - self.best_epoch
            if self.wait >= self.patience:
                print('{} epochs since best performance, stopping training'.format(self.wait))
                self.stopped_epoch = self.last_epoch
                self.model.stop_training = True
    def on_epoch_end(self, epoch, logs=None):
        super().on_epoch_end(epoch, logs)
        print('{} epochs without val loss improvement'.format(self.wait))

import cv2


class StatModel(object):

    def load(self, fn):
        self.model.load(fn)

    def save(self, fn):
        self.model.save(fn)


class SVM(StatModel):

    def __init__(self):
        self.model = cv2.SVM()

    def train(self, samples, labels):
        params = dict(kernel_type=cv2.SVM_RBF, svm_type=cv2.SVM_C_SVC)
        self.model.train_auto(samples, labels, None, None, params)

    def predict(self, X):
        return self.model.predict(X, True)

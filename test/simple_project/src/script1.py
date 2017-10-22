import decu
import logging
import numpy as np

class Script(decu.Script):
    @decu.experiment(data_param='d')
    def exp(self, d, p, p2):
        logging.info('Working on {}'.format(Script.exp.run))
        return np.power(d, p) + p2

    def main(self):
        self.exp(np.arange(5), p=4, p2=10)

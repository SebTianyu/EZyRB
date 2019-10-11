class ReducedOrderModel(object):

    def __init__(self, database, reduction, approximation):

        self.database = database
        self.reduction = reduction
        self.approximation = approximation

        
    def fit(self):
        
        self.approximation.fit(
            self.database.parameters,
            self.reduction.reduce(self.database.snapshots.T))

        return self

    def predict(self, mu):
        print(self.approximation.predict(mu))
        return self.database.scaler_snapshots.inverse(
                self.reduction.expand(self.approximation.predict(mu)))

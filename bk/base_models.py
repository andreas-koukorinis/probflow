"""Abstract model classes.

TODO: more info...

"""

from abc import ABC, abstractmethod
from scipy import stats

class BaseModel(ABC):
    """Abstract model class (just used as implementation base)

    TODO: More info...

    """


    def __init__(self, *args, **kwargs):
        """Construct model.

        TODO: docs. Mention that actually building the tf graph is
        delayed until build() or fit() is called.
        """
        self.args = args
        self.kwargs = kwargs
        self.built_model = None
        self.is_fit = False


    @abstractmethod
    def build(self, data):
        """Build model.
        
        Inheriting class must define this method by building the 
        model for that class.  Should set `self.built_model` to a
        TensorFlow Probability distribution, using the inputs to 
        the constructor which are stored in `self.args` and 
        `self.kwargs`.
        """
        pass


    def fit(self, x, y, batch_size=128, epochs=100, 
            optimizer='adam', learning_rate=None, metrics=None):
        """Fit model.

        TODO: Docs...

        """
        # TODO: build the model
        # TODO: set up the data for fitting
        # TODO: fit the model
        self.is_fit = True
        pass


    def ensure_is_fit(self):
        """Raises a RuntimeError if model has not yet been fit."""
        if not self.is_fit:
            raise RuntimeError('model must first be fit') 


    def posterior(self, params=None):
        """Draw samples from parameter posteriors.

        TODO: Docs...

        """

        # Check model has been fit
        self.ensure_is_fit()

        #TODO
        pass

        
    def predictive_distribution(self, x, num_samples=100):
        """Draw samples from the model given x.

        TODO: Docs...

        Returns array of shape (x.shape[0],y.shape[1],num_samples)

        """

        # Check model has been fit
        self.ensure_is_fit()

        #TODO
        pass


    def predict(self, x, method='mean', prc=50, num_samples=100):
        """Predict dependent variable for samples in x.

        TODO: explain how predictions are generated from the
        posterior predictive distributions, etc.

        Parameters
        ----------
        x : np.ndarray
            Input array of independent variable values.  Should be
            of shape (N,D), where N is the number of samples and D
            is the number of dimensions of the independent variable.
        method : {'mean', 'median', 'mode', 'min', 'max', 'prc'}
            Method to use to convert the predictive distribution 
            into a single prediction.
            * 'mean': Use the mean of the predictive distribution
              (the default).
            * 'median': Use the median of the predictive dist.
            * 'mode': Use the mode of the predictive dist.
            * 'min': Use the minimum of the predictive dist.
            * 'max': Use the maximum of the predictive dist.
            * 'prc': Use a specified percentile of the predictive 
              dist.  The `prc` arg sets what percentile value to 
              use.
        prc : float
            Percentile of the predictive distribution to use as 
            a prediction when ``method=='prc'`. Between 0 and 100
            inclusive.
        num_samples : int
            Number of samples to draw from the posterior predictive
            distribution.

        Returns
        -------
        predictions : np.ndarray
            Predicted y-value for each sample in `x`.  Will be of
            size (N,D_out), where N is the number of samples (equal
            to `x.shape[0]`) and D_out is the number of output 
            dimensions (equal to `y.shape[1]`).

        See Also
        --------
        predictive_distribution : used to generate the distribution
            which is used to make the prediction.

        Notes
        -----
        TODO: Docs...

        Examples
        --------
        TODO: Docs...

        """

        # Check model has been fit
        self.ensure_is_fit()

        # Compute predictive distribution
        pred_dist = self.predictive_distribution(x, num_samples)

        #TODO: should really do straight in tf, 
        # not tf->numpy->sample

        # Compute prediction based on the predictive distribution
        if method=='mean':
            return np.mean(pred_dist, axis=2)
        elif method=='median':
            return np.median(pred_dist, axis=2)
        elif method=='mode':
            return stats.mode(pred_dist, axis=2)
        elif method=='min':
            return np.amin(pred_dist, axis=2)
        elif method=='max':
            return np.amax(pred_dist, axis=2)
        elif method=='prc':
            return np.percentile(pred_dist, prc, axis=2)
        else:
            raise ValueError('method '+str(method)+' is invalid')


    def _plot_by(self, x, data, bins=100, what='mean'):
        """Compute and plot mean of data as a function of x.

        x should be (N,1) or (N,2)
        what can be mean, median, or count
            if mean, plot the mean of data for each bin
            etc

        returns px, py
        px is (Nbins,1) or (Nbins*Nbins,2) w/ bin centers
        py is mean of data in each bin (or count or whatevs)

        plots 2d plot w/ colormap where goes to black w/ less datapoints
        """
        #TODO


    def prob(self, x, y):
        """Compute the probability of observations `y` given `x` and
        the model.

        TODO: docs...
        returns vector of probs w/ shape (x.shape[0],)

        """

        # Check model has been fit
        self.ensure_is_fit()

        # TODO: make dataset/iterator/feed_dict of x and y

        # Compute probability of y given x
        # TODO
        #tf_prob = self.built_model.prob()
        # with tf.Session() as sess:
        #   prob = sess.run(tf_prob, feed_dict=???)


    def prob_by(self, x, y, x_by, bins=100, plot=True):
        """Plot the probability of observations `y` given `x` and
        the model as a function of specified independent variables.

        TODO: docs...

        """
        
        # Compute the model probability
        probs = self.prob(x, y)

        # TODO: alternatively, x_by should be able to be any array_like
        # as long as it's same size as x.shape[0]

        # Plot probability as a fn of x_by cols of x
        px, py = self._plot_by(x[:,x_by], probs, 
                               bins=bins, plot=plot)

        return px, py


    def log_prob(self, x, y):
        """Compute the log probability of observations `y` given 
        `x` and the model.

        TODO: docs...

        """

        # Check model has been fit
        self.ensure_is_fit()

        # TODO: evaluate log_prob w/ tf like above


    def log_prob_by(self, x, y, x_by, bins=100):
        """Plot the log probability of observations `y` given `x` 
        and the model as a function of specified independent 
        variables
        """
        # TODO: same idea as prob_by, above


    def cdf(self, x, y):
        """Compute the cumulative probability of observations `y` 
        given `x` and the model.

        TODO: docs...

        """

        # Check model has been fit
        self.ensure_is_fit()

        # TODO: evaluate cdf w/ tf like above


    def cdf_by(self, x, y, x_by, bins=100):
        """Plot the cumulative probability of observations `y` 
        given `x` and the model as a function of specified 
        independent variables
        """
        # TODO: same idea as prob_by, above


    def log_cdf(self, x, y):
        """Compute the log cumulative probability of observations 
        `y` given `x` and the model.

        TODO: docs...

        """

        # Check model has been fit
        self.ensure_is_fit()

        # TODO: evaluate log_cdf w/ tf like above


    def log_cdf_by(self, x, y, x_by, bins=100):
        """Plot the log cumulative probability of observations `y` 
        given `x` and the model as a function of specified 
        independent variables
        """
        # TODO: same idea as prob_by, above



class ContinuousModel(BaseModel):
    """Abstract continuous model class (used as implementation base)

    TODO: More info...

    """

    def predict(self, x, method='mean', prc=50, num_samples=100):
        """Predict dependent variable for samples in x.

        TODO: Docs...

        """
        return BaseModel.predict(self, x, method=method, prc=prc,
                                 num_samples=num_samples)


    def predictive_prc(self, x, y):
        """Compute the percentile of each observation along the 
        posterior predictive distribution.

        TODO: Docs...

        """

        # Check model has been fit
        self.ensure_is_fit()

        #TODO
        pass

        
    def pred_dist_covered(self, x, y, prc):
        """Compute whether each observation was covered by the 
        inner `prc` percentile of the posterior predictive 
        distribution.

        TODO: Docs...

        """

        # Check model has been fit
        self.ensure_is_fit()

        #TODO
        pass

        
    def pred_dist_coverage(self, x, y, prc):
        """Compute the coverage of the inner `prc` percentile of the
        posterior predictive distribution.

        TODO: Docs...
        returns a scalar (from 0 to 100)

        """

        # Check model has been fit
        self.ensure_is_fit()

        #TODO
        pass


    def coverage_by(self, x, y, x_by, prc, bins=100, plot=True):
        """Compute and plot the coverage of the inner `prc` 
        percentile of the posterior predictive distribution as a 
        function of specified independent variables.

        TODO: Docs...
        x_by should be int or length-2 list of ints which specifies what column of x to plot by
        returns x and coverage matrix
        """

        # Compute whether each sample was covered by the interval
        covered = self.pred_dist_covered(x, y, prc)

        # TODO: alternatively, x_by should be able to be any array_like
        # as long as it's same size as x.shape[0]
        
        # Plot probability as a fn of x_by cols of x
        px, py = self._plot_by(x[:,x_by], covered, 
                               bins=bins, plot=plot)

        return px, py


    def calibration_curve(self, x, y, split_by=None, bins=10):
        """Plot and return calibration curve.

        Plots and returns the calibration curve (the percentile of 
        the posterior predictive distribution on the x-axis, and the
        percent of samples which actually fall into that range on
        the y-axis).

        Parameters
        ----------
        x : np.ndarray
            Input array of independent variable values.  Should be
            of shape (N,D), where N is the number of samples and D
            is the number of dimensions of the independent variable.
        y : np.ndarray
            Array of dependent variable values.  Should be of shape
            (N,D_out), where N is the number of samples (equal to
            `x.shape[0]) and D_out is the number of dimensions of
            the dependent variable.
        split_by : int
            Draw the calibration curve independently for datapoints
            with each unique value in `x[:,split_by]` (a categorical
            column).
        bins : int or vector_like
            Bins used to compute the curve.  If an integer, will use
            `bins` evenly-spaced bins from 0 to 1.  If a vector,
            `bins` is the vector of bin edges.          

        Returns
        -------
        cx : np.ndarray
            Vector of percentiles (the middle of each percentile
            bin).  Length is determined by `bins`.
        cy : np.ndarray
            Vector of percentages of samples which fell within each
            percentile bin of the posterior predictive distribution.

        See Also
        --------
        predictive_distribution : used to generate the posterior
            predictive distribution.

        Notes
        -----
        TODO: Docs...

        Examples
        --------
        TODO: Docs...

        """

        # Check model has been fit
        self.ensure_is_fit()

        #TODO
        pass



class CategoricalModel(BaseModel):
    """Abstract categorical model class (used as implementation base)

    TODO: More info...

    """

    def predict(self, x, method='mode', prc=50, num_samples=100):
        """Predict dependent variable for samples in x.

        TODO: Docs...

        """
        return BaseModel.predict(self, x, method=method, prc=prc, 
                                 num_samples=num_samples)


    def calibration_curve(self, x, y, split_by=None, bins=10):
        """Plot and return calibration curve.

        Plots and returns the calibration curve (estimated 
        probability of outcome vs the true probability of that 
        outcome).

        Parameters
        ----------
        x: 
        y: 
        split_by: draw curve independently for datapoints with 
            each unique value in this categorical column number.
        bins: bins used to compute the curve.  An integer to
            specify the number of evenly-spaced bins from 0 to 
            1, or a list or array-like to specify the bin edges.

        #TODO: split by continuous cols as well? Then will need to define bins or edges too

        TODO: Docs...

        """

        # Check model has been fit
        self.ensure_is_fit()

        #TODO
        pass


    # TODO: are there categorical equivalents of predictive_prc, 
    # pred_dist_covered, pred_dist_coverage, and coverage_by?
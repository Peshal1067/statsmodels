import numpy as np
np.random.seed(5)
from numpy.testing import dec

import statsmodels.api as sm
from statsmodels.graphics.gofplots import qqplot, qqline, ProbPlot
from scipy import stats


try:
    import matplotlib.pyplot as plt
    import matplotlib
    if matplotlib.__version__ < '1':
        raise
    have_matplotlib = True
except:
    have_matplotlib = False


class _base_probplot:
    def base_setup(self):
        self.fig, self.ax = plt.subplots()
        self.other_array = np.random.normal(size=self.prbplt.data.shape)
        self.other_prbplot = sm.ProbPlot(self.other_array)

    def teardown():
        plt.close('all')

    def test_qqplot(self):
        self.fig = self.prbplt.qqplot(ax=self.ax, line=self.line)

    def test_ppplot(self):
        self.fig = self.prbplt.ppplot(ax=self.ax, line=self.line)

    def test_probplot(self):
        self.fig = self.prbplt.probplot(ax=self.ax, line=self.line)

    def test_qqplot_other_array(self):
        self.fig = self.prbplt.qqplot(ax=self.ax, line=self.line,
                                        other=self.other_array)
    def test_ppplot_other_array(self):
        self.fig = self.prbplt.ppplot(ax=self.ax, line=self.line,
                                        other=self.other_array)
    def test_probplot_other_array(self):
        self.fig = self.prbplt.probplot(ax=self.ax, line=self.line,
                                        other=self.other_array)

    def test_qqplot_other_prbplt(self):
        self.fig = self.prbplt.qqplot(ax=self.ax, line=self.line,
                                        other=self.other_prbplot)
    def test_ppplot_other_prbplt(self):
        self.fig = self.prbplt.ppplot(ax=self.ax, line=self.line,
                                        other=self.other_prbplot)
    def test_probplot_other_prbplt(self):
        self.fig = self.prbplt.probplot(ax=self.ax, line=self.line,
                                        other=self.other_prbplot)

    def test_qqplot_custom_labels(self):
        self.fig = self.prbplt.qqplot(ax=self.ax, line=self.line,
                                      xlabel='Custom X-Label',
                                      ylabel='Custom Y-Label')

    def test_ppplot_custom_labels(self):
        self.fig = self.prbplt.ppplot(ax=self.ax, line=self.line,
                                      xlabel='Custom X-Label',
                                      ylabel='Custom Y-Label')

    def test_probplot_custom_labels(self):
        self.fig = self.prbplt.probplot(ax=self.ax, line=self.line,
                                        xlabel='Custom X-Label',
                                        ylabel='Custom Y-Label')

    def test_qqplot_pltkwargs(self):
        self.fig = self.prbplt.qqplot(ax=self.ax, line=self.line,
                                      marker='d', 
                                      markerfacecolor='cornflowerblue',
                                      markeredgecolor='white',
                                      alpha=0.5)

    def test_ppplot_pltkwargs(self):
        self.fig = self.prbplt.ppplot(ax=self.ax, line=self.line,
                                      marker='d', 
                                      markerfacecolor='cornflowerblue',
                                      markeredgecolor='white',
                                      alpha=0.5)

    def test_probplot_pltkwargs(self):
        self.fig = self.prbplt.probplot(ax=self.ax, line=self.line,
                                        marker='d', 
                                        markerfacecolor='cornflowerblue',
                                        markeredgecolor='white',
                                        alpha=0.5)


@dec.skipif(not have_matplotlib)
class test_ProbPlot_Longely(_base_probplot):
    def setup(self):
        self.data = sm.datasets.longley.load()
        self.data.exog = sm.add_constant(data.exog, prepend=False)
        self.mod_fit = sm.OLS(data.endog, data.exog).fit()
        self.prbplt = sm.ProbPlot(mod_fit.resid, stats.t, distargs=(4,))
        self.line = 'r'
        self.base_setup()


@dec.skipif(not have_matplotlib)
class test_ProbPlot_RandomNormal_Minimal(_base_probplot):
    def setup(self):
        self.data = np.random.normal(loc=8.25, scale=3.25, size=37)
        self.prbplt = sm.ProbPlot(self.data)
        self.line = None
        self.base_setup()


@dec.skipif(not have_matplotlib)
class test_ProbPlot_RandomNormal_WithFit(_base_probplot):
    def setup(self):
        self.data = np.random.normal(loc=8.25, scale=3.25, size=37)
        self.prbplt = sm.ProbPlot(self.data, fit=True)
        self.line = 'q'
        self.base_setup()


@dec.skipif(not have_matplotlib)
class test_ProbPlot_RandomNormal_LocScale(_base_probplot):
    def setup(self):
        self.data = np.random.normal(loc=8.25, scale=3.25, size=37)
        self.prbplt = sm.ProbPlot(self.data, loc=8.25, scale=3.25)
        self.line = '45'
        self.base_setup()


class test_top_level:
    def setup(self):
        self.data = sm.datasets.longley.load()
        self.data.exog = sm.add_constant(data.exog, prepend=False)
        self.mod_fit = sm.OLS(data.endog, data.exog).fit()
        self.res = mod_fit.resid
        self.prbplt = sm.ProbPlot(mod_fit.resid, stats.t, distargs=(4,))
        self.other_array = np.random.normal(size=self.prbplt.data.shape)
        self.other_prbplot = sm.ProbPlot(self.other_array)

    def teardown(self):
        plt.close('all')

    @dec.skipif(not have_matplotlib)
    def test_qqplot():
        fig = sm.qqplot(self.res, line='r')

    @dec.skipif(not have_matplotlib)
    def test_qqplot_2samples_ProbPlotObjects():
        # also tests all values for line
        for line in ['r', 'q', '45', 's']:
            # test with `ProbPlot` instances
            fig = sm.qqplot_2samples(self.prbplt, self.other_prbplot, 
                                     line=line)

    @dec.skipif(not have_matplotlib)
    def test_qqplot_2samples_arrays():
        # also tests all values for line
        for line in ['r', 'q', '45', 's']:
            # test with arrays
            fig = sm.qqplot_2samples(x=self.res, self.other_array, line=line)



# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

from audioop import mul
from pydoc import cli
import pylab
import matplotlib.pyplot as plt
import re
import numpy

# cities in our weather data
CITIES = [
    'BOSTON','SEATTLE', 'SAN DIEGO', 'PHILADELPHIA', 'PHOENIX',
    'LAS VEGAS', 'CHARLOTTE', 'DALLAS', 'BALTIMORE',
    'SAN JUAN', 'LOS ANGELES','MIAMI', 'NEW ORLEANS',
    'ALBUQUERQUE', 'PORTLAND', 'SAN FRANCISCO','TAMPA',
    'NEW YORK','DETROIT', 'ST LOUIS', 'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return numpy.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = numpy.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    result = []
    for i in degs:
        fit = numpy.polyfit(x, y, i)
        result.append(numpy.array(fit))

    return result


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    estimateError = ((estimated - y)**2).sum()
    meanOfMeasured = y.sum()/len(y)
    variability = ((y - meanOfMeasured)**2).sum()
    return 1 - estimateError/variability

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        p = numpy.poly1d(model)   # setting degree of polynomial
        r2 = r_squared(y, p(x))
        plt.figure()
        plt.plot(x, y, 'bo', label='Data Points')
        plt.plot(x, p(x), 'r-', label='Model')
        plt.legend(loc='best')
        if len(model) == 2:
            plt.title(f'Degree of fit: {len(model) - 1} \n R2: {r2} \n Ratio of SE: {se_over_slope(x, y, p(x), model)}.')
        else:
            plt.title(f'Degree of fit: {len(model) - 1} \n R2: {r2}')
        plt.xlabel('Year')
        plt.ylabel('Temperature in Celsius')
        plt.show()

    
def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    temps = []
    for i in years:
        temp_for_year = 0.0
        for j in multi_cities:
            temp_for_year += (numpy.mean(climate.get_yearly_temp(j, i)))
        temp_for_year = temp_for_year / len(multi_cities)
        temps.append(temp_for_year)

    return numpy.array(temps)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    out = []
    for i in range(1, len(y) + 1):
        if i < window_length:
            out.append(numpy.average(y[:i]))
        else:
            out.append(numpy.average(y[i-window_length:i]))
    return numpy.array(out)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return numpy.sqrt(((y - estimated)**2).sum()/ len(y))

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    stdDev = []
    for i in years:
        temp_for_year = []
        for j in multi_cities:
           temp_for_year.append(climate.get_yearly_temp(j, i))
        temp_for_year = numpy.array(temp_for_year)
        daily_mean = temp_for_year.mean(axis = 0)
        stdDev.append(numpy.std(daily_mean))

    return numpy.array(stdDev)

    
def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        p = numpy.poly1d(model)   # setting degree of polynomial
        rmse_value = rmse(y, p(x))
        plt.figure()
        plt.plot(x, y, 'bo', label='Data Points')
        plt.plot(x, p(x), 'r-', label='Model')
        plt.legend(loc='best')
        plt.title(f'Degree of fit: {len(model) - 1} \n RMSE: {rmse_value}')
        plt.xlabel('Year')
        plt.ylabel('Temperature in Celsius')
        plt.show()
if __name__ == '__main__':

    data_file = Climate('data.csv')
    temperature_data = []
    for year in TRAINING_INTERVAL:
        temperature = data_file.get_daily_temp('NEW YORK', 1, 10, year)
        temperature_data.append(temperature)
    year_data = numpy.array(TRAINING_INTERVAL)
    temperature_data = numpy.array(temperature_data)
    temp_model = generate_models(year_data, temperature_data, [1])
    evaluate_models_on_training(year_data, temperature_data, temp_model)

    # Problem 4.2 - Annual Temperature, in order to run the code, please uncomment section below.

    data_file = Climate('data.csv')
    avg_temperature_data = []
    for year in TRAINING_INTERVAL:
        avg_temp = data_file.get_yearly_temp('NEW YORK', year).mean()
        avg_temperature_data.append(avg_temp)
    year_data = numpy.array(TRAINING_INTERVAL)
    avg_temperature_data = numpy.array(avg_temperature_data)
    avg_temp_model = generate_models(year_data, avg_temperature_data, [1])
    evaluate_models_on_training(year_data, avg_temperature_data, avg_temp_model)

    # Part B
    # in order to run the code, please uncomment section below.

    data_file = Climate('data.csv')
    all_cities_avg = gen_cities_avg(data_file, CITIES, TRAINING_INTERVAL)
    year_data = numpy.array(TRAINING_INTERVAL)
    all_cities_model = generate_models(year_data, all_cities_avg, [1])
    evaluate_models_on_training(year_data, all_cities_avg, all_cities_model)

    # Part C
    # in order to run the code, please uncomment section below.

    data_file = Climate('data.csv')
    all_cities_avg = gen_cities_avg(data_file, CITIES, TRAINING_INTERVAL)
    year_data = numpy.array(TRAINING_INTERVAL)
    moved_average_cities = moving_average(all_cities_avg, 5)
    all_cities_model = generate_models(year_data, moved_average_cities, [1])
    evaluate_models_on_training(year_data, moved_average_cities, all_cities_model)

    # Part D2
    # in order to run the code, please uncomment section below.

    data_file = Climate('data.csv')
    all_cities_avg = gen_cities_avg(data_file, CITIES, TRAINING_INTERVAL)
    year_data = numpy.array(TRAINING_INTERVAL)
    all_cities_model = generate_models(year_data, all_cities_avg, [1])
    year_data_testing = numpy.array(TESTING_INTERVAL)
    all_cities_avg_testing = gen_cities_avg(data_file, CITIES, TESTING_INTERVAL)
    evaluate_models_on_testing(year_data_testing, all_cities_avg_testing, all_cities_model)

    # Part D2.I
    # in order to run the code, please uncomment section below.

    data_file = Climate('data.csv')
    all_cities_avg = gen_cities_avg(data_file, CITIES, TRAINING_INTERVAL)
    year_data = numpy.array(TRAINING_INTERVAL)
    moved_average_cities = moving_average(all_cities_avg, 5)
    all_cities_models = generate_models(year_data, moved_average_cities, [1, 2, 20])
    evaluate_models_on_training(year_data, moved_average_cities, all_cities_models)

    # Part D2.II
    # in order to run the code, please uncomment section below and section above
    # keep (evaluate_models_in_training) commented.

    year_data_testing = pylab.array(TESTING_INTERVAL)
    all_cities_avg_testing = gen_cities_avg(data_file, CITIES, TESTING_INTERVAL)
    moved_average_cities_testing = moving_average(all_cities_avg_testing, 5)
    evaluate_models_on_testing(year_data_testing, moved_average_cities_testing, all_cities_models)

    # Part E
    # in order to run the code, please uncomment section below.

    data_file = Climate('data.csv')
    deviation = gen_std_devs(data_file, CITIES, TRAINING_INTERVAL)
    year_data = pylab.array(TRAINING_INTERVAL)
    deviation_moved = moving_average(deviation, 5)
    deviation_models = generate_models(year_data, deviation_moved, [1])
    evaluate_models_on_training(year_data, deviation_moved, deviation_models)

    
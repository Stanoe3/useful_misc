"""Provides non-default type hinting"""
from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Lagrange:
    """A dataclass to represent the Lagrange Functions
    """

    def __init__(self, x_array: Iterable[float], denominator: float, numerator: float = 1) -> None:
        self.denominator = denominator
        self.x_array = x_array
        self.numerator = numerator

    def __repr__(self) -> None:
        ret_str = f"Denominator: {self.denominator},\nNumerator: {self.numerator},"
        ret_str += f"\nx values: {self.x_array}"
        return ret_str

    def evaluate(self, eval_point: float) -> float:
        """Evaluates the Lagrange function at a point

        Args:
            eval_point (float): The point at which to evaluate

        Returns:
            float: The result of the evaluation
        """
        product = self.numerator
        for x_val in self.x_array:
            product *= (eval_point - x_val)
        product /= self.denominator
        return product


def horner(polynomial: Iterable[float], x_val: float) -> float:
    """Calculates the value of a polynomial at a specific input

    Args:
        polynomial(Iterable[float]): An iterable of coefficients, where polynomial[i] = a_i * x ^ i
        x(float): The value of x at which to compute the polynomial

    Returns:
        float: The value of the polynomial at the specified point
    """

    result = 0
    for coeff in polynomial:
        result = result * x_val + coeff
    return result


def get_lagranges(x_arr: Iterable[float]) -> Iterable[Lagrange]:
    """Generates the lagrange base functions based on the list given

    Args:
        x_arr(Iterable[float]): A set of values from which to generate base functions

    Returns:
        Iterable[Iterable[float]]: A list of Iterables, the 0... n-1 values are the 'a'
        in (x-a) pairs, the final value is the denominator
    """

    lagrange_list = []
    for i, _ in enumerate(x_arr):
        new_arr = []
        denom_product = 1
        for j, _ in enumerate(x_arr):
            if j != i:
                new_arr.append(x_arr[j])
                denom_product *= x_arr[i] - x_arr[j]
        lagrange_list.append(Lagrange(new_arr, denom_product))
    return lagrange_list


def generate_numerator(lagrange_list: Iterable[Lagrange]) -> str:
    """Generates the numerator string for a Lagrange object

    Args:
        lagrange_list (Iterable[Lagrange]): A list of Lagrange objects representing an interpolated
        polynomial

    Returns:
        str: A string representation of the numerator
    """
    numerator = ""
    for i, lagrange in enumerate(lagrange_list):
        for x_val in lagrange.x_array:
            numerator += f"(x-{x_val})"
        if i != len(lagrange_list)-1:
            numerator += "   "
    return numerator


def generate_seperator(lagrange_list: Iterable[Lagrange], numerator: str) -> str:
    """Generates the seperator (i.e. division line)

    Args:
        lagrange_list (Iterable[Lagrange]): A list of Lagrange objects representing an interpolated
        polynomial
        numerator (str): The string numerator for the Lagrange objects

    Returns:
        str: A string representation of the seperator
    """
    sep = ""
    items = numerator.strip().split(" ")
    terms = [x for x in items if x != ""]
    for i, term in enumerate(terms):
        sep += "_" * len(term)
        if i != len(lagrange_list) - 1:
            sep += " + "
    return sep


def generate_denominator(lagrange_list: Iterable[Lagrange], seperator: str) -> str:
    """Generates the denominator string for a Lagrange object

    Args:
        lagrange_list (Iterable[Lagrange]): A list of Lagrange objects representing an interpolated
        polynomial

    Returns:
        str: A string representation of the denominator
    """
    denominator = ""
    seperator = seperator.strip().split(" + ")
    for i, lagrange in enumerate(lagrange_list):
        denominator += str(lagrange.denominator).center(len(seperator[i]), " ")
        if i != len(lagrange_list) - 1:
            denominator += "   "
    return denominator


def display_lagranges_to_terminal(lagrange_list: Iterable[Lagrange]) -> None:
    """Displays the Lagrange objects in one polynomial to the terminal

    Args:
        lagrange_list (Iterable[Lagrange]): The Lagrange objects to be printed
    """
    numerator = generate_numerator(lagrange_list)
    seperator = generate_seperator(lagrange_list, numerator)
    denominator = generate_denominator(lagrange_list, seperator)
    print(numerator)
    print(seperator)
    print(denominator)


def interpol_poly(x_arr: Iterable[float], y_arr: Iterable[float]) -> List[Lagrange]:
    """Finds and displays the interpolating polynomial of a set of
    data points to a smallest possible degree

    Args:
        x_arr(Iterable[float]): The set of given data points that represent x_i
        y_arr(Iterable[float]): The set of given data points that represent y_i

    Returns:
        Iterable[Iterable[float]]: A list of Iterables, the 0th value is a numerator coefficient,
        the 1... n-1 values are the 'a' in (x-a) pairs, the final value is the denominator
    """
    lagranges = get_lagranges(x_arr)
    for i, lagrange in enumerate(lagranges):
        lagrange.numerator = y_arr[i]
    return lagranges


def convert_poly_to_str(coeffs: Iterable[float]) -> str:
    """Converts a list of coefficients representing a polynomial into readable polynomial equation

    Args:
        coeffs(Iterable[float]): The list of coefficients that describe the polynomial

    Returns:
        str: The converted readable output
    """
    poly_str = ""
    for i, coeff in enumerate(coeffs):
        if i == len(coeffs) - 1:
            return poly_str + f" {coeff}"
        if coeff < 0:
            poly_str = poly_str[:-1]
        poly_str += f"{coeff}x^{len(coeffs)-(i+1)} +"


def evaluate_lagranges(lagrange_list: Iterable[Lagrange], eval_point: float) -> float:
    """Evaluates a list of Lagrange functions at a given point

    Args:
        lagrange_list (Iterable[Lagrange]): A list of Lagrange functions for which to evaluate
        eval_point (float): The point at which to evaluate

    Returns:
        float: The value of the evaluation
    """
    poly_sum = 0
    for lagrange in lagrange_list:
        poly_sum += lagrange.evaluate(eval_point)
    return poly_sum


if __name__ == "__main__":
    lagrange_set = interpol_poly([0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11], [
                                 69, 50, 61, 51, 67, 65, 79, 74, 77, 78, 78])
    # display_lagranges_to_terminal(lagrange_set)
    print(evaluate_lagranges(lagrange_set, 4))

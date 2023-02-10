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
        denom_product = 1
        for j, _ in enumerate(x_arr):
            if j != i:
                denom_product *= x_arr[i] - x_arr[j]
        lagrange_list.append(Lagrange(x_arr, denom_product))
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
    display_lagranges_to_terminal(lagranges)


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


if __name__ == "__main__":
    print(convert_poly_to_str((4, 3, -2, 10)))
    interpol_poly([-1, 0, 1], [-10, 1, 10])

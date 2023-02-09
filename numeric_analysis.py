from typing import Iterable, List


def horner(polynomial: Iterable[float], x: float) -> float:
    """Calculates the value of a polynomial at a specific input

    Args:
        polynomial (Iterable[float]): An iterable of coefficients, where polynomial[i] = a_i * x^i
        x (float): The value of x at which to compute the polynomial

    Returns:
        float: The value of the polynomial at the specified point
    """

    result = 0
    for coeff in polynomial:
        result = result * x + coeff
    return result


def get_lagranges(x_arr: Iterable[float]) -> Iterable[Iterable[float]]:
    """Generates the lagrange base functions based on the list given

    Args:
        x_arr (Iterable[float]): A set of values from which to generate base functions

    Returns:
        Iterable[Iterable[float]]: A list of Iterables, the 0... n-1 values are the 'a'  in (x-a) pairs, the final value is the denominator
    """
    lagrange_list = []
    for i in range(len(x_arr)):
        denom_product = 1
        new_lagrange = []
        for j in range(len(x_arr)):
            if j != i:
                new_lagrange.append(x_arr[j])
                denom_product *= x_arr[i] - x_arr[j]
        new_lagrange.append(denom_product)
        lagrange_list.append(new_lagrange)
    return lagrange_list


def interpol_poly(x_arr: Iterable[float], y_arr: Iterable[float]) -> List[float]:
    """Finds the interpolating polynomial of a set of data points to a smallest possible degree

    Args:
        x_arr (Iterable[float]): The set of given data points that represent x_i
        y_arr (Iterable[float]): The set of given data points that represent y_i

    Returns:
        List[float]: The coefficients of the polynomial
    """
    lagranges = get_lagranges(x_arr)


def convert_poly_to_str(coeffs: Iterable[float]) -> str:
    """Converts a list of coefficients representing a polynomial into readable polynomial equation

    Args:
        coeffs (Iterable[float]): The list of coefficients that describe the polynomial

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
    print(f"Horner's algorithm test for 3x^2 -2x + 10 at x=3. Should return 31")
    print(horner((3, -2, 10), 3))
    print(convert_poly_to_str((4, 3, -2, 10)))

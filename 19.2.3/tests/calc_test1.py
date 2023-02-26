import pytest
from app.calculator import Calculator


class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply_calculate_correctly(self):
        assert self.calc.multiply(self, 11, 21) == 231

    def test_division_calculate_correctly(self):
        assert self.calc.division(self, 108, 12) == 9

    def test_subtraction_calculate_correctly(self):
        assert self.calc.subtraction(self, 56, 42) == 14

    def test_adding_calculate_correctly(self):
        assert self.calc.adding(self, 21, 142) == 163

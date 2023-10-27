"""
Test for the Exercise 2, Task 2
"""

import unittest

#import required modules for importing the code to be tested
import pathlib
import importlib
import sys

here = pathlib.Path(__file__).parent
exercise_dir = here.parent

#Import the exercise 2 python file to test the task 2 module
exercise2_spec=importlib.util.spec_from_file_location("exercise2",exercise_dir / "exercises_02.py")
exercise2 = importlib.util.module_from_spec(exercise2_spec)
exercise2_spec.loader.exec_module(exercise2)
sys.modules["exercise2"] = exercise2




class task_2_test(unittest.TestCase):
    """
    Test Class for assignement 2, task 2
    """


    def run_test(self,test_inpt):
        """
        wrapper for calling the function that is to be evaluated (-> easier to adjust if the testfunction name is different)
        """
        return exercise2.task2(*test_inpt)



    def test_normal_cases(self):
        """
        tests farily normal cases without any 'controversial' inputs
        """
        inpt = ["a","7","gh","fs","f","dlr","1","0"]
        response_expected = (['7', '1', '0'], ['a', '7', 'f', '1', '0'])
        response = self.run_test(inpt)
        self.assertTupleEqual(response,response_expected)


    def test_floats(self):
        """
        test how the program handles floats
        Expects: Floats are recognized as numbers
        """
        inpt = ["a","5.6","6.2323","7","2.0"]
        response_expected = (['5.6', '6.2323', '7', '2.0'], ['a', '7'])
        response = self.run_test(inpt)
        self.assertTupleEqual(response,response_expected)


    def test_nan(self):
        """
        test how the program handles the string 'nan' which is interprted as a number by python
        Expects: 'nan' is not recognized as a number
        """
        inpt = ["nan"]
        response_expected = ([], [])
        response = self.run_test(inpt)
        self.assertTupleEqual(response,response_expected)


    def test_infinity(self):
        """
        test how the program handles the string 'infinity' and similar inputs
        Expects: Infinity is recognized as a number
        """
        inpt = ["infinity","-infinity","+infinity"]
        response_expected = (['infinity', '-infinity', '+infinity'], [])
        response = self.run_test(inpt)
        self.assertTupleEqual(response,response_expected)


    def test_complex(self):
        """
        test how the program handles complex numbers
        Expects: Complex numbers are recognized as numbers
        """
        inpt = ["5+3j","1+1j","0+1j","1+0j","j"]
        response_expected = (['5+3j', '1+1j', '0+1j', '1+0j', 'j'], ['j'])
        response = self.run_test(inpt)
        self.assertTupleEqual(response, response_expected)



if __name__ == '__main__':
    unittest.main()



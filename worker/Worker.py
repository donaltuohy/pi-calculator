import flask, requests, os, sys, subprocess
import logging
import math
from decimal import Decimal, getcontext
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)

class Worker:
    # Initialise Worker class
    def __init__(self):
        logging.info("Initialising worker.")

    # Take in parameters for calculating pi
    # param 1: start - Number to start calculating pi at
    # param 2: end - Number to stop calculating pi at
    # param 3: precision - The precision to work with when calculating pi. Ensures we keep precision to get n decimals places.
    # return type: Decimal type of the summed result from start to end
    def pi(self, start, end, precision):
        logging.info("Recieved work - calculating from " + str(start) + " to " + str(end) + ".")
        getcontext().prec = precision
        sum = Decimal(0)
        for k in range(start, end):
            sum = sum + self.pi_formula_decimals(k, precision)
        result = sum 
        return result

    # https://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula
    def pi_formula_decimals(self, k, precision):
        getcontext().prec = precision

        dec_k = Decimal(k)
        dec_1 = Decimal(1)
        dec_2 = Decimal(2)
        dec_4 = Decimal(4)
        dec_5 = Decimal(5)
        dec_6 = Decimal(6)
        dec_8 = Decimal(8)
        dec_16 = Decimal(16)
    
        result = (dec_1)/(dec_16**dec_k) * ( (Decimal(4)/((Decimal(8) * dec_k)+ dec_1) ) - (dec_2 / ((dec_8*dec_k) + dec_4)) - ( dec_1 / ((dec_8 * dec_k) + dec_5) ) - ( dec_1 / ((dec_8 * dec_k) + dec_6)))
        return result

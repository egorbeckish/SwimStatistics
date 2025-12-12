import streamlit as st
import pdfplumber
import os
import regex
import base64
import json
import pandas as pd
import re
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import datetime
import iso3166
import psutil
import time
import uuid
from dotenv import load_dotenv, dotenv_values
import sys
from ast import literal_eval
from geonamescache import GeonamesCache


# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import *


STATISTICS = dotenv_values(r".env\.env.statistics")
EVENT = STATISTICS["EVENT"]
STAGE = STATISTICS["STAGE"]


PAGES = dotenv_values(r".env\.env.pages")
TYPE_CONTEST = PAGES["TYPE_CONTEST"].split("\n")
WORLD_CUP_STAGE = PAGES["WORLD_CUP_STAGE"].split("\n")
SEX = PAGES["SEX"].split("\n")
POOL_DISTANCE = PAGES["POOL_DISTANCE"].split("\n")
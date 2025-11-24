from lib import (
	os,
	psutil
)


psutil.Process(os.getpid()).terminate()
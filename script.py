import sys, subprocess

app = sys.argv[1]
arguments = sys.argv[1:]
if app=="power":
	cmd = ["RScript", "power_matrix.R"] + arguments
elif app=="samples":
	cmd = ["RScript", "sample_size_matrix.R"] + arguments
else:
	print(app+" is an unknown application. exiting")
	exit()
print(cmd)
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

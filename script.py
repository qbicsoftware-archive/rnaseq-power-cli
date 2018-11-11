import sys, subprocess

USAGE = '''USAGE
power estimation:

power [# genes] [# diff. expr. genes] [min. detectable fold change] [dispersion] [FDR]

sample size estimation:

samples [# genes] [# diff expr. genes] [dispersion] [FDR] [power/sensitivity]'''

if len(sys.argv) < 2:
	print USAGE
	exit()
app = sys.argv[1]
arguments = sys.argv[2:]
if app=="power":
	cmd = ["Rscript", "/power_matrix.R"] + arguments
elif app=="samples":
	cmd = ["Rscript", "/sample_size_matrix.R"] + arguments
else:
	print(USAGE)
	exit()

print(cmd)
#process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE)
	p.wait()
	(result, error) = p.communicate()
except subprocess.CalledProcessError as e:
	sys.stderr.write("common::run_command() : [ERROR]: output = %s, error code = %s\n" % (e.output, e.returncode))

print(result)

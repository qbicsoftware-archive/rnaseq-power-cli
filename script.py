import sys, subprocess

USAGE = '''USAGE

[user] [projectcode] [app = power/samples] [app parameters...]

power estimation parameters:
power [# genes] [# diff. expr. genes] [min. detectable fold change] [dispersion] [FDR]

sample size estimation:
samples [# genes] [# diff expr. genes] [dispersion] [FDR] [power/sensitivity]'''

if len(sys.argv) < 4:
	print(USAGE)
	exit()
user = sys.argv[1]
project = sys.argv[2]
app = sys.argv[3]
arguments = sys.argv[4:]

if app=="power":
	filename = "power.pdf"
	cmd = ["Rscript", "/power_matrix.R"] + arguments
elif app=="samples":
	filename = "sample_size.pdf"
	cmd = ["Rscript", "/sample_size_matrix.R"] + arguments
else:
	print(USAGE)
	exit()
cmd += filename
print(cmd)

try:
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE)
	p.wait()
	(result, error) = p.communicate()
except subprocess.CalledProcessError as e:
	sys.stderr.write("common::run_command() : [ERROR]: output = %s, error code = %s\n" % (e.output, e.returncode))

print(result)
print(error)

cmd = ["attachi", "-u", user, "-t", "Information", project, filename, "RnaSeqSampleSize analysis for "+project]
print(cmd)

try:
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE)
	p.wait()
	(result, error) = p.communicate()
except subprocess.CalledProcessError as e:
	sys.stderr.write("common::run_command() : [ERROR]: output = %s, error code = %s\n" % (e.output, e.returncode))

print(result)
print(error)

upload_folder = "unkonw"

cmd = ["tar", "-c", upload_folder, "|", "dync", "-n", upload_folder+".tar", "-k", "untar:True", "data.qbic.uni-tuebingen.de"]
print(cmd)

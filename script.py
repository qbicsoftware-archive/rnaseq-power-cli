import sys, subprocess, os

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
cmd += [filename]
print(cmd)

try:
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE)
	p.wait()
	(result, error) = p.communicate()
except subprocess.CalledProcessError as e:
	sys.stderr.write("common::run_command() : [ERROR]: output = %s, error code = %s\n" % (e.output, e.returncode))

print(result)
print(error)

#create results folder
results_path = "results"
os.mkdir(results_path)

cmd = ["attachi", "-o", results_path, "-u", user, "-t", "Information", project, filename, "RnaSeqSampleSize analysis for "+project]
print(cmd)

try:
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE)
	p.wait()
	(result, error) = p.communicate()
except subprocess.CalledProcessError as e:
	sys.stderr.write("common::run_command() : [ERROR]: output = %s, error code = %s\n" % (e.output, e.returncode))

print(result)
print(error)

listed_dir = os.listdir(results_path)
if len(listed_dir) == 1:
	upload_folder = listed_dir[0]
else:
	sys.exit("folder contains "+len(listed_dir)+" files. existing.")

os.rename(os.path.join(results_path, upload_folder), upload_folder)

tar_cmd = ["tar", "-c", upload_folder]
dync_cmd = ["dync", "-n", upload_folder+".tar", "-k", "untar:True", "data.local"]

try:
	tar = subprocess.Popen(tar_cmd, stdout=subprocess.PIPE)
	p = subprocess.Popen(dync_cmd, stdout = subprocess.PIPE, stdin=tar.stdout)
	p.wait()
	(result, error) = p.communicate()
except subprocess.CalledProcessError as e:
	sys.stderr.write("common::run_command() : [ERROR]: output = %s, error code = %s\n" % (e.output, e.returncode))

print(result)
print(error)

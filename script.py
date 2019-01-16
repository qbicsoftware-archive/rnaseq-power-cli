import sys, subprocess, os

USAGE = '''USAGE

[user] [sampleCode] [app = power/samples] [app parameters...]

power estimation parameters:
power none [# genes] [# diff. expr. genes] [replicates (sample size)] [FDR] [dispersion]
OR
power tcga [# genes] [# diff. expr. genes] [replicates (sample size)] [FDR] [TCGA name]

sample size estimation:
samples none [# genes] [# diff expr. genes] [FDR] [dispersion] [avg counts/gene]
OR
samples tcga [# genes] [# diff expr. genes] [FDR] [TCGA name]'''

if len(sys.argv) < 4:
	print(USAGE)
	exit()
user = sys.argv[1]
sampleCode = sys.argv[2]
project = sampleCode[0:5]
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
if not os.path.exists(results_path):
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

old_results_path = os.path.join(results_path, upload_folder)
attachCode = project+"000"

cmd = ["sed", "-i", "s/"+attachCode+"/"+sampleCode+"/g", os.path.join(old_results_path, "metadata.txt")]
print(cmd)

try:
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE)
	p.wait()
	(result, error) = p.communicate()
except subprocess.CalledProcessError as e:
	sys.stderr.write("common::run_command() : [ERROR]: output = %s, error code = %s\n" % (e.output, e.returncode))

print(result)
print(error)
os.rename(old_results_path, upload_folder)

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

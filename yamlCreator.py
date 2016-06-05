import yaml
import sys
import os
from shutil import copyfile

global arguments
arguments = {}

def yamlCreator():
	#Valid yaml creation
	data = dict(
		version = "0.9.0",
		arguments = [dict(
				fastq = [dict(
						id = arguments["id"],
						type = (arguments["type"]),
						value = "/bbx/input/reads.fq.gz"
				)]
			)]
		)
	yamlFile = open(arguments["yaml"], "w")

	with yamlFile as f:
		yaml.dump(data, f, default_flow_style=False)

def folderPath(folder):
	#If startswith / indicating that the complete path is already given
	if folder.startswith('/'):
		if folder.endswith('/'):
			return folder
		else:
			return folder.rsplit('/', 1)[0]
	#Otherwise append the path of the script to the current folder location of the script
	return os.path.dirname(os.path.realpath(__file__)) + folder

def assemblerSelection():
	#This can be a file...
	assemblers = ["bioboxes/velvet",
				  "bioboxes/megahit",
				  "bioboxes/sga",
				  "bioboxes/idba",
				  "bioboxes/minia",
				  "bioboxes/ray",
				  "bioboxes/sparse",
				  "bioboxes/soap"]

	if "--assembler" not in sys.argv:
		print "Use --assembler to select your assembler"
		print "Currently supported assemblers:"
		print '\n'.join(assemblers)
		sys.exit()

	selection = sys.argv[sys.argv.index("--assembler")+1]

	if selection not in assemblers and "--force" not in sys.argv:
		print "Currently supported assemblers:"
		print '\n'.join(assemblers)
		print "To force your public docker use --force"
		sys.exit()

	return selection

def runDocker():
	assembler = assemblerSelection()
	output = open("docker.sh", "w")

	#INPUT needs to be the folder...
	bash = '''
docker run \
--volume="'''+arguments["fastq"]+''':/bbx/input/reads.fq.gz:ro" \
--volume="'''+arguments["yaml"]+''':/bbx/input/biobox.yaml:ro" \
--volume="'''+arguments["output"]+''':/bbx/output/:rw" \
--rm \
'''+assembler+''' \
default
'''
	output.write(bash)
	output.close()
	command = "bash docker.sh"
	print(command)
	os.system(command)

def test():
	arguments["fastq"] = os.path.abspath("myReadFolder/reads.fq.gz")
	arguments["output"] = os.path.abspath("test")
	arguments["yaml"] = arguments["output"]+"/biobox.yaml"
	#IF output folder does not exist yet...
	if not os.path.isdir(arguments["output"]):
		os.mkdir(arguments["output"])
	arguments["id"] = "TEST"
	arguments["fasta"] = "myTestResult.fa"


	assemblers = ["bioboxes/velvet",
				  "bioboxes/megahit",
				  "bioboxes/sga",
				  "bioboxes/idba",
				  "bioboxes/minia",
				  "bioboxes/ray",
				  "bioboxes/sparse",
				  "bioboxes/soap"]

	for assembler in assemblers:
		arguments["assembler"] = assembler
		arguments["type"] = "single"
		assemblerSelection()
		yamlCreator()
		runDocker()

	for assembler in assemblers:
		arguments["assembler"] = assembler
		arguments["type"] = "paired"
		assemblerSelection()
		yamlCreator()
		runDocker()


if __name__ == '__main__':
	if "--test" in sys.argv:
		print("PERFORMING TESTS")
		test()

	if "--fastq" not in sys.argv:
		print("--fastq FASTQ required")
		sys.exit()
	else:
		#Get complete path of input file
		arguments["fastq"] = os.path.abspath(sys.argv[sys.argv.index("--fastq")+1])

	if "--output" not in sys.argv:
		print("--output folder required")
		sys.exit()
	else:
		#Get complete path of output folder
		arguments["output"] = os.path.abspath(sys.argv[sys.argv.index("--output")+1])
		arguments["yaml"] = arguments["output"]+"/biobox.yaml"
		#IF output folder does not exist yet...
		if not os.path.isdir(arguments["output"]):
			os.mkdir(arguments["output"])

	if "--type" not in sys.argv:
		print("--type paired/single required")
		sys.exit()
	else:
		arguments["type"] = sys.argv[sys.argv.index("--type")+1]

	if "--id" not in sys.argv:
		print("--id required")
		sys.exit()
	else:
		arguments["id"] = sys.argv[sys.argv.index("--id")+1]

	assemblerSelection()
	yamlCreator()
	runDocker()

	#If the output fasta file is required to be moved to somewhere else -ofasta is used
	if "--fasta" in sys.argv:
		arguments["fasta"] = sys.argv[sys.argv.index("--fasta")+1]
		import shutil
		shutil.move(arguments["output"]+"/contig.fa", arguments["fasta"])



import yaml
import sys
import os
from shutil import copyfile

global arguments
arguments = {}

def yamlCreator():
	# This creates a YAML file without - and is not valid for biobox
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

	#Should we create a symbolic link to FASTQ on different location?

	#INPUT needs to be the folder...
	bash = '''
docker run \
--volume="'''+arguments["fastq"]+''':/bbx/input/reads.fq.gz:ro" \
--volume="'''+arguments["yaml"]+''':/bbx/input/biobox.yaml:ro" \
--volume="'''+arguments["tmp"]+''':/bbx/output/:rw" \
--rm \
'''+assembler+''' \
default
'''
	output.write(bash)
	output.close()
	command = "bash docker.sh"
	print(command)
	os.system(command)

if __name__ == '__main__':
	if "--fastq" not in sys.argv:
		print("--fastq FASTQ required")
		sys.exit()
	else:
		#Get complete path of input file
		arguments["fastq"] = os.path.abspath(sys.argv[sys.argv.index("--fastq")+1])

	if "--tmp" not in sys.argv:
		print("--tmp folder required")
		sys.exit()
	else:
		#Get complete path of output folder
		arguments["tmp"] = os.path.abspath(sys.argv[sys.argv.index("--tmp")+1])
		arguments["yaml"] = arguments["tmp"]+"/biobox.yaml"
		#IF output folder does not exist yet...
		if not os.path.isdir(arguments["tmp"]):
			os.mkdir(arguments["tmp"])

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

	if "--output" not in sys.argv:
		print("--output folder required")
		sys.exit()
	else:
		#Get complete path of output folder
		arguments["output"] = os.path.abspath(sys.argv[sys.argv.index("--output")+1])
		#IF output folder does not exist yet... create it
		if not os.path.isdir(arguments["output"]):
			os.mkdir(arguments["output"])

	# if "--assembler" not in sys.argv:
	# else:
		# arguments["assembler"] = sys.argv[sys.argv.index("--assembler")+1]

	assemblerSelection()
	yamlCreator()
	runDocker()


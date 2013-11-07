import sys, argparse
import os, datetime
import re
import math
from array import *

def generateReport(benchmark_result):
	anlyze_result = []

	#clearing to get pure json snippet
	benchmark_result = benchmark_result.replace("  [java] "," ")
	strbegin = "<json>"
	strend = "</json>"
	output  = re.compile('<json>(.*?)</json>', re.DOTALL |  re.IGNORECASE).findall(benchmark_result)
	jsonsnippet = str(output[0])
	jsonsnippet = jsonsnippet.replace("\n","")
	jsonsnippet = jsonsnippet.replace("\"","")
	
	# get 	THROUGHPUT
	output  = re.compile('TXNPERMILLI: (.*?),', re.DOTALL |  re.IGNORECASE).findall(jsonsnippet)
	THROUGHPUT = str(output[0])
	basic = " " + THROUGHPUT
	anlyze_result.append(THROUGHPUT)
	# get 	AVG LATENCY
	output  = re.compile('TOTALAVGLATENCY: (.*?),', re.DOTALL |  re.IGNORECASE).findall(jsonsnippet)
	AVGLATENCY = str(output[0])
	basic += " " + AVGLATENCY
	anlyze_result.append(AVGLATENCY)
	
	# total transaction count
	output  = re.compile('TXNTOTALCOUNT: (.*?),', re.DOTALL |  re.IGNORECASE).findall(jsonsnippet)
	TXNTOTALCOUNT = str(output[0])
	basic += " " + TXNTOTALCOUNT
	anlyze_result.append(TXNTOTALCOUNT)
	# DTXNTOTALCOUNT
	output  = re.compile('DTXNTOTALCOUNT: (.*?),', re.DOTALL |  re.IGNORECASE).findall(jsonsnippet)
	DTXNTOTALCOUNT = str(output[0])
	basic += " " + DTXNTOTALCOUNT
	anlyze_result.append(DTXNTOTALCOUNT)
	# SPECEXECTOTALCOUNT
	output  = re.compile('SPECEXECTOTALCOUNT: (.*?),', re.DOTALL |  re.IGNORECASE).findall(jsonsnippet)
	SPECEXECTOTALCOUNT = str(output[0])
	basic += " " + SPECEXECTOTALCOUNT
	anlyze_result.append(SPECEXECTOTALCOUNT)

	# TXNMINPERSECOND 
	output  = re.compile('TXNMINPERSECOND: (.*?),', re.DOTALL |  re.IGNORECASE).findall(jsonsnippet)
	TXNMINPERSECOND = str(output[0])
	basic += " " + TXNMINPERSECOND
	anlyze_result.append(TXNMINPERSECOND)
	# TXNMAXPERSECOND
	output  = re.compile('TXNMAXPERSECOND: (.*?),', re.DOTALL |  re.IGNORECASE).findall(jsonsnippet)
	TXNMAXPERSECOND = str(output[0])
	basic += " " + TXNMAXPERSECOND
	anlyze_result.append(TXNMAXPERSECOND)
	# STDDEVTXNPERSECOND
	output  = re.compile('STDDEVTXNPERSECOND: (.*?),', re.DOTALL |  re.IGNORECASE).findall(jsonsnippet)
	STDDEVTXNPERSECOND = str(output[0])
	basic += " " + STDDEVTXNPERSECOND
	anlyze_result.append(STDDEVTXNPERSECOND)
	
	# TOTALMINLATENCY
	output  = re.compile('TOTALMINLATENCY: (.*?),', re.DOTALL |  re.IGNORECASE).findall(jsonsnippet)
	TOTALMINLATENCY = str(output[0])
	basic += " " + TOTALMINLATENCY
	anlyze_result.append(TOTALMINLATENCY)
	# TOTALMAXLATENCY
	output  = re.compile('TOTALMAXLATENCY: (.*?),', re.DOTALL |  re.IGNORECASE).findall(jsonsnippet)
	TOTALMAXLATENCY = str(output[0])
	basic += " " + TOTALMAXLATENCY
	anlyze_result.append(TOTALMAXLATENCY)
	# TOTALSTDEVLATENCY
	output  = re.compile('TOTALSTDEVLATENCY: (.*?),', re.DOTALL |  re.IGNORECASE).findall(jsonsnippet)
	TOTALSTDEVLATENCY = str(output[0])
	basic += " " + TOTALSTDEVLATENCY
	anlyze_result.append(TOTALSTDEVLATENCY)
	
	print basic
	#analyze the content
	#print "This benchmark result is :", jsonsnippet
	return anlyze_result

def getReportFromList(list):
	report = ""
	for item in list:
		report += " " + item
	return report

# get mean, std for array
def getMeanAndStd(a):
	n = len(a)
	mean = sum(a) / n
	std = math.sqrt(sum((x-mean)**2 for x in a) / n) 
	return mean, std

# get the args from command line
# set default values for parameters needed by script
timestamp = datetime.datetime.now()
t = timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second
defaultoutput = 'experiment' + '_'.join(str(i) for i in t)+ '.txt'
# get paramets from command line input

parser = argparse.ArgumentParser(description='This is a benchmark auto-run script, made by hawk.')
parser.add_argument('-p','--project', help='Benchmark name', default='tpcc')
parser.add_argument('-o','--output', help='output file', default=defaultoutput)
parser.add_argument('--stop', help='indicate if the threshold will be used to stop expeiments', action='store_true')
parser.add_argument('--tmin', help='min - thread per host', type=int, default=10)
parser.add_argument('--tmax', help='max - thread per host', type=int, default=10)
parser.add_argument('--rmin', help='min - txnrate', type=int, default=1000)
parser.add_argument('--rmax', help='max - txnrate', type=int, default=1000)
parser.add_argument('--lmin', help='min - log timeout', type=int, default=10)
parser.add_argument('--lmax', help='max - log timeout', type=int, default=10)


args = parser.parse_args()

projectname = args.project
resultfile  = args.output
stopflag    = args.stop
tmin	    = args.tmin
tmax	    = args.tmax
rmin	    = args.rmin
rmax	    = args.rmax
lmin	    = args.lmin
lmax	    = args.lmax

print projectname, resultfile, stopflag, tmin, tmax, rmin, rmax, lmin, lmax

#exit(0)

file = open(resultfile, "w")

#print fields
fields = "client.threads_per_host " + "client.txnrate " + "site.commandlog_timeout " + "THROUGHPUT(txn/s) " + "AVGLATENCY(ms) " + "TotalTXN "
fields += "Distributed " + "SpecExec " + "THMIN " + "THMAX " + "THSTDDEV " + "LAMIN " + "LAMAX " + "LASTDDEV"
file.write(fields + "\n")

#  make command line to execute benchmark with the indicated configuration
client_threads_per_host 	= tmin;
client_txnrate			= rmin
site_commandlog_timeout		= lmin

number_need_to_determine = 5
stdev_threshold = 0.03

resultlist =  list()

while client_threads_per_host <= tmax:
	while client_txnrate <= rmax:
		while site_commandlog_timeout <= lmax:
			str_antcmd 			= "ant hstore-benchmark"
			str_project 			= " -Dproject=" + projectname
			str_client_blocking 		= " -Dclient.output_results_json=" + "true"
			str_client_output_results_json 	= " -Dclient.bloking=" + "true"
			str_client_threads_per_host 	= " -Dclient.threads_per_host=" + "{0:d}".format(client_threads_per_host)
			str_client_txnrate		= " -Dclient.txnrate=" + "{0:d}".format(client_txnrate)
			str_site_commandlog_timeout = " -Dsite.commandlog_timeout=" + "{0:d}".format(site_commandlog_timeout)
		
			basic = "{0:d}".format(client_threads_per_host) + " " + "{0:d}".format(client_txnrate) + " " +  "{0:d}".format(site_commandlog_timeout)
		
			runcmd = str_antcmd + str_project + str_client_blocking + str_client_output_results_json + str_client_threads_per_host + str_client_txnrate + str_site_commandlog_timeout
		
			print "running benchmark with following configuration:"
			print runcmd
	
			# run the benchmark by calling the runcmd with os
			f = os.popen( runcmd )
		
			# get the benchmark running result, and print it on screen
			result = f.read()
			#print "This benchmark result is :", result
		        singlereport = generateReport(result)
			basic += getReportFromList(singlereport)
			file.write(basic+"\n")
	
			resultlist.append(singlereport)
		
			site_commandlog_timeout += 10
	
			if stopflag == False:
				continue
			
			#determien if we should stop experiment, because the stdev/average is so little
			if len(resultlist) >= number_need_to_determine:
				latestresult = resultlist[len(resultlist)-number_need_to_determine::1]
	        	        throughputarray = array('f')
				latencyarray = array('f')	
				for item in latestresult:
					print item
					throughputarray.append(float(item[0]))
					latencyarray.append(float(item[1]))
				#if ((scipy.std(throughputarray)/scipy.mean(throughputarray)) < stdev_threshold) and ((scipy.std(latencyarray)/scipy.mean(latencyarray)) < stdev_threshold) :i
				thmeanvalue, thstdvalue = getMeanAndStd(throughputarray)
				lameanvalue, lastdvalue = getMeanAndStd(latencyarray)
				if (thstdvalue/thmeanvalue) < stdev_threshold and (lastdvalue/lameanvalue) < stdev_threshold :
					break;
		client_txnrate += 100
	client_threads_per_host += 5;	

file.close()

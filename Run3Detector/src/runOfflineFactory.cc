#include "./interface/OfflineFactory.h"
#include <algorithm>

char* getCmdOption(char ** begin, char ** end, const std::string & option)
{
    char ** itr = std::find(begin, end, option);
    if (itr != end && ++itr != end)
    {
        return *itr;
    }
    return 0;
}

bool cmdOptionExists(char** begin, char** end, const std::string& option)
{
    return std::find(begin, end, option) != end;
}

int main(int argc, char **argv){

    // string helpString = "Usage: ./script.exe -i <inputFileName> -o <outputFileName> [-a APPEND] [--drs] [-c CONFIGS] [-h] \n\nOPTIONS:\
	// 		 \n-i input file\n-o output file \n-c configuration files \
    //                      (comma sep list of files with NO spaces) or json as string \n \
    //                      -a text to appendToTag \n --drs runs with DRS input \n -h show this message \";

    //Read input and output files (necessary arguments)
    bool versionMode = cmdOptionExists(argv, argv + argc, "-v");
    if (versionMode){
        OfflineFactory offlineFactory = OfflineFactory("","",false,-1,-1);
        std::cout << offlineFactory.getVersion() << std::endl;
        return 0;
    }
    char * inputFilenameChar = getCmdOption(argv, argv + argc, "-i");
    char * outputFilenameChar = getCmdOption(argv, argv + argc, "-o");
    char * offlineDir = getCmdOption(argv,argv+argc,"--offlineDir");
    char * appendToTag = getCmdOption(argv,argv+argc,"-a");
    char * mergedTriggerFile = getCmdOption(argv, argv + argc, "-m");
    bool isDRSdata = cmdOptionExists(argv, argv + argc, "--drs");
    if (isDRSdata) std::cout << "Assuming DRS input" << std::endl;
    //char * DRS_num = getCmdOption(argv, argv + argc, "-DRS_num");
    //char * numChanDRS = getCmdOption(argv, argv + argc, "-nDRSchan");
    int runNumber = -1;
    int fileNumber = -1;
    if (cmdOptionExists(argv, argv + argc, "-r")) runNumber = atoi(getCmdOption(argv, argv + argc, "-r"));
    if (cmdOptionExists(argv, argv + argc, "-f")) fileNumber = atoi(getCmdOption(argv, argv + argc, "-f"));
    if (!inputFilenameChar || !outputFilenameChar || cmdOptionExists(argv, argv+argc, "-h"))
    {
	std::cout << "Need input and output file" << std::endl;
	return 0;
    }
    bool displayMode = false;
    std::vector<int> eventsToDisplay;
    if (cmdOptionExists(argv, argv + argc, "--display")){
	displayMode = true;
	char * eventsToDisplayChar = getCmdOption(argv, argv + argc, "--display"); 
	stringstream ss(eventsToDisplayChar);
	while (ss.good()){
	    string substr;
	    getline(ss, substr,',');
	    eventsToDisplay.push_back(stoi(substr));
	}
    }

    std::cout << "Running in standard mode with:\nInput file: " << inputFilenameChar << "\nOutput file: " << outputFilenameChar << std::endl;
    OfflineFactory offlineFactory = OfflineFactory(inputFilenameChar,outputFilenameChar,appendToTag,isDRSdata,runNumber,fileNumber);

    //Read configuration files
    char * configChar = getCmdOption(argv, argv + argc, "-c");
    if (configChar){
	string config = configChar;
	if (config.find("{") != std::string::npos) offlineFactory.loadJsonConfig(config);
	else if (config.find(",") == std::string::npos) offlineFactory.loadJsonConfig(config);
	else{
	    stringstream ss(config);
	    while (ss.good()) {
		string substr;
		getline(ss, substr, ',');
		offlineFactory.loadJsonConfig(substr);
	    }
	}
    std::cout << "Configuration: " << configChar << std::endl;
    }
    // OfflineFactory offlineFactory = OfflineFactory("/home/milliqan/data_2022/testing_07_12_22/MilliQan_Cd109Shell.root","testOutput.root");
    // offlineFactory.loadJsonConfig("/home/milliqan/milliqanOffline/offlineProduction/configuration/chanMaps/testMap.json");
    // offlineFactory.loadJsonConfig("/home/milliqan/milliqanOffline/offlineProduction/configuration/pulseFinding/pulseFindingTest.json");
    // offlineFactory.loadJsonConfig("/home/milliqan/milliqanOffline/offlineProduction/configuration/calibrations/testCalibration.json");
    offlineFactory.setFriendFile(mergedTriggerFile);
    if (displayMode) {
	if (isDRSdata){
	    offlineFactory.processDisplays(eventsToDisplay,TString(offlineDir)+"/displaysDRS/");
	}
	else{
	    offlineFactory.processDisplays(eventsToDisplay,TString(offlineDir)+"/displays/");
	}
    }
    else offlineFactory.process();
    return 0;
}


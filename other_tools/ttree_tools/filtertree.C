#include <string>
#include <iostream>
#include <dirent.h> // for traversing a directory
#include <chrono> // for timing
#include "TChain.h"
using std::string;
using std::cout;
using std::endl;

// PARAMETERS
string treename = "twoprongNtuplizer/fTree2";
string path = "/cms/chiarito/eos/twoprong/prelim/Nov5/qcd2015/"; // must end with '/'

// forward declare helper functions
void ProcessDirectory(std::string directory);
void ProcessFile(std::string file);
void ProcessEntity(struct dirent* entity);

// globals
TChain * chain = new TChain(treename.c_str());

void filtertree()
{
  // make a chain with all rootfiles in a directory
  cout << "Running on " << path << endl;
  ProcessDirectory("");

  TFile * newfile = new TFile("filtered_tree.root", "RECREATE");
  newfile->cd();

  chrono::high_resolution_clock::time_point time_1 = chrono::high_resolution_clock::now();
  TTree * newtree = chain->CopyTree("nIDPhotons>0");
  chrono::high_resolution_clock::time_point time_2 = chrono::high_resolution_clock::now();

  auto run_time = chrono::duration_cast<chrono::seconds>( time_2 - time_1 ).count();
  cout << "CopyTree() took " << run_time << " seconds" << endl;

  cout << "original tree " << chain->GetEntries() << " entires" << endl;
  cout << "new tree      " << newtree->GetEntries() << " entires" << endl;

  newtree->Write();
  newfile->Close();
}

// helper function definitions
void ProcessDirectory(std::string directory)
{
    std::string dirToOpen = path + directory;
    auto dir = opendir(dirToOpen.c_str());
    path = dirToOpen + "/";
    if(NULL == dir) {
        std::cout << "could not open directory: " << dirToOpen.c_str() << std::endl;
        return;
    }
    auto entity = readdir(dir);
    while(entity != NULL) {
        ProcessEntity(entity);
        entity = readdir(dir);
    }
    path.resize(path.length() - 1 - directory.length());
    closedir(dir);
}

void ProcessEntity(struct dirent* entity)
{
    if(entity->d_type == DT_DIR) {
        if(entity->d_name[0] == '.') return;
        ProcessDirectory(std::string(entity->d_name));
        return;
    }
    if(entity->d_type == DT_REG) {
        ProcessFile(std::string(entity->d_name));
        return;
    }
}

void ProcessFile(std::string file)
{
    if (file.find(".root") != std::string::npos) {
      std::cout << "Found rootfile     : " << (file) << std::endl;
        chain->Add((path + file).c_str());
    }
}

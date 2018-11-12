void copytree() {
   // oldfile will be _file0
   TTree *oldtree = (TTree*)_file0->Get("diphotonAnalyzer/fTree2");
   oldtree->SetBranchStatus("*",1);
   oldtree->SetBranchStatus("TwoProng_CHpos_dxy",0);

   std::string name = _file0->GetName();
   std::size_t pos = name.find(".root"); 
   name = name.substr(0,pos);
   name = name + "_small.root";
   cout << name << endl;
   TFile *newfile = new TFile(name.c_str(),"recreate");
   cout << "cloning..." << endl;
   TTree *newtree = oldtree->CloneTree();
   cout << "Done." << endl;

   //newtree->Print();
   newfile->Write();
   delete _file0;
   delete newfile;
}

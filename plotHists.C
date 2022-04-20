void plotHists(){

	TFile *f = new TFile("trees/_processed_MilliQan_Run1.combined_PMT121_Cd109.root","READ");
        TTree *t = nullptr;
        //TH1D *h = new TH1D("h","","");
        f->GetObject("t",t);
	t->Draw("max","","hist");
        //h->SetLineColor(kRed);
        //h->Draw("hist");
        //gPad->GetListOfPrimitives()->At(0);
        //((TH1D*)(gPad->GetListOfPrimitives()->At(0)))->SetLineColor(0);
	//TCanvas *c = new TCanvas();
	//TH1D *h = (TH1D*)f->Get("T->max");
	//h->SetLineColor(kBlack);
	TFile *f1 = new TFile("trees/_processed_MilliQan_Run1.combined_PMT121_noSource.root","READ");
	//TH1D *h1 = new TH1D("h1","","");
        f1->GetObject("t",t);
	t->Draw("max","","hist same");
        //h1->SetLineColor(kBlue);
        //h1->Draw("same");
        //gPad->GetListOfPrimitives()->At(1);
        //((TH1D*)(gPad->GetListOfPrimitives()->At(1)))->SetLineColor(1);

}

//first index is layer=0,1,2
//second index is column: L=0,R=1
//third index is height in column: bottom=0, top=2
int channelMap[3][2][3] = {
  { {8, 24,0}, {9, 25, 1} },
  { {12, 16, 6}, {13, 17, 7} },
  { {4, 22, 2}, {5, 23, 3} }
};

// define the parametric line equation
void line(double t, vector<double> parFit, double &x, double &y, double &z)
{
  double p[4];
  // xz
  p[0] =  -1.*parFit.at(1)/parFit.at(0);
  p[1] =  1./parFit.at(0);
  // yz
  p[2] =  -1.*parFit.at(5)/parFit.at(4);
  p[3] =  1./parFit.at(4);

  x = p[0] + p[1]*t;
  y = p[2] + p[3]*t;
  z = t;
}

void line(double t, const double *p, double &x, double &y, double &z) {
    // a parametric line is define from 6 parameters but 4 are independent
    // x0,y0,z0,z1,y1,z1 which are the coordinates of two points on the line
    // can choose z0 = 0 if line not parallel to x-y plane and z1 = 1;
    x = p[0] + p[1]*t;
    y = p[2] + p[3]*t;
    z = t;
 }

std::vector<int> convertRawToPhysCh(unsigned int raw_ch, bool isHS)
{
  int phys_ch[3] ={0,0,0}; // x, y, z
  if(isHS)
  {
     // bottom vertical bars
     if(raw_ch==0)        {phys_ch[0]= -4;  phys_ch[1]=  0;  phys_ch[2]=  2;}
     else if(raw_ch==1)   {phys_ch[0]= -3;  phys_ch[1]=  0;  phys_ch[2]=  2;}
     else if(raw_ch==2)   {phys_ch[0]= -2;  phys_ch[1]=  0;  phys_ch[2]=  2;}
     else if(raw_ch==3)   {phys_ch[0]= -1;  phys_ch[1]=  0;  phys_ch[2]=  2;}
     else if(raw_ch==4)   {phys_ch[0]= -4;  phys_ch[1]=  0;  phys_ch[2]=  1;}
     else if(raw_ch==5)   {phys_ch[0]= -3;  phys_ch[1]=  0;  phys_ch[2]=  1;}
     else if(raw_ch==6)   {phys_ch[0]= -2;  phys_ch[1]=  0;  phys_ch[2]=  1;}
     else if(raw_ch==7)   {phys_ch[0]= -1;  phys_ch[1]=  0;  phys_ch[2]=  1;}
     else if(raw_ch==8)   {phys_ch[0]=  1;  phys_ch[1]=  0;  phys_ch[2]=  2;}
     else if(raw_ch==9)   {phys_ch[0]=  2;  phys_ch[1]=  0;  phys_ch[2]=  2;}
     else if(raw_ch==10)  {phys_ch[0]=  3;  phys_ch[1]=  0;  phys_ch[2]=  2;}
     else if(raw_ch==11)  {phys_ch[0]=  4;  phys_ch[1]=  0;  phys_ch[2]=  2;}
     else if(raw_ch==12)  {phys_ch[0]=  1;  phys_ch[1]=  0;  phys_ch[2]=  1;}
     else if(raw_ch==13)  {phys_ch[0]=  2;  phys_ch[1]=  0;  phys_ch[2]=  1;}
     else if(raw_ch==14)  {phys_ch[0]=  3;  phys_ch[1]=  0;  phys_ch[2]=  1;}
     else if(raw_ch==15)  {phys_ch[0]=  4;  phys_ch[1]=  0;  phys_ch[2]=  1;}
     // bottom horizontal bars
     else if(raw_ch==16)  {phys_ch[0]=  0;  phys_ch[1]=  8;  phys_ch[2]=  1;}
     else if(raw_ch==17)  {phys_ch[0]=  0;  phys_ch[1]=  7;  phys_ch[2]=  1;}
     else if(raw_ch==18)  {phys_ch[0]=  0;  phys_ch[1]=  6;  phys_ch[2]=  1;}
     else if(raw_ch==19)  {phys_ch[0]=  0;  phys_ch[1]=  5;  phys_ch[2]=  1;}
     else if(raw_ch==20)  {phys_ch[0]=  0;  phys_ch[1]=  8;  phys_ch[2]=  2;}
     else if(raw_ch==21)  {phys_ch[0]=  0;  phys_ch[1]=  7;  phys_ch[2]=  2;}
     else if(raw_ch==22)  {phys_ch[0]=  0;  phys_ch[1]=  6;  phys_ch[2]=  2;}
     else if(raw_ch==23)  {phys_ch[0]=  0;  phys_ch[1]=  5;  phys_ch[2]=  2;}
     else if(raw_ch==24)  {phys_ch[0]=  0;  phys_ch[1]=  4;  phys_ch[2]=  1;}
     else if(raw_ch==25)  {phys_ch[0]=  0;  phys_ch[1]=  3;  phys_ch[2]=  1;}
     else if(raw_ch==26)  {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]=  1;}
     else if(raw_ch==27)  {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]=  1;}
     else if(raw_ch==28)  {phys_ch[0]=  0;  phys_ch[1]=  4;  phys_ch[2]=  2;}
     else if(raw_ch==29)  {phys_ch[0]=  0;  phys_ch[1]=  3;  phys_ch[2]=  2;}
     else if(raw_ch==30)  {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]=  2;}
     else if(raw_ch==31)  {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]=  2;}
     // top horizontal bars
     else if(raw_ch==32)  {phys_ch[0]=  0;  phys_ch[1]=  4;  phys_ch[2]= -2;}
     else if(raw_ch==33)  {phys_ch[0]=  0;  phys_ch[1]=  3;  phys_ch[2]= -2;}
     else if(raw_ch==34)  {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]= -2;}
     else if(raw_ch==35)  {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]= -2;}
     else if(raw_ch==36)  {phys_ch[0]=  0;  phys_ch[1]=  4;  phys_ch[2]= -1;}
     else if(raw_ch==37)  {phys_ch[0]=  0;  phys_ch[1]=  3;  phys_ch[2]= -1;}
     else if(raw_ch==38)  {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]= -1;}
     else if(raw_ch==39)  {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]= -1;}
     else if(raw_ch==40)  {phys_ch[0]=  0;  phys_ch[1]=  8;  phys_ch[2]= -2;}
     else if(raw_ch==41)  {phys_ch[0]=  0;  phys_ch[1]=  7;  phys_ch[2]= -2;}
     else if(raw_ch==42)  {phys_ch[0]=  0;  phys_ch[1]=  6;  phys_ch[2]= -2;}
     else if(raw_ch==43)  {phys_ch[0]=  0;  phys_ch[1]=  5;  phys_ch[2]= -2;}
     else if(raw_ch==44)  {phys_ch[0]=  0;  phys_ch[1]=  8;  phys_ch[2]= -1;}
     else if(raw_ch==45)  {phys_ch[0]=  0;  phys_ch[1]=  7;  phys_ch[2]= -1;}
     else if(raw_ch==46)  {phys_ch[0]=  0;  phys_ch[1]=  6;  phys_ch[2]= -1;}
     else if(raw_ch==47)  {phys_ch[0]=  0;  phys_ch[1]=  5;  phys_ch[2]= -1;}
     // bottom vertical bars
     else if(raw_ch==48)  {phys_ch[0]=  4;  phys_ch[1]=  0;  phys_ch[2]= -2;}
     else if(raw_ch==49)  {phys_ch[0]=  3;  phys_ch[1]=  0;  phys_ch[2]= -2;}
     else if(raw_ch==50)  {phys_ch[0]=  2;  phys_ch[1]=  0;  phys_ch[2]= -2;}
     else if(raw_ch==51)  {phys_ch[0]=  1;  phys_ch[1]=  0;  phys_ch[2]= -2;}
     else if(raw_ch==52)  {phys_ch[0]=  4;  phys_ch[1]=  0;  phys_ch[2]= -1;}
     else if(raw_ch==53)  {phys_ch[0]=  3;  phys_ch[1]=  0;  phys_ch[2]= -1;}
     else if(raw_ch==54)  {phys_ch[0]=  2;  phys_ch[1]=  0;  phys_ch[2]= -1;}
     else if(raw_ch==55)  {phys_ch[0]=  1;  phys_ch[1]=  0;  phys_ch[2]= -1;}
     else if(raw_ch==56)  {phys_ch[0]= -1;  phys_ch[1]=  0;  phys_ch[2]= -2;}
     else if(raw_ch==57)  {phys_ch[0]= -2;  phys_ch[1]=  0;  phys_ch[2]= -2;}
     else if(raw_ch==58)  {phys_ch[0]= -3;  phys_ch[1]=  0;  phys_ch[2]= -2;}
     else if(raw_ch==59)  {phys_ch[0]= -4;  phys_ch[1]=  0;  phys_ch[2]= -2;}
     else if(raw_ch==60)  {phys_ch[0]= -1;  phys_ch[1]=  0;  phys_ch[2]= -1;}
     else if(raw_ch==61)  {phys_ch[0]= -2;  phys_ch[1]=  0;  phys_ch[2]= -1;}
     else if(raw_ch==62)  {phys_ch[0]= -3;  phys_ch[1]=  0;  phys_ch[2]= -1;}
     else if(raw_ch==63)  {phys_ch[0]= -4;  phys_ch[1]=  0;  phys_ch[2]= -1;}
     else
     {
       cout << "HS raw_ch = " << raw_ch << " is not correct. Enter a correct raw_ch." << endl;
     }
  }
  else
  {
     if(raw_ch==0)        {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]=  4;}
     else if(raw_ch==1)   {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]=  3;}
     else if(raw_ch==2)   {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]=  2;}
     else if(raw_ch==3)   {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]=  1;}
     else if(raw_ch==4)   {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]=  4;}
     else if(raw_ch==5)   {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]=  3;}
     else if(raw_ch==6)   {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]=  2;}
     else if(raw_ch==7)   {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]=  1;}
     else if(raw_ch==8)   {phys_ch[0]=  0;  phys_ch[1]= -2;  phys_ch[2]=  1;}
     else if(raw_ch==9)   {phys_ch[0]=  0;  phys_ch[1]= -2;  phys_ch[2]=  2;}
     else if(raw_ch==10)  {phys_ch[0]=  0;  phys_ch[1]= -2;  phys_ch[2]=  3;}
     else if(raw_ch==11)  {phys_ch[0]=  0;  phys_ch[1]= -2;  phys_ch[2]=  4;}
     else if(raw_ch==12)  {phys_ch[0]=  0;  phys_ch[1]= -1;  phys_ch[2]=  1;}
     else if(raw_ch==13)  {phys_ch[0]=  0;  phys_ch[1]= -1;  phys_ch[2]=  2;}
     else if(raw_ch==14)  {phys_ch[0]=  0;  phys_ch[1]= -1;  phys_ch[2]=  3;}
     else if(raw_ch==15)  {phys_ch[0]=  0;  phys_ch[1]= -1;  phys_ch[2]=  4;}
     else if(raw_ch==16)  {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]=  1;}
     else if(raw_ch==17)  {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]=  2;}
     else if(raw_ch==18)  {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]=  3;}
     else if(raw_ch==19)  {phys_ch[0]=  0;  phys_ch[1]=  1;  phys_ch[2]=  4;}
     else if(raw_ch==20)  {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]=  1;}
     else if(raw_ch==21)  {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]=  2;}
     else if(raw_ch==22)  {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]=  3;}
     else if(raw_ch==23)  {phys_ch[0]=  0;  phys_ch[1]=  2;  phys_ch[2]=  4;}
     else
     {
       cout << "TP raw_ch = " << raw_ch << " is not correct. Enter a correct raw_ch." << endl;
     }
  }

  std::vector<int> phys_ch_vec;
  phys_ch_vec.push_back(phys_ch[0]);
  phys_ch_vec.push_back(phys_ch[1]);
  phys_ch_vec.push_back(phys_ch[2]);
  return phys_ch_vec;
}

std::vector<float> convertPhysChToCoord(std::vector<int> phys_ch, bool isHS)
{
  // unit = cm
  float space_btw_packs = 1;
  float space_btw_bars  = 0.2;

  int phys_ch_x = phys_ch[0];
  int phys_ch_y = phys_ch[1];
  int phys_ch_z = phys_ch[2];

  float x=-999;
  float y=-999;
  float z=-999;
  float ex=-999;
  float ey=-999;
  float ez=-999;

  if(isHS)
  {
    // vertical: y=0
    if(phys_ch_y==0)
    {
      // bottom: z>0
      if(phys_ch_z>0)
      {
        // x
        if(phys_ch_x>0) x = space_btw_packs/2 + 2./2 + (phys_ch_x-1)*2. + (phys_ch_x-1)*0.2;
        else x = -1*space_btw_packs/2 - 2./2 + (phys_ch_x+1)*2. + (phys_ch_x+1)*0.2;
        // z
        z = 180 + 0.5 +  (phys_ch_z-1)*2. + 2./2 + (phys_ch_z-1)*0.2;
        // y: approximate
        y=0;
      }
      // top: z<0
      else
      {
        // x
        if(phys_ch_x>0) x = space_btw_packs/2 + 2./2 + (phys_ch_x-1)*2. + (phys_ch_x-1)*0.2;
        else x = -1*space_btw_packs/2 - 2./2 + (phys_ch_x+1)*2. + (phys_ch_x+1)*0.2;
        // z
        z = -180 - 10 - 0.5 + (1+phys_ch_z)*2. - 2./2 + (1+phys_ch_z)*0.2;
        // y
        y=0;
      }
      //ex = TMath::Sqrt(2.*2./12.);
      //ey = TMath::Sqrt(45.*45./12.);
      //ez = TMath::Sqrt(2.*2./12.);
      ex = TMath::Sqrt(0.2*0.2/12.);
      ey = TMath::Sqrt(45.*45./12.);
      ez = TMath::Sqrt(0.2*0.2/12.);
    }
    // horizontal: x=0
    if(phys_ch_x==0)
    {
      // y
      if(phys_ch_y<5) y = -1.25 + (phys_ch_y-1)*2. + (phys_ch_y-1)*0.2;
      else y = -1.25 + (phys_ch_y-1)*2. + (phys_ch_y-1)*0.2+0.8;

      // bottom: z>0
      if(phys_ch_z>0)
      {
        z = 180 - (2-phys_ch_z)*2. - 2./2 - (2-phys_ch_z)*0.2;
      }
      // top: z<0
      else
      {
        z = -180 - 5 + (phys_ch_z+1)*2. - 2./2 + (phys_ch_z+1)*0.2;
      }
      x=0;
      //ex = TMath::Sqrt(45.*45./12.);
      //ey = TMath::Sqrt(2.*2./12.);
      //ez = TMath::Sqrt(2.*2./12.);
      ex = TMath::Sqrt(45.*45./12.);
      ey = TMath::Sqrt(0.2*0.2/12.);
      ez = TMath::Sqrt(0.2*0.2/12.);
    }
  }
  else
  {
    cout << "TP ... " << endl;
  }

  std::vector<float> coord_vec;
  coord_vec.push_back(x);
  coord_vec.push_back(y);
  coord_vec.push_back(z);
  // uncertainty
  // note that the variance of a flat distribution is l^2/12 where l is the width
  coord_vec.push_back(ex);
  coord_vec.push_back(ey);
  coord_vec.push_back(ez);
  return coord_vec;
}


void lineInverted(double t, vector<double> parFit, double &x, double &y, double &z)
{
  double p[4];
  // xz
  //p[0] =  -1.*parFit.at(1)/parFit.at(0);
  //p[1] =  1./parFit.at(0);
  p[1] = parFit.at(0);
  p[0] = parFit.at(1);

  // yz note: parFit.at(3) ==

  //p[2] =  -1.*parFit.at(5)/parFit.at(4);
  //p[3] =  1./parFit.at(4);
  p[3] = parFit.at(4);
  p[2] = parFit.at(5);

  x = p[0] + p[1]*t;
  y = p[2] + p[3]*t;
  z = t;
}



// track fit
vector<double> doFit(vector<int> *hs_data)
{
  // return this vector
  vector<double> parFit;
  parFit.clear();

  if(hs_data->size()<2) return parFit;

  // arrays for fit
  const int n = hs_data->size();
  Double_t x[n], y[n], z[n];
  Double_t ex[n], ey[n], ez[n];

  int n_hs_botver=0;
  int n_hs_bothor=0;
  int n_hs_topver=0;
  int n_hs_tophor=0;
  int n_hs_bot=0;
  int n_hs_top=0;
  for(unsigned int ihs=0; ihs<hs_data->size(); ihs++)
  {
    int ch = hs_data->at(ihs);
    //cout << "hs hits: " << ch << endl;
    if(ch<16) n_hs_botver++;
    if(ch>=48) n_hs_topver++;
    if(ch>=16 && ch<32) n_hs_bothor++;
    if(ch>=32 && ch<48) n_hs_tophor++;
    if(ch<32) n_hs_bot++;
    if(ch>=32) n_hs_top++;
  }

  bool doTrackFit = false;
  doTrackFit = n_hs_topver>0 && n_hs_botver>0 && n_hs_tophor>0 && n_hs_bothor>0;
  //doTrackFit = n_hs_bot>1 && n_hs_top>1;

  if(0)
  {
    cout << "Number of top vertical hits:   " << n_hs_topver << endl;
    cout << "Number of bot vertical hits:   " << n_hs_botver << endl;
    cout << "Number of top horizontal hits: " << n_hs_tophor << endl;
    cout << "Number of bot horizontal hits: " << n_hs_bothor << endl;
    cout << "Perform fit or not:            " << doTrackFit << endl;
  }

  //
  if(!doTrackFit) return parFit;

  // 1. convert to physical channels
  // Hodoscope
  for(unsigned int i=0; i<hs_data->size(); i++)
  {
    std::vector<int> phys_ch = convertRawToPhysCh(hs_data->at(i), true);
    std::vector<float> coord_ch = convertPhysChToCoord(phys_ch, true);
    if(0)
    {
      cout << hs_data->at(i) << " :: " << phys_ch[0] << " " << phys_ch[1] << " " << phys_ch[2] << endl;
      cout << coord_ch[0] << " +/- " << coord_ch[3] << endl;
      cout << coord_ch[1] << " +/- " << coord_ch[4] << endl;
      cout << coord_ch[2] << " +/- " << coord_ch[5] << endl;
      cout << endl;
    }

    //TESTING
    //if(coord_ch[0] != 0) x[i] = coord_ch[0];
    //if(coord_ch[1] != 0) y[i] = coord_ch[1];
    x[i] = coord_ch[0];
    y[i] = coord_ch[1];
    z[i] = coord_ch[2];
    //TESTING
    //if(coord_ch[0] != 0) ex[i] = coord_ch[3];
    //if(coord_ch[1] != 0) ey[i] = coord_ch[4];
    ex[i] = coord_ch[3];
    ey[i] = coord_ch[4];
    ez[i] = coord_ch[5];
    phys_ch.clear();
    coord_ch.clear();
  }

  TGraphErrors *g_xz = new TGraphErrors(n, x, z, ex, ez);
  TF1 *f_xz = new TF1("f_xz","x*[0]+[1]", 1000, -1000);
  int fit_xz_status = g_xz->Fit("f_xz");

  TGraphErrors *g_yz = new TGraphErrors(n, y, z, ey, ez);
  TF1 *f_yz = new TF1("f_yz","x*[0]+[1]", 1000, -1000);
  int fit_yz_status = g_yz->Fit("f_yz");

  if(fit_xz_status==0 || f_xz->GetParameter(0)>10000)
  {
    parFit.push_back(f_xz->GetParameter(0));
    parFit.push_back(f_xz->GetParameter(1));
  }
  else{
    parFit.push_back(-1);
    parFit.push_back(-1);
  }
  if(fit_yz_status==0 || f_yz->GetParameter(0)>10000)
  {
    parFit.push_back(f_yz->GetParameter(0));
    parFit.push_back(f_yz->GetParameter(1));
  }
  else
  {
    parFit.push_back(-1);
    parFit.push_back(-1);
  }

  return parFit;
}
//
void getPathLengthInverted(vector<double> parFit, vector<int> &chan, vector<double> &path_length)
{

  //   l1          l2          l3
  // 0    1      6    7      2    3
  // 24   25     16   17     22   23
  // 8    9      12   13     4    5
  double l1_z_center      = 120+10+2;
  double l2_z_center      = 0+10;
  double l3_z_center      = -120+10-5;
  double col_left_center  = -3;
  double col_right_center = 3;
  double row1_center      = 0;
  double row2_center      = 6;
  double row3_center      = 12;

  int ch[32];
  for(int i=0; i<32; i++) ch[i]=0;

  //
  int ndiv = 10000;
  double t0 = 0;
  double dt = 200;
  for(int i=0; i<2*ndiv; i++)
  {
    double t = t0 + dt*i/ndiv - dt;
    double x,y,z;
    lineInverted(t,parFit,x,y,z);

    // layer1
    if(z>l1_z_center-40 && z<l1_z_center+40)
    {
      // left column
      if(x>col_left_center-2.5 && x<col_left_center+2.5)
      {
        if(y>row3_center-2.5 && y<row3_center+2.5) ch[0]++;   // row3
        if(y>row2_center-2.5 && y<row2_center+2.5) ch[24]++;  // row2
        if(y>row1_center-2.5 && y<row1_center+2.5) ch[8]++;   // row1
      }
      // right column
      if(x>col_right_center-2.5 && x<col_right_center+2.5)
      {
        if(y>row3_center-2.5 && y<row3_center+2.5) ch[1]++;   // row3
        if(y>row2_center-2.5 && y<row2_center+2.5) ch[25]++;  // row2
        if(y>row1_center-2.5 && y<row1_center+2.5) ch[9]++;   // row1
      }
    }
    // layer2
    if(z>l2_z_center-40 && z<l2_z_center+40)
    {
      // left column
      if(x>col_left_center-2.5 && x<col_left_center+2.5)
      {
        if(y>row3_center-2.5 && y<row3_center+2.5) ch[6]++;   // row3
        if(y>row2_center-2.5 && y<row2_center+2.5) ch[16]++;  // row2
        if(y>row1_center-2.5 && y<row1_center+2.5) ch[12]++;  // row1
      }
      // right column
      if(x>col_right_center-2.5 && x<col_right_center+2.5)
      {
        if(y>row3_center-2.5 && y<row3_center+2.5) ch[7]++;   // row3
        if(y>row2_center-2.5 && y<row2_center+2.5) ch[17]++;  // row2
        if(y>row1_center-2.5 && y<row1_center+2.5) ch[13]++;  // row1
      }
    }
    // layer3
    if(z>l3_z_center-40 && z<l3_z_center+40)
    {
      // left column
      if(x>col_left_center-2.5 && x<col_left_center+2.5)
      {
        if(y>row3_center-2.5 && y<row3_center+2.5) ch[2]++;   // row3
        if(y>row2_center-2.5 && y<row2_center+2.5) ch[22]++;  // row2
        if(y>row1_center-2.5 && y<row1_center+2.5) ch[4]++;   // row1
      }
      // right column
      if(x>col_right_center-2.5 && x<col_right_center+2.5)
      {
        if(y>row3_center-2.5 && y<row3_center+2.5) ch[3]++;   // row3
        if(y>row2_center-2.5 && y<row2_center+2.5) ch[23]++;  // row2
        if(y>row1_center-2.5 && y<row1_center+2.5) ch[5]++;   // row1
      }
    }
  }

  for(int i=0; i<32; i++)
  {
    if(ch[i]>0)
    {
      chan.push_back(i);
      float delta_z = ch[i]*dt/ndiv;
      float delta_x = delta_z/parFit.at(0);
      float delta_y = delta_z/parFit.at(2);
      path_length.push_back(TMath::Sqrt(delta_x*delta_x+delta_y*delta_y+delta_z*delta_z));
    }
  }

}

//
class hsData
{
  private:
    int   event_mq_;
    int   epoch_time_;
    int   us_;
    std::vector<bool>  data_hs_;
    std::vector<bool>  data_tp_;

  public:
    //
    hsData(int epoch_time, int us, std::vector<bool> data_hs, std::vector<bool> data_tp, int event_mq)
    {
      epoch_time_ = epoch_time;
      us_         = us;
      event_mq_   = event_mq;
      for(unsigned int i=0; i<data_hs.size(); i++) data_hs_.push_back(data_hs[i]);
      for(unsigned int i=0; i<data_tp.size(); i++) data_tp_.push_back(data_tp[i]);
    }
    //
    hsData(TString tstr_data, bool preTS1)
    {
      tstr_data.ReplaceAll(" ",":");

      TObjArray *tk_data = tstr_data.Tokenize(":");
      epoch_time_ =  (static_cast<TObjString*>(tk_data->At(0)))->String().Atoi();
      us_         =  (static_cast<TObjString*>(tk_data->At(7)))->String().Atoi();
      // hs data
      for(int i=38; i<=164; i=i+2)
      {
        if(tstr_data[i]=='1') data_hs_.push_back(1);
        else data_hs_.push_back(0);
      }
      // trackpack data
      for(int i=167; i<=213; i=i+2)
      {
        if(tstr_data[i]=='1') data_tp_.push_back(1);
        else data_tp_.push_back(0);
      }
      // extrg
      if(!preTS1 && tstr_data[216]=='1') event_mq_=1;
      else event_mq_=0;

      delete tk_data;
    }
    //
    int getEpochTime()            {return epoch_time_;               }
    double getMicroTime()         {return epoch_time_+0.000001*us_;  }
    std::vector<bool> getHSData() {return data_hs_;                  }
    std::vector<bool> getTPData() {return data_tp_;                  }
    int isMQEvent()               {return event_mq_;  }
    void printData()
    {
      std::cout << epoch_time_+0.000001*us_ << " " << event_mq_ << " ";
      for(unsigned int i=0; i<data_hs_.size(); i++) std::cout << data_hs_.at(i);
      std::cout << " " ;
      for(unsigned int i=0; i<data_tp_.size(); i++) std::cout << data_tp_.at(i);
      std::cout << std::endl;
    }
};

TString kind_str(int kind)
{
  if(kind==-1) return "previous";
  else if(kind==1) return "next";
  else return "current";
}

void loadHSDataTree(TString hs_file_dir, TString hs_file, std::vector<hsData> &hsDataLoaded, int kind, bool preTS1=false)
{
  ifstream fin(Form("%s/%s", hs_file_dir.Data(), hs_file.Data()));
  // cout << (Form("Loading %s HS file: %s/%s", kind_str(kind).Data(), hs_file_dir.Data(), hs_file.Data())) << endl;

  // Get the number of events
  int nLines=-1;
  string s;
  if(fin.is_open())
  {
    while(fin.good())
    {
      getline(fin, s);
      nLines++;
    }
  }
  // cout << "Number of lines: " << nLines << endl;
  fin.close();

  // Add events to memory
  ifstream finfile(Form("%s/%s", hs_file_dir.Data(), hs_file.Data()));
  int line=0;
  if(finfile.is_open())
  {
    while(finfile.good())
    {
      // get a line from finfile
      getline(finfile, s);
      line++;

      if(line>nLines) break;

      if(kind==-1 && line<nLines*0.9) continue;
      if(kind==1 && line>nLines*0.1) break;

      hsData hsDataOne(static_cast<TString>(s), preTS1);
      hsDataLoaded.push_back(hsDataOne);
    }
  }
  finfile.close();
}

void loadHSData(TString hs_file_dir, TString hs_file, std::vector<hsData> &hsDataLoaded, int kind, bool preTS1=false)
{
  ifstream fin(Form("%s/%s", hs_file_dir.Data(), hs_file.Data()));
  // cout << (Form("Loading %s HS file: %s/%s", kind_str(kind).Data(), hs_file_dir.Data(), hs_file.Data())) << endl;

  // Get the number of events
  int nLines=-1;
  string s;
  if(fin.is_open())
  {
    while(fin.good())
    {
      getline(fin, s);
      nLines++;
    }
  }
  // cout << "Number of lines: " << nLines << endl;
  fin.close();

  // Add events to memory
  ifstream finfile(Form("%s/%s", hs_file_dir.Data(), hs_file.Data()));
  int line=0;
  if(finfile.is_open())
  {
    while(finfile.good())
    {
      // get a line from finfile
      getline(finfile, s);
      line++;

      if(line>nLines) break;

      if(kind==-1 && line<nLines*0.9) continue;
      if(kind==1 && line>nLines*0.1) break;

      hsData hsDataOne(static_cast<TString>(s), preTS1);
      hsDataLoaded.push_back(hsDataOne);
    }
  }
  finfile.close();
}


vector<double> doCircleFit(vector<int> * hs_data)
{
  // return this vector
  vector<double> parFit;
  parFit.clear();

  if(hs_data->size()<2) return parFit;

  // arrays for fit
  const int n = hs_data->size();
  Double_t x[n], y[n], z[n];
  Double_t ex[n], ey[n], ez[n];

  int n_hs_botver=0;
  int n_hs_bothor=0;
  int n_hs_topver=0;
  int n_hs_tophor=0;
  int n_hs_bot=0;
  int n_hs_top=0;
  for(unsigned int ihs=0; ihs<hs_data->size(); ihs++)
  {
    int ch = hs_data->at(ihs);
    //cout << "hs hits: " << ch << endl;
    if(ch<16) n_hs_botver++;
    if(ch>=48) n_hs_topver++;
    if(ch>=16 && ch<32) n_hs_bothor++;
    if(ch>=32 && ch<48) n_hs_tophor++;
    if(ch<32) n_hs_bot++;
    if(ch>=32) n_hs_top++;
  }

  bool doTrackFit = false;
  doTrackFit = n_hs_topver>0 && n_hs_botver>0 && n_hs_tophor>0 && n_hs_bothor>0;
  //doTrackFit = n_hs_bot>1 && n_hs_top>1;

  if(0)
  {
    cout << "Number of top vertical hits:   " << n_hs_topver << endl;
    cout << "Number of bot vertical hits:   " << n_hs_botver << endl;
    cout << "Number of top horizontal hits: " << n_hs_tophor << endl;
    cout << "Number of bot horizontal hits: " << n_hs_bothor << endl;
    cout << "Perform fit or not:            " << doTrackFit << endl;
  }

  //
  if(!doTrackFit) return parFit;

  // 1. convert to physical channels
  // Hodoscope
  for(unsigned int i=0; i<hs_data->size(); i++)
  {
    std::vector<int> phys_ch = convertRawToPhysCh(hs_data->at(i), true);
    std::vector<float> coord_ch = convertPhysChToCoord(phys_ch, true);
    if(0)
    {
      cout << hs_data->at(i) << " :: " << phys_ch[0] << " " << phys_ch[1] << " " << phys_ch[2] << endl;
      cout << coord_ch[0] << " +/- " << coord_ch[3] << endl;
      cout << coord_ch[1] << " +/- " << coord_ch[4] << endl;
      cout << coord_ch[2] << " +/- " << coord_ch[5] << endl;
      cout << endl;
    }
    x[i] = coord_ch[0];
    y[i] = coord_ch[1];
    z[i] = coord_ch[2];
    ex[i] = coord_ch[3];
    ey[i] = coord_ch[4];
    ez[i] = coord_ch[5];
    phys_ch.clear();
    coord_ch.clear();
  }

  TGraphErrors *g_xz = new TGraphErrors(n, x, z, ex, ez);
  TF1 *f_xz = new TF1("f_xz","x*[0]+[1]", 1000, -1000);
  int fit_xz_status = g_xz->Fit("f_xz", "q");

  TGraphErrors *g_yz = new TGraphErrors(n, y, z, ey, ez);
  TF1 *f_yz = new TF1("f_yz","x*[0]+[1]", 1000, -1000);
  int fit_yz_status = g_yz->Fit("f_yz", "q");

  if(fit_xz_status==0 || f_xz->GetParameter(0)>10000)
  {
    parFit.push_back(f_xz->GetParameter(0));
    parFit.push_back(f_xz->GetParameter(1));
    parFit.push_back(f_xz->GetParError(0));
    parFit.push_back(f_xz->GetParError(1));
  }
  else{
    parFit.push_back(-1);
    parFit.push_back(-1);
    parFit.push_back(-1);
    parFit.push_back(-1);
  }
  if(fit_yz_status==0 || f_yz->GetParameter(0)>10000)
  {
    parFit.push_back(f_yz->GetParameter(0));
    parFit.push_back(f_yz->GetParameter(1));
    parFit.push_back(f_yz->GetParError(0));
    parFit.push_back(f_yz->GetParError(1));
  }
  else
  {
    parFit.push_back(-1);
    parFit.push_back(-1);
    parFit.push_back(-1);
    parFit.push_back(-1);
  }

  return parFit;
}



















bool equalDoubles(double a, double b, double epsilon = 1e-320){
    return abs(a - b) <= epsilon;
}

int checkIntervalOverlap(double min1Temp, double max1Temp, double min2Temp, double max2Temp) {
  // 0 == intervals don't overlap
  // 1 == intervals overlap but not contained within each other
  // 2 == interval 2 inside 1
  // 3 == interval 1 inside 2
  // 4 == same interval 

  double min1(min1Temp), max1(max1Temp), min2(min2Temp), max2(max2Temp);
  // if intervals not ordered, order them:
  if(max1 < min1){ min1Temp = max1; max1Temp = min1; }
  if(max2 < min2){ min2Temp = max2; max2Temp = min2; }

  int intervalStatus = 0;

  // check if either interval is a point:
  bool point1 = equalDoubles(min1, max1);
  bool point2 = equalDoubles(min2, max2);

  if(point1 && !point2){
    if(min1 > min2 && min1 < max2) intervalStatus = 1;
    if(equalDoubles(min1, min2)||equalDoubles(min1, max2)) intervalStatus = 4;
  }
  else if(!point1 && point2){
    if(min2 > min1 && min2 < max1) intervalStatus = 1;
    if(equalDoubles(min2, min1)||equalDoubles(min2, max1)) intervalStatus = 4;
  }
  else if(point1 && point2){
    if(equalDoubles(min1, min2)) intervalStatus = 4;
  }
  else{
    // intervals overlap but not inside
    if(equalDoubles(max1, min2) &&  min1 < min2 && max2 > min2) intervalStatus = 1;
    else if(equalDoubles(max2, min1) && min2 < min1) intervalStatus = 1;
    else if(min1 > min2 && min1 < max2 && max1 > max2) intervalStatus = 1;
    else if(min2 > min1 && min2 < max1 && max2 > max1) intervalStatus = 1;

    // interval 2 inside 1
    if(min2 > min1 && min2 < max1 && max2 > min1 && max2 < max1) intervalStatus = 2;
    else if(equalDoubles(min1, min2) && max2 < max1) intervalStatus = 2;
    else if(equalDoubles(max1, max2) && min2 > min1) intervalStatus = 2;

    // interval 1 inside 2
    if(min1 > min2 && min1 < max2 && max1 > min2 && max1 < max2) intervalStatus = 3;
    else if(equalDoubles(min1, min2) && max1 < max2) intervalStatus = 3;
    else if(equalDoubles(max1, max2) && min1 > min2) intervalStatus = 3;

    // intervals equal
    if(equalDoubles(min1, min2) && equalDoubles(max1, max2)) intervalStatus = 4;
  }
  
  return intervalStatus;
}


///////////////////////////////////////////////////////////////////////////////////////////////////// Inverted Stuff

void getCirclePathLengthInverted(vector<double> parFit, vector<int> &chan, vector<double> &path_length, int runFit, int fileFit, int eventFit, string stringFit, bool& mathematicaRequired, bool weighted)
{
  bool testing = false;

  bool parFitGood = true;
  if(parFit.size() == 0) return;

  for(auto i:parFit){
    if(abs(-1 - i) < 5e-324) parFitGood = false;
  }

  if(!parFitGood) return;

  //   l1          l2          l3
  // 0    1      6    7      2    3
  // 24   25     16   17     22   23
  // 8    9      12   13     4    5
  double l1_z_center      = 120+10+2;
  double l2_z_center      = 0+10;
  double l3_z_center      = -120+10-5;
  double col_left_center  = -3;
  double col_right_center = 3;
  double row1_center      = 0;
  double row2_center      = 6;
  double row3_center      = 12;

  vector<int> ch(32,0);

  //
  int ndiv = 150;
  double t0 = 0;
  double dt = 200;

  ofstream fout;
  // ofstream foutNoMath;
  if(!testing){
    fout.open(stringFit, std::ios_base::app);
    // foutNoMath.open(stringFit+"noMath.txt", std::ios_base::app);
  }


  for(int i=0; i<2*ndiv; i++)
  {
    vector<int> tempCh(32,0);

    double t = t0 + dt*i/ndiv - dt;
    double x,y,z;

    lineInverted(t,parFit,x,y,z);

    // indices 2,3 are xz errors, 6,7 are yz errors
    double xInterceptError = parFit[3];
    double xSlopeError = parFit[2];
    double yInterceptError = parFit[7];
    double ySlopeError = parFit[6];

    //half of the error
    //error given by distance between max slope error  and max yint slope
    double x_axis_length = sqrt(pow(z,2)*pow(xSlopeError,2) + pow(xInterceptError, 2));
    double y_axis_length = sqrt(pow(z,2)*pow(ySlopeError,2) + pow(yInterceptError, 2));

    //cout << "{Ellipsoid[{" << x << ", " << y << ", " <<  z << "},{" << x_axis_length << ", " << y_axis_length << ",0}]}, " << endl;

    int axesInsideSquare = 0;
    int layer = -1;
    vector<int> rows = {};
    vector<int> cols = {};

    // layers
    if(z>l1_z_center-40 && z<l1_z_center+40) layer = 1;
    if(z>l2_z_center-40 && z<l2_z_center+40) layer = 2;
    if(z>l3_z_center-40 && z<l3_z_center+40) layer = 3;

    //cols
    if(weighted){
      int col1Status = checkIntervalOverlap(x-x_axis_length, x+x_axis_length, col_left_center - 2.5, col_left_center + 2.5);
      int col2Status = checkIntervalOverlap(x-x_axis_length, x+x_axis_length, col_right_center - 2.5, col_right_center +2.5);
      if(col1Status > 0) cols.push_back(1);
      if(col2Status > 0) cols.push_back(2);
      if(col1Status == 3 || col2Status == 3) ++axesInsideSquare;
    }
    else{
      int col1Status = checkIntervalOverlap(x, x, col_left_center - 2.5, col_left_center + 2.5);
      int col2Status = checkIntervalOverlap(x, x, col_right_center - 2.5, col_right_center +2.5);
      if(col1Status > 0) cols.push_back(1);
      if(col2Status > 0) cols.push_back(2);
    }

    //rows
    if(weighted){
      int row1Status = checkIntervalOverlap(y-y_axis_length, y+y_axis_length, row1_center - 2.5, row1_center +2.5);
      int row2Status = checkIntervalOverlap(y-y_axis_length, y+y_axis_length, row2_center - 2.5, row2_center +2.5);
      int row3Status = checkIntervalOverlap(y-y_axis_length, y+y_axis_length, row3_center - 2.5, row3_center +2.5);
      if(row1Status > 0) rows.push_back(1);
      if(row2Status > 0) rows.push_back(2);
      if(row3Status > 0) rows.push_back(3);
      if(row1Status == 3 || row2Status == 3 || row3Status == 3) ++axesInsideSquare;
    }
    else{
      int row1Status = checkIntervalOverlap(y, y, row1_center - 2.5, row1_center +2.5);
      int row2Status = checkIntervalOverlap(y, y, row2_center - 2.5, row2_center +2.5);
      int row3Status = checkIntervalOverlap(y, y, row3_center - 2.5, row3_center +2.5);
      if(row1Status > 0) rows.push_back(1);
      if(row2Status > 0) rows.push_back(2);
      if(row3Status > 0) rows.push_back(3);
    }

    if(layer > 0 && rows.size() != 0 && cols.size() != 0){
      for(auto c:cols){
        for(auto r:rows){
          //cout << "l: "<< layer << " c: " << c << " r: " << r << endl;
          //cout << "ch: " << channelMap[layer][c][r] << endl;
          tempCh[channelMap[layer-1][c-1][r-1]] = 1;
        }
      }
    }

    mathematicaRequired = false;
    bool channelHit = false;
    for(int i=0; i<32; ++i) if(tempCh[i]>0) channelHit = true;
    for(int i=0; i<32; ++i) if(tempCh[i]>0) ch[i] = 1;
   
    if(channelHit && !testing && axesInsideSquare < 2 && weighted){
      mathematicaRequired = true;
      fout << runFit << " " << fileFit << " " << eventFit << " " << x << " " << y << " " << z << " " << x_axis_length << " " << y_axis_length << endl;
    }

    if(!mathematicaRequired && channelHit){
      // foutNoMath << "Run " << runFit <<  " File " << fileFit <<  " Event "  << eventFit << " Channels {";
      fout << "Run " << runFit <<  " File " << fileFit <<  " Event "  << eventFit << " Channels {";
      bool printedChan = false;

      for(unsigned int t=0;t<tempCh.size(); ++t){
        if(tempCh[t] > 0){
          if(printedChan) fout << ", " << t;
          else{
            fout << " " << t;
            printedChan = true;
          }
          fout << "} Ratios {1.}" << endl;
        }
      }
    } // end line loop
  }
  fout.close();
  // foutNoMath.close();


  for(int i=0; i<32; i++)
  {
    if(ch[i]>0)
    {
      chan.push_back(i);
      float delta_z = ch[i]*dt/ndiv;
      float delta_x = delta_z/parFit.at(0);
      float delta_y = delta_z/parFit.at(2);
      path_length.push_back(TMath::Sqrt(delta_x*delta_x+delta_y*delta_y+delta_z*delta_z));
    }
  }


}




vector<double> doCircleFitInverted(vector<int> * hs_data)
{
  // return this vector
  vector<double> parFit;
  parFit.clear();

  if(hs_data->size()<2) return parFit;

  // arrays for fit
  const int n = hs_data->size();
  Double_t x[n], y[n], z[n];
  Double_t ex[n], ey[n], ez[n];

  int n_hs_botver=0;
  int n_hs_bothor=0;
  int n_hs_topver=0;
  int n_hs_tophor=0;
  int n_hs_bot=0;
  int n_hs_top=0;
  for(unsigned int ihs=0; ihs<hs_data->size(); ihs++)
  {
    int ch = hs_data->at(ihs);
    //cout << "hs hits: " << ch << endl;
    if(ch<16) n_hs_botver++;
    if(ch>=48) n_hs_topver++;
    if(ch>=16 && ch<32) n_hs_bothor++;
    if(ch>=32 && ch<48) n_hs_tophor++;
    if(ch<32) n_hs_bot++;
    if(ch>=32) n_hs_top++;
  }

  bool doTrackFit = false;
  doTrackFit = n_hs_topver>0 && n_hs_botver>0 && n_hs_tophor>0 && n_hs_bothor>0;
  //doTrackFit = n_hs_bot>1 && n_hs_top>1;

  if(0)
  {
    cout << "Number of top vertical hits:   " << n_hs_topver << endl;
    cout << "Number of bot vertical hits:   " << n_hs_botver << endl;
    cout << "Number of top horizontal hits: " << n_hs_tophor << endl;
    cout << "Number of bot horizontal hits: " << n_hs_bothor << endl;
    cout << "Perform fit or not:            " << doTrackFit << endl;
  }

  //
  if(!doTrackFit) return parFit;

  // 1. convert to physical channels
  // Hodoscope
  for(unsigned int i=0; i<hs_data->size(); i++)
  {
    std::vector<int> phys_ch = convertRawToPhysCh(hs_data->at(i), true);
    std::vector<float> coord_ch = convertPhysChToCoord(phys_ch, true);
    if(coord_ch.size() < 6) continue;
    x[i] = coord_ch[0];
    y[i] = coord_ch[1];
    z[i] = coord_ch[2];
    ex[i] = coord_ch[3];
    ey[i] = coord_ch[4];
    ez[i] = coord_ch[5];
    phys_ch.clear();
    coord_ch.clear();
  }

  // NOTE: x and z are switched
  TGraphErrors *g_xz = new TGraphErrors(n, z, x, ez, ex);
  TF1 *f_xz = new TF1("f_xz","x*[0]+[1]", 1000, -1000);
  int fit_xz_status = g_xz->Fit("f_xz", "q");

  // NOTE: y and z switched
  TGraphErrors *g_yz = new TGraphErrors(n, z, y, ez, ey);
  TF1 *f_yz = new TF1("f_yz","x*[0]+[1]", 1000, -1000);
  int fit_yz_status = g_yz->Fit("f_yz", "q");

  if(fit_xz_status==0 || f_xz->GetParameter(0)>10000)
  {
    parFit.push_back(f_xz->GetParameter(0));
    parFit.push_back(f_xz->GetParameter(1));
    parFit.push_back(f_xz->GetParError(0));
    parFit.push_back(f_xz->GetParError(1));
  }
  else{
    parFit.push_back(-1);
    parFit.push_back(-1);
    parFit.push_back(-1);
    parFit.push_back(-1);
  }
  if(fit_yz_status==0 || f_yz->GetParameter(0)>10000)
  {
    parFit.push_back(f_yz->GetParameter(0));
    parFit.push_back(f_yz->GetParameter(1));
    parFit.push_back(f_yz->GetParError(0));
    parFit.push_back(f_yz->GetParError(1));
  }
  else
  {
    parFit.push_back(-1);
    parFit.push_back(-1);
    parFit.push_back(-1);
    parFit.push_back(-1);
  }

  return parFit;
}


void getCirclePathLengthInverted(vector<double> parFit, vector<int> &chan, vector<double> &path_length)
{

  bool parFitGood = true;
  for(auto i:parFit){
    if(abs(-1 - i) < 5e-324) parFitGood = false;
    }
  if(!parFitGood) return;


  //   l1          l2          l3
  // 0    1      6    7      2    3
  // 24   25     16   17     22   23
  // 8    9      12   13     4    5
  double l1_z_center      = 120+10+2;
  double l2_z_center      = 0+10;
  double l3_z_center      = -120+10-5;
  double col_left_center  = -3;
  double col_right_center = 3;
  double row1_center      = 0;
  double row2_center      = 6;
  double row3_center      = 12;

  int ch[32];
  for(int i=0; i<32; i++) ch[i]=0;

  //
  int ndiv = 10000;
  double t0 = 0;
  double dt = 200;

  // TH2D * h2int = new TH2D("h2int", "h2int", 1e6, -1e6, 1e6,  1e6, -1e6, 1e6);
  // TH2D * h2slope = new TH2D("h2slope", "h2slope", 1e6, -1e6, 1e6,  1e6, -1e6, 1e6);

  // cout << "PARFIT: ";
  // for(unsigned int iP=0; iP<parFit.size(); ++iP) cout << parFit[iP] << " ";
  // cout << endl;

  for(int i=0; i<2*ndiv; i++)
  {
    double t = t0 + dt*i/ndiv - dt;
    double x(0), y(0), z(0);
    lineInverted(t,parFit,x,y,z);

    // indices 2,3 are xz errors, 6,7 are yz errors
    double xInterceptError = parFit[3];
    double xSlopeError = parFit[2];
    double yInterceptError = parFit[7];
    double ySlopeError = parFit[6];


    //h2int->Fill(parFit[3]/parFit[1],parFit[7]/parFit[5]);
    //h2slope->Fill(parFit[2]/parFit[0],  parFit[6]/parFit[4]);
    //half of the error
    //error given by distance between max slope error  and max yint slope
    double x_axis_length = sqrt(pow(z,2)*pow(xSlopeError,2) + pow(xInterceptError, 2));
    double y_axis_length = sqrt(pow(z,2)*pow(ySlopeError,2) + pow(yInterceptError, 2));


    //cout << "{Ellipsoid[{" << x << ", " << y << ", " <<  z << "},{" << x_axis_length << ", " << y_axis_length << ",0}]}, " << endl;


    // layer1
    if(z>l1_z_center-40 && z<l1_z_center+40)
    {
      // left column
      //if(x>col_left_center-2.5 && x<col_left_center+2.5)
      if(abs(x - col_left_center) < (2.5 + x_axis_length))
      {
        if(abs(y - row3_center) < (2.5 + y_axis_length)) ch[0]++;   // row3
        if(abs(y - row2_center) < (2.5 + y_axis_length)) ch[24]++;  // row2
        if(abs(y - row1_center) < (2.5 + y_axis_length)) ch[8]++;   // row1
      }
      // right column
      if(abs(x - col_right_center) < (2.5 + x_axis_length))
      {
        if(abs(y - row3_center) < (2.5 + y_axis_length)) ch[1]++;   // row3
        if(abs(y - row2_center) < (2.5 + y_axis_length)) ch[25]++;  // row2
        if(abs(y - row1_center) < (2.5 + y_axis_length)) ch[9]++;   // row1
      }
    }
    // layer2
    if(z>l2_z_center-40 && z<l2_z_center+40)
    {
      // left column
      if(abs(x - col_left_center) < (2.5 + x_axis_length))
      {
        if(abs(y - row3_center) < (2.5 + y_axis_length)) ch[6]++;   // row3
        if(abs(y - row2_center) < (2.5 + y_axis_length)) ch[16]++;  // row2
        if(abs(y - row1_center) < (2.5 + y_axis_length)) ch[12]++;  // row1
      }
      // right column
      if(abs(x - col_right_center) < (2.5 + x_axis_length))
      {
        if(abs(y - row3_center) < (2.5 + y_axis_length)) ch[7]++;   // row3
        if(abs(y - row2_center) < (2.5 + y_axis_length)) ch[17]++;  // row2
        if(abs(y - row1_center) < (2.5 + y_axis_length)) ch[13]++;  // row1
      }
    }
    // layer3
    if(z>l3_z_center-40 && z<l3_z_center+40)
    {
      // left column
      if(abs(x - col_left_center) < (2.5 + x_axis_length))
      {
        if(abs(y - row3_center) < (2.5 + y_axis_length)) ch[2]++;   // row3
        if(abs(y - row2_center) < (2.5 + y_axis_length)) ch[22]++;  // row2
        if(abs(y - row1_center) < (2.5 + y_axis_length)) ch[4]++;   // row1
      }
      // right column
      if(abs(x - col_right_center) < (2.5 + x_axis_length))
      {
        if(abs(y - row3_center) < (2.5 + y_axis_length)) ch[3]++;   // row3
        if(abs(y - row2_center) < (2.5 + y_axis_length)) ch[23]++;  // row2
        if(abs(y - row1_center) < (2.5 + y_axis_length)) ch[5]++;   // row1
      }
    }
  }

  for(int i=0; i<32; i++)
  {
    if(ch[i]>0)
    {
      chan.push_back(i);
      float delta_z = ch[i]*dt/ndiv;
      float delta_x = delta_z/parFit.at(0);
      float delta_y = delta_z/parFit.at(2);
      path_length.push_back(TMath::Sqrt(delta_x*delta_x+delta_y*delta_y+delta_z*delta_z));
    }
  }

}



vector<double> convertBarChToPhysCoord(int barCh){
    vector<int> row3 = {0,1,6,7,2,3};
    vector<int> row2 = {24,25, 16,17, 22,23};
    vector<int> row1 = {8,9,12,13,4,5};

    double x=-999;
    double y=-999;
    for(auto b:row1){
      if(barCh == b) y = 0;
    }
   for(auto b:row2){
      if(barCh == b) y = 6;
    }
    for(auto b:row3){
      if(barCh == b) y = 12;
    }
    if(barCh % 2 == 0) x = -3;
    else x = 3;

    vector<double> coords = {x,y};
    return coords;
}

vector<double> calcIntervalErrors(TH1D * hPassArg,TH1D * hTotalArg){
    vector<double> errorBounds = {-1,-1};
    TGraphAsymmErrors * effGraph = new TGraphAsymmErrors(hPassArg, hTotalArg);
    errorBounds = {effGraph->GetErrorYlow(0),effGraph->GetErrorYhigh(0)};
    return errorBounds;
    }
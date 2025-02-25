//*******************************************************
// S2+L (re)construction using orthogonal sampling method
//*******************************************************

//updated May, 28th, 2008

//modified: 05/14/2012
//the prevous method sampling L was not complete, missing
// important events...

//version 2.0:
//use the most efficient method for sampling S2

using namespace std;

#include <stdio.h>  
#include <stdlib.h> 
#include <math.h>
#include <iostream>
#include <time.h>


#define MAXX 20  
#define MAXY 25000 
#define Nt 10
#define PI acos(-1)

int NP; 
double f1;
double f2;


int pix_position[MAXX]; 
int pix_counter;


int config[MAXX][MAXX];   

int lineS2[MAXX][Nt];    
int columeS2[MAXX][Nt];   


int N2V[MAXX][Nt];       
int N2H[MAXX][Nt];       

double SQ[Nt]; 
double TriVer[Nt];
double TriHor[Nt];
double HexaVer[Nt];
double HexaHor[Nt];
double Octagon[Nt];
int Nside=100;
double Arbi[Nt];





void read_config()   
{
  for(int i=0; i<MAXX; i++)
    for(int j=0; j<MAXX; j++)
      config[i][j] = 0;


  FILE* fp;  

  
  if((fp=fopen("Mconfig.txt","r"))==NULL)
    {
      printf("No Mconfig.txt is found! Abort!\n");
      exit(1);
    }

  int tempx;
  int tempy;

  fscanf(fp, "%d", &NP);  
  int temp_NP = 0;

  for(int i=0; i<NP; i++)
    {

      fscanf(fp, "%d", &tempx); 
      fscanf(fp, "%d", &tempy); 

      if(tempx<MAXX && tempy<MAXX)  
	{
	  config[tempx][tempy] = 1;  
	  temp_NP++;
	}
    }


  NP = temp_NP;                    
  cout<<"NP = "<<NP<<endl;

  fclose(fp);
}






void sampleS2line(int index1)
{
	
  for(int r=0; r<Nt; r++)  // initilize lineS2 for each column 
    {
      lineS2[index1][r] = 0; 
    }


  //serach the line for pixel positions  
  pix_counter = 0;

  for(int i=0; i<MAXX; i++)
    {
      if(config[i][index1] == 1)    
	   {
	  pix_position[pix_counter] = i;  
	  pix_counter++;
	   }
    }

  //now get the distance between all pixels on the line...
  int temp_dist;

  for(int i=0; i<pix_counter; i++)
    for(int j=0; j<=i; j++)
      {
	temp_dist = abs(pix_position[i]-pix_position[j]);

	if(temp_dist>=MAXX/2) temp_dist = MAXX-temp_dist;  

	lineS2[index1][temp_dist]++;  


      }

  
}



void sampleS2colume(int index1)
{

  for(int r=0; r<Nt; r++)
    {
      columeS2[index1][r] = 0;
    }

  
  pix_counter = 0;

  for(int i=0; i<MAXX; i++)
    {
      if(config[index1][i]==1)    //@@@@@@@@@@@@@
	{
	  pix_position[pix_counter] = i;
	  pix_counter++;
	}
    }

  //now get the distance between all pixels on the line...
  int temp_dist;

  for(int i=0; i<pix_counter; i++)
    for(int j=0; j<=i; j++)
      {
	temp_dist = abs(pix_position[i]-pix_position[j]);

	if(temp_dist>=MAXX/2) temp_dist = MAXX-temp_dist;

	columeS2[index1][temp_dist]++;



      }

  
}




void sample_horizontal(int lindex) 
{
  for(int r=0; r<Nt; r++)
    N2H[lindex][r] = 0;  

  int ener[MAXX];     
  int flag_empty = 0;

  for(int i=0; i<MAXX; i++)
    {
      if(config[lindex][i]==0) ener[i]=-1;
      else
	{
	  int en = 0;  
	  int neb1 = i - 1;   
	  if(neb1<0) neb1 = neb1 + MAXX;
	  if(config[lindex][neb1]==1) en++;
	  int neb2 = i+1;
	  if(neb2>=MAXX) neb2 = neb2 - MAXX;  
	  if(config[lindex][neb2]==1) en++;

	  ener[i] = en;  
	  flag_empty ++;  
	}
    }

  int position[MAXX]; 
  for(int i=0; i<MAXX; i++)
    {
      position[i] = -1;  
    }

  int ctp = 0;  
  for(int i=0; i<MAXX; i++)
    {
      if(ener[i]==1) 
	{
	  position[ctp] = i; 
	  ctp++;
	}
      else if(ener[i]==0) 
	{
	  N2H[lindex][0]++;  
	}
    }
  
  
  if(config[lindex][0]==1&&config[lindex][MAXX-1]==1)
    {
      if(ctp>2)  
	{
	  for(int i=1; i<ctp-1; i=i+2)
	    {
	      int len = position[i+1]-position[i]+1;  
	      for(int r=0; r<=len; r++)
		{
		  if(r<Nt) N2H[lindex][r] = N2H[lindex][r]+(len-r);   
		}
	    }

	  int len = (position[0]+1)+(MAXX - position[ctp-1]);   
	  for(int r=0; r<=len; r++)
	    {
	      if(r<Nt) N2H[lindex][r] = N2H[lindex][r]+(len-r);  
	    }
	}
      else if(ctp ==2) 
	{
	  int len = (position[0]+1)+(MAXX - position[ctp-1]);   
	  for(int r=0; r<=len; r++)
	    {
	      if(r<Nt) N2H[lindex][r] = N2H[lindex][r]+(len-r);  
	    }
	}
      else if(ctp == 0 & flag_empty != 0) // ALL black point     
	{
	  int len = MAXX;
	  for(int r=0; r<=len; r++)
	    {
	      if(r<Nt) N2H[lindex][r] = N2H[lindex][r]+(len-r);  
	    }
	}

    }

  //when the cord is not at the bd
  else
    {
      for(int i=0; i<ctp; i=i+2)
	{
	  int len = position[i+1]-position[i]+1;  
	  for(int r= 0; r<=len; r++)
	    {
	      if(r<Nt) N2H[lindex][r] = N2H[lindex][r]+(len-r);  
	    }
	}
    }



}

void sample_vertical(int cindex)  
{
 for(int r=0; r<Nt; r++)
    N2V[cindex][r] = 0;

  int ener[MAXX];
  int flag_empty = 0;
  for(int i=0; i<MAXX; i++)
    {
      if(config[i][cindex]==0) ener[i]=-1;
      else
	{
	  int en = 0;
	  int neb1 = i - 1;
	  if(neb1<0) neb1 = neb1 + MAXX;
	  if(config[neb1][cindex]==1) en++;
	  int neb2 = i+1;
	  if(neb2>=MAXX) neb2 = neb2 - MAXX;
	  if(config[neb2][cindex]==1) en++;

	  ener[i] = en;
	  flag_empty++;
	}
    }

  int position[MAXX];
  for(int i=0; i<MAXX; i++)
    {
      position[i] = -1;
    }

  int ctp = 0;
  for(int i=0; i<MAXX; i++)
    {
      if(ener[i]==1)
	{
	  position[ctp] = i;
	  ctp++;
	}
      else if(ener[i]==0) 
	{
	  N2V[cindex][0]++;
	}
    }

  if(config[0][cindex]==1&&config[MAXX-1][cindex]==1)
    {
      if(ctp>2)
	{
	  for(int i=1; i<ctp-1; i=i+2)
	    {
	      int len = position[i+1]-position[i]+1;
	      for(int r=0; r<=len; r++)
		{
		  if(r<Nt) N2V[cindex][r] = N2V[cindex][r]+(len-r);
		}
	    }

	  int len = (position[0]+1) + (MAXX - position[ctp-1]);
	  for(int r=0; r<=len; r++)
	    {
	      if(r<Nt) N2V[cindex][r] = N2V[cindex][r]+(len-r);
	    }
	}
      else if(ctp ==2)
	{
	  int len = (position[0]+1)+(MAXX - position[ctp-1]);
	  for(int r=0; r<=len; r++)
	    {
	      if(r<Nt) N2V[cindex][r] = N2V[cindex][r]+(len-r);
	    }
	}
      else if(ctp == 0 & flag_empty != 0)
	{
	  int len = MAXX;
	  for(int r=0; r<=len; r++)
	    {
	      if(r<Nt) N2V[cindex][r] = N2V[cindex][r]+(len-r);
	    }
	}

    }
  else
    {
      for(int i=0; i<ctp; i=i+2)
	{
	  int len = position[i+1]-position[i]+1;
	  for(int r= 0; r<=len; r++)
	    {
	      if(r<Nt) N2V[cindex][r] = N2V[cindex][r]+(len-r);
	    }
	}
    }



}

void squrefunction() 
{
	if(Nt<=MAXX/2){          
	
	for (int R=0;R<Nt;R++){  
		
		for (int r=0;r<MAXX;r++){ 
			
			for (int c=0;c<MAXX;c++){
			
			if(config[r][c]==1){ 
			
			int xx=c+R;
			if(xx>MAXX)
			xx=xx-MAXX;
			
			int yy=r+R;
			if(yy>MAXX)
			yy=yy-MAXX;
				
			if (config[r][xx]==1 && config[yy][c]==1 && config[yy][xx]==1){ 
				
			SQ[R]++;
				
			    }
			 
			  }
		
			}		
		}
		
	}
	
  }
}

void TriangleVer() 
{
	if(Nt<=MAXX/2){         
	
	for (int R=0;R<Nt;R=R+2){ 
		
		for (int r=0;r<MAXX;r++){ 
			
			for (int c=0;c<MAXX;c++){
			
			if(config[r][c]==1){ 
			
			int xx;
		
			xx=c+((R/2)*sqrt(3))+1;  
			if(R==0)  
			xx=c+((R/2)*sqrt(3));
			
			
			
			if(xx>MAXX)
			xx=xx-MAXX;
			
			int gg=r+(R/2);
			if(gg>MAXX)
			gg=gg-MAXX;
			
			int yy=r+R;
			if(yy>MAXX)
			yy=yy-MAXX;
				
			if (config[yy][c]==1 && config[gg][xx]==1){ 
				
			TriVer[R]++;
			      }
			  }

			}		
		}
		cout<<TriVer[R]<<"***"<<endl;
	}
	
  }
}

void TriangleHor() 
{
	if(Nt<=MAXX/2){         
	
	for (int R=0;R<Nt;R=R+2){ 
		
		for (int r=0;r<MAXX;r++){ 
			
			for (int c=0;c<MAXX;c++){
			
			if(config[r][c]==1){ 
			
			int yy;
		
			yy=r+((R/2)*sqrt(3))+1;  
			if(R==0)   
			yy=r+((R/2)*sqrt(3));
			
			
			
			if(yy>MAXX)
			yy=yy-MAXX;
			
			int gg=c+(R/2);
			if(gg>MAXX)
			gg=gg-MAXX;
			
			int xx=c+R;
			if(xx>MAXX)
			xx=xx-MAXX;
				
			if (config[r][xx]==1 && config[yy][gg]==1){ 
				
			TriHor[R]++;
			      }
			  }

			}		
		}
		cout<<TriHor[R]<<"***"<<endl;
	}
	
  }
}



void HexagonVer() 
{
	if(Nt<=MAXX/2){          
	
	for (int R=0;R<Nt;R++){ 
		
		for (int r=0;r<MAXX;r++){ 
			
			for (int c=0;c<MAXX;c++){
			
			if(config[r][c]==1){ 
			
			
			float P2x=0;
			float P2y=0;
			float P3x=0;
			float P3y=0;
			float P4x=0;
			float P4y=0;
			float P5x=0;
			float P5y=0;
			float P6x=0;
			float P6y=0;
			
		    P2x=r+(sqrt(3)*0.5*R);
			P2y=c-(0.5*R);
			P3x=r+(sqrt(3)*0.5*R)+(sqrt(3)*0.5*R);
			P3y=c+(0.5*R)-(0.5*R);
			P4x=r+(sqrt(3)*0.5*R)+(sqrt(3)*0.5*R);
			P4y=c+(0.5*R)-(0.5*R)+R;
			P5x=r+(sqrt(3)*0.5*R);
			P5y=c+R+(0.5*R);
			P6x=r;
			P6y=c+R;
			
			P2x=ceil(P2x);
			P2y=ceil(P2y);
			P3x=ceil(P3x);
			P3y=ceil(P3y);
			P4x=ceil(P4x);
			P4y=ceil(P4y);
			P5x=ceil(P5x);
			P5y=ceil(P5y);
			P6x=ceil(P6x);
			P6y=ceil(P6y);
	
			
			if(P2x>MAXX)
			P2x=P2x-MAXX;
			if(P2y<0)
			P2y=P2y+MAXX;
			
			if(P3x>MAXX)
			P3x=P3x-MAXX;
			
			
			if(P4x>MAXX)
			P4x=P4x-MAXX;
			if(P4y>MAXX)
			P4y=P4y-MAXX;
			
			if(P5x>MAXX)
			P5x=P5x-MAXX;
			if(P5y>MAXX)
			P5y=P5y-MAXX;
			
		
			if(P6y>MAXX)
			P6y=P6y-MAXX;
			
		
				
			if (config[(int)P2x][(int)P2y]==1 && config[(int)P3x][(int)P3y]==1 && config[(int)P4x][(int)P4y]==1 && config[(int)P5x][(int)P5y]==1 && config[(int)P6x][(int)P6y]==1){ //confirm that if each square element is black or not
				
			HexaVer[R]++;
			      }
			  }

			}		
		}
		cout<<HexaVer[R]<<"***"<<endl;
	}
	
  }
}


void HexagonHor() 
{
	if(Nt<=MAXX/2){          
	
	for (int R=0;R<Nt;R++){   
		
		for (int r=0;r<MAXX;r++){  
			
			for (int c=0;c<MAXX;c++){
			
			if(config[r][c]==1){ 
			
			
			float P2x=0;
			float P2y=0;
			float P3x=0;
			float P3y=0;
			float P4x=0;
			float P4y=0;
			float P5x=0;
			float P5y=0;
			float P6x=0;
			float P6y=0;
			
		    P2x=r+R;
			P2y=c;
			P3x=r+R+(0.5*R);
			P3y=c+(sqrt(3)*0.5*R);
			P4x=r+R;
			P4y=c+(sqrt(3)*0.5*R);
			P5x=r;
			P5y=c+(sqrt(3)*R);;
			P6x=r-(0.5*R);
			P6y=c+(sqrt(3)*0.5*R);
			
			P2x=ceil(P2x);
			P2y=ceil(P2y);
			P3x=ceil(P3x);
			P3y=ceil(P3y);
			P4x=ceil(P4x);
			P4y=ceil(P4y);
			P5x=ceil(P5x);
			P5y=ceil(P5y);
			P6x=ceil(P6x);
			P6y=ceil(P6y);
	
			
			if(P2x>MAXX)
			P2x=P2x-MAXX;
		
			
			if(P3x>MAXX)
			P3x=P3x-MAXX;
			if(P3y>MAXX)
			P3y=P3y-MAXX;
			
			if(P4x>MAXX)
			P4x=P4x-MAXX;
			if(P4y>MAXX)
			P4y=P4y-MAXX;
			
			
			if(P5y>MAXX)
			P5y=P5y-MAXX;
			
		
			
			if(P2x<0)
			P2x=P2x+MAXX;
		    if(P6y>MAXX)
			P6y=P6y-MAXX;
				
			if (config[(int)P2x][(int)P2y]==1 && config[(int)P3x][(int)P3y]==1 && config[(int)P4x][(int)P4y]==1 && config[(int)P5x][(int)P5y]==1 && config[(int)P6x][(int)P6y]==1){ //confirm that if each square element is black or not
				
			HexaHor[R]++;
			      }
			  }

			}		
		}
		cout<<HexaHor[R]<<"***"<<endl;
	}
	
  }
}








void Octa() 
{
	if(Nt<=MAXX/2){         
	
	for (int R=0;R<Nt;R++){ 
		
		for (int r=0;r<MAXX;r++){  
			
			for (int c=0;c<MAXX;c++){
			
			if(config[r][c]==1){ 
			
			
			float P2x=0;
			float P2y=0;
			float P3x=0;
			float P3y=0;
			float P4x=0;
			float P4y=0;
			float P5x=0;
			float P5y=0;
			float P6x=0;
			float P6y=0;
			float P7x=0;
			float P7y=0;
			float P8x=0;
			float P8y=0;
			
		    P2x=r+(R/sqrt(2));
			P2y=c-(R/sqrt(2));
			P3x=r+(R/sqrt(2))+R;
			P3y=c-(R/sqrt(2));
			P4x=r+((2*R/sqrt(2))+R);
			P4y=c;
			P5x=r+((2*R/sqrt(2))+R);
			P5y=c+R;
			P6x=r+(R/sqrt(2))+R;
			P6y=c+R+(R/sqrt(2));
			P7x=r+(R/sqrt(2));
			P7y=c+R+(R/sqrt(2));
			P8x=r;
			P8y=c+R;
			
			P2x=ceil(P2x);
			P2y=ceil(P2y);
			P3x=ceil(P3x);
			P3y=ceil(P3y);
			P4x=ceil(P4x);
			P4y=ceil(P4y);
			P5x=ceil(P5x);
			P5y=ceil(P5y);
			P6x=ceil(P6x);
			P6y=ceil(P6y);
			P7x=ceil(P7x);
			P7y=ceil(P7y);
			P8x=ceil(P8x);
			P8y=ceil(P8y);
	
			
			if(P2x>MAXX)
			P2x=P2x-MAXX;
			if(P2y<0)
			P2y=P2y+MAXX;
		    
			
			if(P3x>MAXX)
			P3x=P3x-MAXX;
			if(P3y<0)
			P3y=P3y+MAXX;
			
			if(P4x>MAXX)
			P4x=P4x-MAXX;
			
			
			
			if(P5x>MAXX)
			P5x=P5x-MAXX;
			if(P5y>MAXX)
			P5y=P5y-MAXX;
			
		
			
		    if(P6x>MAXX)
			P6x=P6x-MAXX;
			if(P6y>MAXX)
			P6y=P6y-MAXX;
			
			if(P7x>MAXX)
			P7x=P7x-MAXX;
			if(P7y>MAXX)
			P7y=P7y-MAXX;
			
			
			if(P8y>MAXX)
			P8y=P8y-MAXX;
			
				
			if (config[(int)P2x][(int)P2y]==1 && config[(int)P3x][(int)P3y]==1 && config[(int)P4x][(int)P4y]==1 && config[(int)P5x][(int)P5y]==1 && config[(int)P6x][(int)P6y]&& config[(int)P7x][(int)P7y]&& config[(int)P8x][(int)P8y]==1){ //confirm that if each square element is black or not
				
			Octagon[R]++;
			      }
			  }

			}		
		}
		cout<<Octagon[R]<<"***"<<endl;
	}
	
  }
}




void Arbitrary() 
{
	if(Nt<=MAXX/2){          
	
	for (int R=0;R<Nt;R++){  
		
		for (int r=0;r<MAXX;r++){ 
			
			for (int c=0;c<MAXX;c++){
			
			
			float ArbiX[Nside];
			float ArbiY[Nside];
			
			double Thta=(360.0/Nside);
			Thta=Thta/180*PI;
			double Radius=2*sin(Thta/2)/R;
			int Summ=0;
			
			for (int i=0;i<Nside;i++){
			ArbiX[i]=0;
			ArbiY[i]=0;
			
			Thta=Thta*i;
			if (0.5*PI<Thta<PI)
			Thta=PI-Thta;
			if (PI<Thta<1.5*PI)
			Thta=PI-180;
			if (1.5*PI<Thta<2*PI)
			Thta=2*PI-Thta;
			
			ArbiX[i]=Radius*cos(Thta);
			ArbiY[i]=Radius*sin(Thta);
			ArbiX[i]=ceil(ArbiX[i]);
			ArbiY[i]=ceil(ArbiY[i]);
			
			
			if (ArbiX[i]>MAXX)
			ArbiX[i]=ArbiX[i]-MAXX;	
			if(ArbiX[i]<0)
			ArbiX[i]=ArbiX[i]+MAXX;
			
			if (ArbiY[i]>MAXX)
			ArbiY[i]=ArbiY[i]-MAXX;	
			if(ArbiY[i]<0)
			ArbiY[i]=ArbiY[i]+MAXX;
			
			if (config[(int)ArbiX[i]][(int)ArbiY[i]]==1)
	        Summ=Summ+1;	
			}
			
		    
		    if (Summ==Nside)
		    Arbi[R]++;
		    
			  

			}		
		}
		cout<<Arbi[R]<<"***"<<endl;
	}
	
  }
}




main()
{
  double S2[Nt];  
  double ST2[Nt]; 
 
  double L[Nt];
  double LT[Nt];  

  int SS2[Nt]; 
  int SL[Nt];


  for(int i=0; i<Nt; i++)
    {
      S2[i] = 0;
      ST2[i] = 0;
      SS2[i] = 0;

      L[i] = 0;
      LT[i] = 0;
      SL[i] = 0;
    }

  for(int i=0; i<MAXX; i++)
    for(int j=0; j<Nt; j++)
      {
	lineS2[i][j] = 0;
	columeS2[i][j] = 0;

	N2H[i][j] = 0;
	N2V[i][j] = 0;
      }

	// we initilize all the parameters.




  read_config();

 
  cout<<"sampling S_2 now..."<<endl;


   for(int i=0; i<MAXX; i++)
	{
	  sampleS2line(i);
	  sampleS2colume(i);


     for(int r=0; r<Nt; r++)
       {
	    SS2[r] = SS2[r] + lineS2[i][r] + columeS2[i][r];
	   }
    }

 for(int r=0; r<Nt; r++)
    {
      S2[r] = (double) SS2[r]/(double)(2*MAXX*MAXX); 

      printf("%d\t%f\n", r, S2[r]);
    }

  printf("**********************************************\n");

  FILE* file = fopen("sobjS2.txt", "w");  
  for(int r=0; r<Nt; r++)
    {
          fprintf(file, "%d\t%f\n", r, S2[r]);  
    }
  fclose(file);





  //now we sample L for the first time...
  cout<<"sampling L now..."<<endl;


  for(int r=0; r<Nt; r++) 
    {
      for(int i=0; i<MAXX; i++)
	{
	  sample_horizontal(i); 
	  sample_vertical(i);   

	  SL[r] = SL[r] + N2H[i][r] + N2V[i][r];
	}

      L[r] = (double) SL[r]/(double)(2*MAXX*MAXX);

      printf("%d\t%f\n", r, L[r]);

    }

   file = fopen("sobjL.txt", "w");
   for(int r=0; r<Nt; r++)
    {
          fprintf(file, "%d\t%f\n", r, L[r]);
    }
  fclose(file);

  printf("******************************************\n");
  
  
  
   cout<<"sampling SQ now..."<<endl;//@@@@
   
   
 
  double total=0;
  double SQF[Nt];
  
  
  // initial the value
  
   for(int i=0; i<Nt; i++)
    {
      SQ[i] = 0;
      SQF[i]=0;
    }


  // calculate the # of the square range
  
  squrefunction();
  /*
  for(int i=0;i<=Nt;i++){
  	
  total=total+SQ[i];
  }
   
 for(int r=0; r<Nt; r++)
    {
      
      printf("%d\t%f\n", r, SQ[r]);
    }    
*/
 for(int r=0; r<Nt; r++)
    {
      SQF[r] = SQ[r] /(double)(MAXX*MAXX); 

      printf("%d\t%f\n", r, SQF[r]);
    }

  printf("**********************************************\n");

  file = fopen("SobjSQF.txt", "w");  
  for(int r=0; r<Nt; r++)
    {
          fprintf(file, "%d\t%f\n", r, SQF[r]); 
    }
  fclose(file);
  
 

  printf("******************************************\n");

  
  
  
  cout<<"sampling Triangle-Vertical function now..."<<endl;
   
   
 

  double TriVerF[Nt];
  
  
  // initial the value
  
   for(int i=0; i<Nt; i++)
    {
      TriVer[i] = 0;
      TriVerF[i]=0;
    }


  // calculate the # of the triangle(Vertical) range
  
  TriangleVer();
 
 
 for(int r=0; r<Nt; r++)
    {
      TriVerF[r] = TriVer[r] /(double)(MAXX*MAXX); 

      printf("%d\t%f\n", r, TriVerF[r]);
    }

  printf("**********************************************\n");

  file = fopen("SobjTriV.txt", "w");  
  for(int r=0; r<Nt; r++)
    {
          fprintf(file, "%d\t%f\n", r, TriVerF[r]);  
    }
  fclose(file);
  
    file = fopen("TriVDra.xls", "w");  
  for(int r=0; r<Nt; r=r+2)
    {
          fprintf(file, "%d\t%f\n", r, TriVerF[r]);  
    }
  fclose(file);
  
 

  printf("******************************************\n");
  
  




  cout<<"sampling Triangle-Horizontal function now..."<<endl;
   
   
 

  double TriHorF[Nt];
  
  
  // initial the value
  
   for(int i=0; i<Nt; i++)
    {
      TriHor[i] = 0;
      TriHorF[i]=0;
    }


  // calculate the # of the triangle(horizon) range
  
  TriangleHor();
 
 
 for(int r=0; r<Nt; r++)
    {
      TriHorF[r] = TriHor[r] /(double)(MAXX*MAXX); 

      printf("%d\t%f\n", r, TriHorF[r]);
    }

  printf("**********************************************\n");

  file = fopen("SobjTriH.txt", "w");  
  for(int r=0; r<Nt; r++)
    {
          fprintf(file, "%d\t%f\n", r, TriHorF[r]);  
    }
  fclose(file);
  
    file = fopen("TriHDra.xls", "w");  
  for(int r=0; r<Nt; r=r+2)
    {
          fprintf(file, "%d\t%f\n", r, TriHorF[r]);  
    }
  fclose(file);
  
 

  printf("******************************************\n");





cout<<"sampling vertical Hexagon function now..."<<endl;
   
  double HexaVerF[Nt];
  
  
  // initial the value
  
   for(int i=0; i<Nt; i++)
    {
      HexaVer[i] = 0;
      HexaVerF[i]=0;
    }
  
  HexagonVer();
 

 for(int r=0; r<Nt; r++)
    {
      HexaVerF[r] = HexaVer[r] /(double)(MAXX*MAXX); 

      printf("%d\t%f\n", r, HexaVerF[r]);
    }

  printf("**********************************************\n");

  file = fopen("SobjHesaVer.txt", "w");  
  for(int r=0; r<Nt; r++)
    {
          fprintf(file, "%d\t%f\n", r, HexaVerF[r]); 
    }
  fclose(file);
  
  printf("******************************************\n");
  
  
  
  
  
  cout<<"sampling Horizontal Hexagon function now..."<<endl;
   
  double HexaHorF[Nt];
  
  
  // initial the value
  
   for(int i=0; i<Nt; i++)
    {
      HexaHor[i] = 0;
      HexaHorF[i]=0;
    }

  
  HexagonHor();
 

 for(int r=0; r<Nt; r++)
    {
      HexaHorF[r] = HexaHor[r] /(double)(MAXX*MAXX); 

      printf("%d\t%f\n", r, HexaHorF[r]);
    }

  printf("**********************************************\n");

  file = fopen("SobjHexaHor.txt", "w");  
  for(int r=0; r<Nt; r++)
    {
          fprintf(file, "%d\t%f\n", r, HexaHorF[r]);  
  fclose(file);
  

  
 

  printf("******************************************\n");
  
  
  
    cout<<"sampling Octagon function now..."<<endl;
   
  double OctagonF[Nt];
  
  
  // initial the value
  
   for(int i=0; i<Nt; i++)
    {
      Octagon[i] = 0;
    
    }
  // calculate the # of the hexagon(vertical) range
  
  Octa();
 

 for(int r=0; r<Nt; r++)
    {
      OctagonF[r] = Octagon[r] /(double)(MAXX*MAXX); 

      printf("%d\t%f\n", r, OctagonF[r]);
    }

  printf("**********************************************\n");

  file = fopen("SobjOctagon.txt", "w"); 
  for(int r=0; r<Nt; r++)
    {
          fprintf(file, "%d\t%f\n", r, OctagonF[r]); 
    }
  fclose(file);
  
  printf("******************************************\n");
  
  


  
return 0;
}
}

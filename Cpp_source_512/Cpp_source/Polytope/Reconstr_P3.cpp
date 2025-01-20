//*******************************************************
// P3(re)construction using orthogonal sampling method
//*******************************************************

//updated Sep, 16th, 2019

//modified date: 


 

using namespace std;

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <time.h>


#define MAXX 20  
#define MAXY 5000
#define Nt 10
 
int NP;
double f1;
double f2;

int flag_iconfig; 

int indexi; int indexj; int indexm; int indexn; 

int config[MAXX][MAXX];
int best_config[MAXX][MAXX];


double SQ[Nt]; 
double objP3H[Nt];
double P3Hb[Nt];


//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//The cooling schedule ...

int Nevl = 50000; 

double alpha = 0.88; 
double beta = 0.85;

int TN = 0; 


double T = 0.00005; 

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

void read_parameter()
{
  cout<<"Now, Let's input the parameters to start P3H reconstruction."<<endl<<endl<<endl;
  
  cout<<"Reading parameters for annealing reconstruction from standard input"<<endl<<endl;

  cout<<"Init config flag flag_iconfig =    (0 for random sturcture and other numbers for input structure)"; cin>>flag_iconfig; cout<<endl;

  cout<<"Number of black pixels: NP = "; cin>>NP; cout<<endl;

  //now computing the volume fraction...
  f1 = (double)NP/(double)(MAXX*MAXX*MAXX);
  f2 = 1.0 - f1;

  //now for the cooling schedule
  cout<<"Starint temp T0 = "; cin>>T; cout<<endl;
  cout<<"Decreasing ratio: alpha = "; cin>>alpha; cout<<endl;
  cout<<"Number of decreasing T stages: TN = "; cin>>TN; cout<<endl;
  cout<<"Number of pxiel move per stage: Nevl = "; cin>>Nevl; cout<<endl;


  
}

void get_obj()
{
  FILE* fp;
  
  int ind;
  float value;
  double fr = f1;

  
  //For P3H...

 if((fp = fopen("SobjTriH.txt","r"))==NULL)
    {
      printf("Can not open objective file for P3H! Abort!\n");
      exit(1);
    }



  fscanf(fp, "%d", &ind);
  fscanf(fp, "%f", &value);

 
  if((1.0-value)<0.001)
    {
      objP3H[0] = fr*(1-fr)*value + fr*fr;
      for(int i=1; i<Nt; i++)
	{
           fscanf(fp, "%d", &ind);
           fscanf(fp, "%f", &value);

	   objP3H[i] = fr*(1-fr)*value + fr*fr;
	}

      
    }
  else
    {
      objP3H[0] = value;
      for(int i=1; i<Nt; i++)
	{
           fscanf(fp, "%d", &ind);
           fscanf(fp, "%f", &value);

	   objP3H[i] = value;
	}

      
    }

  fclose(fp);

  //print out the read-in ...

  fp = fopen("objP3H.txt","w");
   for(int r=0; r<Nt; r++)
     fprintf(fp,"%d \t %f\n", r, objP3H[r]);
  fclose(fp);  


}

void read_config()
{
  for(int i=0; i<MAXX; i++)
    for(int j=0; j<MAXX; j++)
      config[i][j] = 0;


  FILE* fp;

  if((fp=fopen("config_OL.txt","r"))==NULL)
    {
      printf("No config_OL.txt is found! Abort!\n");
      exit(1);
    }

  int tempx;
  int tempy;

  for(int i=0; i<NP; i++)
    {

      fscanf(fp, "%d", &tempx);
      fscanf(fp, "%d", &tempy);

      config[tempx][tempy] = 1;
    }

  fclose(fp);
}



void init_config()
{
  for(int i=0; i<MAXX; i++)
    for(int j=0; j<MAXX; j++)
      {
        config[i][j] = 0;
      }


  for(int i=0; i<NP; i++)
    {
      int m = rand()%MAXX;
      int n = rand()%MAXX;

      while(config[m][n]==1)
	{
	  m = rand()%MAXX;
	  n = rand()%MAXX;
	}

      config[m][n] = 1;
    }

  //****************************
  for(int i=0; i<MAXX; i++)
    for(int j=0; j<MAXX; j++)
      best_config[i][j] = 0;

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
				
			SQ[R]++;
			      }
			  }

			}		
		}
	
	}
	
  }
}


void change_config()
{
  int i, j, m, n;
  int lim = 0;

  //fist we change the lines
 
  do{   i = rand()%MAXX;
        m = rand()%MAXX; 
        j = rand()%MAXX; 
        n = rand()%MAXX; 
        lim++;
    }while(config[i][j] == config[m][n] && lim < 100);

  int temp;

  temp = config[i][j];
  config[i][j] = config[m][n];
  config[m][n] = temp;

  indexi = i;
  indexj = j;
  indexm = m;
  indexn = n;

}


void resume_config()
{
  int temp;
  //first we resume the config
  temp = config[indexi][indexj];
  config[indexi][indexj] = config[indexm][indexn];
  config[indexm][indexn] = temp;

}


double energy(double S[Nt])
{
  double E=0;

  for(int i=1; i<Nt; i++)
    {
      E = E + (S[i] - objP3H[i])*(S[i] - objP3H[i]);  
	  
    }
  
  
  return E;
}


double d_energy(double P3H[Nt], double PT3H[Nt])    
{
  double d_E = 0;
  d_E = energy(PT3H) - energy(P3H);
  return d_E;
}

double PE(double dE, double T) 
{
  if(dE > 0) return exp(-dE/T);
  else return 1;
}


main()
{
  
  
  

  double P3H[Nt]; 
  double PT3H[Nt];

  int SP3H[Nt];
 


  double energyb = MAXY; 
  double energyt = 0; 


  for(int i=0; i<Nt; i++)
    {
      P3H[i] = 0;
      PT3H[i] = 0;
      SP3H[i] = 0;
     
    }




  get_obj();


  read_parameter();
  
  if(flag_iconfig == 0)
    init_config();
  else
    read_config();
 


    
    
    // initial the value
  
   for(int i=0; i<Nt; i++)
    {
      SQ[i] = 0;
      
    }
    
    
 
   TriangleHor();
	
	cout<<"The P3H for the initail structure"<<endl; 
	
  for(int r=0; r<Nt; r++)
    {
    

      P3H[r] = (double) SQ[r]/(double)(MAXX*MAXX);

      printf("%d\t%f\n", r, P3H[r]);

    }

  printf("**********************************************\n");

  FILE* file = fopen("TP3H.txt", "w");  // create TP4.txt 
  for(int r=0; r<Nt; r++)
    {
          fprintf(file, "%d\t%f\n", r, P3H[r]);
    }
  fclose(file);
  
  FILE* fp = fopen("E.txt","w");
  fclose(fp);

      //simulated annealing procedure to evlove the system
      //*****************************************************************
      //*****************************************************************
      
      
     cout<< "Starting annealing procedure"<<endl;

      for(int q=0; q<TN; q++)  
	{
	  T = alpha*T;

	  for(int i=0; i< Nevl; i++)  
	    {
	      change_config();
	  

	     for(int b=0; b<Nt; b++)
         {
          SQ[b] = 0;
         }


         TriangleHor(); 



	      //Now we compute the P3H for the new configuration...
	      for(int r=0; r<Nt; r++)
		{

                  //the following method only consider the changes.. 
                  //************************************************

		 
		  PT3H[r] = (double)SQ[r]/(double)(MAXX*MAXX); 
                  //************************************************

	
		}

	      //Monte Carlo steps...

	      double P = double (rand() % MAXY)/(double) MAXY;

	      
	      if( P > PE(d_energy(P3H, PT3H), T))  
		{
		  resume_config();
		  //this just resumes the 'configuration', still need to resume P3H...
		 
                 
		} 

	      else 
		{
		  for(int r=0; r<Nt; r++)
		    {
		      P3H[r] = PT3H[r];  
		     
		    }
		}


	      //compare and record the best energy and configuration...
	      energyt = energy(P3H);
	     
	      if(energyt < energyb)  
		{
		  energyb = energyt;

		  for(int i=0; i<MAXX; i++)
		    for(int j=0; j<MAXX; j++)
		      {
			best_config[i][j] = config[i][j];
		      }

                  for(int it = 0; it<Nt; it++) 
		    {
		    
		      P3Hb[it] = P3H[it];
		    }
		}
	      
	      

	    }

        
	  printf("%d th change of temperature has finished... \n",q+1 );

    
       fp = fopen("Fconfig.txt","w");
       for(int it=0; it<MAXX; it++)
	 for(int jt=0; jt<MAXX; jt++)
	   {
	     if(config[it][jt]==1) 
	       fprintf(fp, "%d\t%d\n", it, jt);
	   }
       fclose(fp);

    
    
       fp = fopen("P3H.txt", "w");
       for(int r=0; r<Nt; r++)
	 {
              fprintf(fp, "%d \t %f \n", r, P3Hb[r]);
	 }
       fclose(fp);

       fp = fopen("E.txt","a");
       fprintf(fp, "%1.12f \n", energyb);
       fclose(fp);      

       printf("energy = %f  \n", energyb);
	  printf("*************************************************\n");

	}

      //*****************************************************************
      //*****************************************************************
      //this is the end of simulated annealing


    

  //this is the end of the codes...
  
  


}

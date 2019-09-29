#include <stdio.h>
#include <stdlib.h>

extern int SOMA(int aa, int bb);
extern int SOMA_V(int *a, int n);
extern void somaVFSIMDFEX1A(float *P, float *Q, float *R, int n);


int main() {

	// Q1

	int a = 5;
	int b = 10;
	int ca = 0;
    ca =  SOMA( a, b);
    //printf("A soma � %d\n", ca);


    // Q2
	
	int dim = 5;
	int v[] = { 3, -1, 8, 0, -3};
	int res;
	res = SOMA_V(v, dim);
	//printf("Soma dos elementos = %d\n", res);
	
    // Q3

	float PFSIMDFEX1A[] = { 3.4, 5.3, -1.0, -2.1, 3.4, 5.3, -1.0, -2.1, 3.4, 5.3, -1.0, -2.1, 3.4, 5.3, -1.0, -2.1};
	float QFSIMDFEX1A[] = { 1.4, 1.3, 1.0, 1.1, 1.4, 1.3, 1.0, 1.1, 1.4, 1.3, 1.0, 1.1, 1.4, 1.3, 1.0, 1.1};
	float RFSIMDFEX1A[] = { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
	int NFSIMDFEX1A = 16;
	somaVFSIMDFEX1A(PFSIMDFEX1A, QFSIMDFEX1A, RFSIMDFEX1A, NFSIMDFEX1A );
	    for(int i = 0; i < 16; i++) {
	    	 	        //printf("R[%d]= %f\n",i, RFSIMDFEX1A[i]);
	    }

return 0;

}

//https://github.com/sosy-lab/sv-benchmarks/blob/master/c/array-examples/standard_running-1.c


extern void abort(void);
#include <assert.h>
void reach_error() { assert(0); }
void __VERIFIER_assert(int cond) { if(!(cond)) { ERROR: {reach_error();abort();} } }
extern int __VERIFIER_nondet_int();

#define N 5

int main ( ) {
  int a[N];
  int b[N]; 
  int i = 0;
	
	for(i = 0; i< N; i++) 
	{ 
	    a[i] = __VERIFIER_nondet_int();
	}
	
	i=0;
  while ( i < N ) {
    if ( a[i] >= 0 ) b[i] = 1;
    else b[i] = 0;
    i = i + 1;
  }
  int f = 1;
  i = 0;
  while ( i < N ) {
    if ( a[i] >= 0 && !b[i] ) f = 0;
    if ( a[i] < 0 && !b[i] ) f = 0;
    i = i + 1;
  }
  __VERIFIER_assert ( f ); 
  return 0;
}


int __VERIFIER_nondet_int() {
  int a = getchar() % 5;
  int b = getchar() % 5;

  return b-a;
}
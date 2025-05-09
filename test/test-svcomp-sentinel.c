// https://github.com/sosy-lab/sv-benchmarks/blob/master/c/array-examples/standard_sentinel-1.c

extern void abort(void);
#include <assert.h>
void reach_error() { assert(0); }
void __VERIFIER_assert(int cond) { if(!(cond)) { ERROR: {reach_error();abort();} } }
extern int __VERIFIER_nondet_int();

#define N 5

int main ( ) {
  int a[N];
  int marker = __VERIFIER_nondet_int();
  int pos = __VERIFIER_nondet_int();
	
	for(int i = 0; i < N; i++) 
	{
	  a[i] = __VERIFIER_nondet_int();
	}
	
  if ( pos >= 0 && pos < N ) {
    a[ pos ] = marker;

    int i = 0;
    while( a[ i ] != marker ) {
      i = i + 1;
    }
   
    __VERIFIER_assert(  i <= pos  );
  }
  return 0;
}

int __VERIFIER_nondet_int() {
  int a = getchar() % 5;
  int b = getchar() % 5;

  return b-a;
}
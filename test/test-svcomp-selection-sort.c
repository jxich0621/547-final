//https://github.com/sosy-lab/sv-benchmarks/blob/master/c/array-examples/sorting_selectionsort_ground-1.c

extern void abort(void);
#include <assert.h>
void reach_error() { assert(0); }
void __VERIFIER_assert(int cond) { if(!(cond)) { ERROR: {reach_error();abort();} } }
extern int __VERIFIER_nondet_int();

#define N 10

int main( ) {
  int a[ N ];
  int i = 0;
  int x;
  int y;
	
	for(int i = 0; i < 10; i++) 
	{
	    a[i] = __VERIFIER_nondet_int();
	}
	
	i = 0;
  while ( i < N ) {
    int k = i + 1;
    int s = i;
    while ( k < N ) {
      if ( a[k] < a[s] ) {
        s = k;
      }
      k = k+1;
    }
    if ( s != i ) {
      int tmp = a[s];
      a[s] = a[i];
      a[i] = tmp;
    }
    
    for ( x = 0 ; x < i ; x++ ) {
      for ( y = x + 1 ; y < i ; y++ ) {
        __VERIFIER_assert(  a[x] <= a[y]  );
      }
    }
    for ( x = 0 ; x < N ; x++ ) {
      __VERIFIER_assert(  a[x] >= a[i]  );
    }
    
    i = i+1;
  }
    
  for ( x = 0 ; x < N ; x++ ) {
    for ( y = x + 1 ; y < N ; y++ ) {
      __VERIFIER_assert(  a[x] <= a[y]  );
    }
  }
  return 0;
}


int __VERIFIER_nondet_int() {
    int a = getchar() % 5;
    int b = getchar() % 5;
  
    return b-a;
  }
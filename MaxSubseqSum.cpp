#include <iostream>
using namespace std;

int MaxSubseqSum(int A[], int N);

int main() {
	int N;
	cin >> N;
	int A[N];
	for (int i = 0; i < N; i++) {
		cin >> A[i];
	}
	
	MaxSubseqSum(A, N);
	
	return 0;
} 

int MaxSubseqSum(int A[], int N) {
	int start, Start, Stop, ThisSum, MaxSum;
	start = Start = Stop = ThisSum = MaxSum = 0;
	
	for (int i = 0; i < N; i++) {
		ThisSum = ThisSum + A[i];
		if (ThisSum > MaxSum) {
			MaxSum = ThisSum;
			Stop = i;
			Start = start;
		} else if (ThisSum < 0) {
			ThisSum = 0;
			start = i + 1;
		}		
	}
	
	cout << MaxSum << ' ' << Start << ' ' << Stop << endl;
	
	return MaxSum;
}

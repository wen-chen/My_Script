#include <iostream>
#include <ctime>
using namespace std;

clock_t start, stop;
/* clock_t是clock()函数返回的变量类型 */

double duration;

int main() {
	start = clock();
    //这里写要测试运行时间代码    
	stop = clock();
	duration = ((double) (stop - start)) / CLK_TCK;
	cout << duration;
} 
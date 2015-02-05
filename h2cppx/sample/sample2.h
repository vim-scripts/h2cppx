#include <vector>
#include <string>

#define DEF_1 1
#define OS_NAME "Linux"

using namespace std;

int friend_meth();

extern int ext_meth();

class SampleClass:public Test
{
public:
    typedef int MyTypedef;
    SampleClass();

    SampleClass(double a);

    explict SampleClass(int t=10);

    char f1(int a) const;
    bool f2(float a);
    int f3(const unsigned char a);
    long f4(int a) const ;
    float f5(int a);
    double f6(int a);
    std::string f7(int a);
    const unsigned int f8(int a);

};


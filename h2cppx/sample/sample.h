#include <vector>
#include <string>

#define DEF_1 1
#define OS_NAME "Linux"

using namespace std;

int friend_meth();

extern int ext_meth();

class SampleClass
{
public:
    TEST_MACRO(X);

    typedef int MyTypedef;
    SampleClass();

    SampleClass(double a);

    explict SampleClass(int t=10);

    explict SampleClass(float t);

    SampleClass(int a, int b=5, int c=6);

    ~SampleClass();

    bool operator<(SampleClass &rhs);

    /*!
     * Method 1
     */
    std::string meth1();

    ///
    /// Method 2 description
    ///
    /// @param v1 Variable 1
    ///
    int meth2(int v1);

    /**
     * Method 3 description
     *
     * \param v1 Variable 1
     * \param v2 Variable 2
     */
    void meth3(const string & v1, vector<string> & v2);

    /**********************************
     * Method 4 description
     *
     * @return Return value
     *********************************/
    virtual unsigned int vmeth1();

    virtual unsigned int vmeth2() = 0;

    const unsigned int vmeth3() const;

    friend int friend_meth();

private:
    void * meth5(){return NULL};

    inline float meth6() { return 0.0f; }

    string prop2;

    static const int prop3;
    const static int prop4;

    /// prop1 description
    static std::string prop1;
    //! prop5 description
    static int prop5;

    static MyTypedef prop6;
};

inline SampleClass::meth2(int v1) {
}

namespace Alpha
{
    class AlphaClass
    {
    public:
        AlphaClass();

    private:
        void alphaMethod();

        string alphaString;

        static string s_alphaString;
    };

    namespace Omega
    {
        class OmegaClass
        {
        public:
            OmegaClass();

            string omegaString;

            int f2(int f);
        };
    };
}

int sampleFreeFunction(int i)
{
	return i + 1;
}

int anotherFreeFunction(void);


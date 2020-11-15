#include "MyOtherClass.h"
#include <iostream>
#define Pi_Value 3.14

using std::cout;
using std::endl;

enum My_Enum{
    First = 1,
    second = 2
}

namespace MyNamespace_first{
    int bVar = 3;
    const double const_var_in_Namespace = 3;
    void bar(){ std::cout << "some text" << std::endl; }
}

template<typename t, typename v__>
class my_class : public my_other_class{
public:
    int* foo(my_other_class &Other){
        not_existing_func();
        secondVar = const_Class_Var
        return some_ClassField;
    }

    void change_parent_member(int Value){
        other_class_Var = Value;
    }

    v__ T1;
    t T2;
private:
    int* some_ClassField = new int(0);
    int secondVar = MyNamespace_first::bVar;
    int c,d = 6,e;
    const int const_Class_Var = 6;
    my_other_class m;
}

void global__Func(int a){}

my_struct create_My_struct(int a){
    my_struct m;
    m.Something = 5;
    return m;
}
int main(int &Args, char**Argv){
    my_class<int, double> *A = new my_class<int, double>;
    A->change_parent_member(6)
    A->other_class_Var = 8;
    my_other_class &Other;
    (*A).foo(Other);
    int x = My_Enum::second;
    int y = OtherNamespace::one;
    auto it = std::find_if()
    my_other_class m;
    const double double_Const_Var = m.foo_F(1.3)
    my_struct m = create_My_struct(5);
    return 0;
}
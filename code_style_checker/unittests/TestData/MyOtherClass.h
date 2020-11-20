#include <string>

namespace OtherNamespace{
    const int one;
}

enum other_Enum{
    otherOne = 1,
    otherTwo = 2
}
//my struct which                   have two fields. First is bit     field and second         is int field Something. Some    text for large comment. It should be split by some small comments. The end.

struct my_struct{
    int BitField : 1;
    int Something = 3;
}

/*my_other_class which have one field. It is field with value 1. Some text for large comment. It should be split by some small comments. The end.
And some text, some some some comment comment comment comment comment comment comment comment comment comment comment comment comment comment
comment comment comment comment comment comment comment comment comment comment comment comment comment comment comment comment
*/

class my_other_class{
public:
    int other_class_Var = 1;
    void foo_F(double Func_Param){
        return static_cast<double>(Func_Param)
    }
}

int print_global(std::string text){
    std::pretty_print(text)
}
如何编写模板文件来控制代码的生成格式
====================================

[TOC]

模板文件的组成
--------------
模板文件为yaml格式,使用了python的Cheetah模板库进行具体配置解析,
配置项和配置说明如下:

* DOXYGEN : {Yes | No }  //是否添加头文件的doxygen注释(如果存在)

* VARIABLE_INTERVAL : 2 //相邻变量定义的空行数,值为数值

* FUNCTION_INTERVAL : 2 //相邻函数定义的空行数,值为数值

* VARIABLE : "" //变量定义生成格式,值为字符串

* FUNCTION : "" //函数定义生成格式,值为字符串

**以下皆为可选项**

* VARIABLE_START : ""   //变量定义开始处添加的描述字符串 

* VARIABLE_END   : ""   //变量定义结束处添加的描述字符串

* FUNCTION_START : ""   //函数定义开始处添加的描述字符串

* FUNCTION_END   : ""   //函数定义结束处添加的描述字符串

* CLASS_START    : ""   //类定义开始处添加的描述字符串

* CLASS_END      : ""   //类定义结束处添加的描述字符串

* HEADER_START   : ""   //头文件开始处添加的描述字符串

* HEADER_END     : ""   //头文件结束处添加的描述字符串

模板格式的编写
--------------
对于大部分配置项,都会有一个配置项环境变量存在,可以通过环境变量的属性来定制
代码格式的生成,以下列出每一个项所拥有的配置环境:

* VARIABLE : $variable
* FUNCTION : $function
* VARIABLE_START : $variable
* VARIABLE_END   : $variable
* FUNCTION_START : $function
* FUNCTION_END   : $function
* CLASS_START    : $class
* CLASS_END      : $class
* HEADER_START   : $header
* HEADER_END     : $header

对于每个不同的环境变量,主要有以下属性可供使用:
$variable:
* access : 变量的入口权限(如果存在)
* type   : 变量的完整类型
* raw_type:变量的原始类型
* typedef: 如果是typedef后的类型,会指出类型别名的作用域
* doxygen: 变量的doxygen注释(如果存在)
* name   : 变量名
* namespace: 变量所在的名字空间
* owner  : 变量所属的类名
* constant: 变量是否是常量
* default_value : 变量的默认值(如果存在)
* path   : 变量的完整作用域名(包括名字空间和类名)
* sign_type : 完整的变量类型签名
* sign_name : 完整的变量名字签名

>有了这些信息,通过以下方式配置VARIABLE项即可简单定制变量生成的格式,例如:
VARIABLE : "$variable.sign_type $variable.sign_name;" 
如类A里有个变量static int var,此格式将会生成 int A::var;的变量定义

$function:
* access : 函数的入口权限(如果存在)
* name   : 函数名
* return_type: 函数返回值类型
* namespace: 函数所属名字空间
* parameters : 函数的参数列表,列表里每项是一个变量类型,拥有变量环境的属性
* const   : 函数是否是const函数
* path    : 函数的完整作用域名(包括名字空间和类名)
* operator: 函数是否是操作符重载函数
* virtual : 函数是否是虚函数
* explict : 函数是否是explict函数
* constructor: 函数是否是构造函数
* destructor : 函数是否是析构函数
* doxygen: 变量的doxygen注释(如果存在)
* sign_name : 函数名的完整签名

$class:
* inherits : 类的基类(如果存在)
* name : 类名
* namespace: 类所在名字空间
* doxygen: 类的doxygen注释(如果存在)

$header:
* filename : 头文件名(绝对路径)
* includes : 头文件所包含的头文件

**具体可参考template目录下的模板文件来编写**

**cheetah提供更细致的流控制能力,详细的模板语法可以参考cheetah用户手册**

[Cheetah User's Guide](http://pythonhosted.org//Cheetah/users_guide/index.html)

[Cheetah Flow Control](http://pythonhosted.org//Cheetah/users_guide/flowControl.html)


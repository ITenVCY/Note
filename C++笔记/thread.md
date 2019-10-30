## C++ 多线程

#### thread  探究

##### 网上文章

https://www.shiyanlou.com/library/Cpp-Concurrency-In-Action/content/chapter1/1.2-chinese

> 详细讲解了C++中并发和多线程的知识(包括基础概念的讲解), 目前很多表达看不懂

##### 学习视频

https://www.bilibili.com/video/av39171692?p=4

> 对C++11新增加的thread进行详细的解释, 学习目的通过学习完毕, 看是否`pthread`中是否有类似这种新特性

###### thread和thread.deatch() 分离

```C++
#include <iostream>
#include <thread>

using namespace std;

class A
{
private:
	int m;
public:
	A(int c) :m(c) 
	{
		cout << "id = " << this_thread::get_id() << "A(int c)" << endl;
	}
	~A()
	{
		cout << "id = " << this_thread::get_id() << "	~A()" << endl;
	}
	A(const A &a) :m(a.m)
	{
		cout << "id = " << this_thread::get_id() << "	A(const A &a)" << endl;
	}
    void operator()(int mun) //直接用对象作为线程的起始函数,
    {
       	cout << "id = " << this_thread::get_id() << "	operator()(int mun)" << endl;
    }
    void thread(int mun)
    {
        cout << "id = " << this_thread::get_id() << "	thread(int mun)" << endl;
    }
};


void myprint(A a)
{
	cout << "子线程id = " << this_thread::get_id() << "myprint(A &a)" << endl;
}

int main()
{
	cout << "主线程id = " << this_thread::get_id() << endl;
	//A a(2);
	int a = 4;

	thread mythread(myprint,a);
	mythread.join(); 	
    
    A b(2);
    thread mythread2(&A::thread,b,12); //类中别的函数作为线程的启动函数,调用拷贝构造函数
    
    A c(3);
    thread mythread3(c,2);//operator作为启动函数,调用拷贝构造函数
    A c1(3);
    thread mythread3(std::ref(c),2);//operator作为启动函数,不调用拷贝构造函数
} 

/*  	
	结论1: 若调用函数含有引用, 且想通过隐式类型转换为调用函数参数时会出错 如图1-1所示,修改方法,将mypirnt(const type(类型) &a);即可, 若传入参数不需要类型转换则无此问题,如图1-2所示.
	结论2: 若调用函数有引用, 传入参数不管是不是需要类型转换,结果应该都时一致的.(加上const的前提)如图	1-5, 因为上方图片时传入不需要类型转换的A类类型, 所以会多一次构造和析构.
	结论3: 若调用函数有引用,传入参数为类类型时 如图1-3, 此时会比调用函数为值传递少一次拷贝,如图1-4.所以,若从资源节合的方向考虑, 想要节省系统开销应该选用加引用, 但是当调用函数值不为类类型时,此时应该考虑是否可以采用值传递(避免调用detach方法出现问题)
	结论4: 若线程启动调用拷贝构造函数,则后续调用detach()是安全的,因为是在另一个线程里申请的空间,而不是主线程, 若没有调用拷贝构造函数,那么随着主线程结束.内存空间被释放,则访问的是已经释放的空间.
	结论5: 线程中若调用了拷贝构造函数. 那么在线程中修改传入的值是不会修改主线程中的值, 因为此时传递的是假引用, 若想一致修改则应该加上ref, 这样传递过去子线程修改, 主线程也会修改,但是此时不应该调用detach函数, 必须调用join,不然当主线程资源释放,子线程会调用已释放的空间.
	综上, 若代码中存在有线程调用函数, 且需要传入参数, 那么在不改变的参数前加上const,防止调用时出现不持支隐式类型转换
*/
```



![图1-1](C:\Users\yx\Desktop\笔记\1566367211953.png)

​																				图1-1

![1566367614430](C:\Users\yx\Desktop\笔记\1566367614430.png)

​																				图1-2												

![1566368541413](C:\Users\yx\Desktop\笔记\1566368541413.png)

​																				图1-3		

![1566368607909](C:\Users\yx\Desktop\笔记\1566368607909.png)

​																				图1-4	

![1566369366384](C:\Users\yx\Desktop\笔记\1566369366384.png)

​																				图1-5

###### 创建和等待多个线程

```c++
#include <iostream>
#include <thread>
#include <vector>

using namespace std;


void myprint(int mu)
{
	cout << "my thread start = "<< mu << endl;
	cout << "thread end = "<< mu << endl;
}

int main()
{
	vector<thread> mythread;

	for (int index = 0; index < 10; ++index)
	{
		mythread.push_back(thread(myprint, index)); //创建和执行线程
	}


	for (auto it = mythread.begin();it != mythread.end();++it)
	{
		it->join();
	}

	cout << "主线程 end" << endl;
	return 0;
}
/*
	由于系统随机切换, 所以不会按照我们等待的顺序或者初始化的顺序输出
*/
```

###### 共享数据问题分析

```C++
#include <iostream>
#include <thread>
#include <vector>

using namespace std;

//共享读数据
vector<int> Gx = { 1,2,3 };

void myprint(int mu)
{
	
	for (auto it = Gx.begin(); it != Gx.end(); it++)
	{
		cout << "当前线程id = " << this_thread::get_id() << endl;
		cout << *it << endl;
	}
}

int main()
{
	vector<thread> mythread;

	for (int index = 0; index < 10; ++index)
	{
		mythread.push_back(thread(myprint, index)); //创建和执行线程
	}


	for (auto it = mythread.begin();it != mythread.end();++it)
	{
		it->join();
	}

	cout << "主线程 end" << endl;
	return 0;
}
/*
	当多线程只是读数据,不影响,但是写数据会有问题.
	因为你可能以为的数据其余的线程正在更改这个数据.所以你读出来的数据和预期会产生偏差; 所以只能存在一个线程对数据写,可以多个线程对同一个数据读;
	
*/
```

###### 同时写数据

```c++
#include <iostream>
#include <thread>
#include <vector>
#include <list>
#include <mutex>

using namespace std;

//成员函数作为线程的启动函数
class Rev
{
public:
	Rev()
	{

	}
	~Rev() 
	{

	}
	bool protectedOutData(int &commd)
	{
		myMutex.lock();
		if (!msgRecvQue.empty())
		{
			commd = msgRecvQue.front();//取出第一个元素
			msgRecvQue.pop_front();//移除最后一个元素
			//命令处理
			cout << commd << endl;
			myMutex.unlock();
			return true;
		}
		myMutex.unlock();
		return false;
	}
	void inMsgRecvQue()
	{
		for (int i = 0; i < 100000; ++i)
		{
			cout << "inMsgQue" << endl;
			myMutex.lock();
			msgRecvQue.push_back(i);//i就是玩家的命令
			myMutex.unlock();
		}
	}
	void outMsgRecvQue()
	{
		int cmd = 0;
		while (true)
		{
			
			bool result = protectedOutData(cmd);
			if (result)
			{
				cout << "取出元素成功:" << cmd << endl;
			}
			else
			{
				cout << "当前数据为空" << endl;
			}
		}
	}
private:
	list<int> msgRecvQue; //玩家发送过来的命令
	mutex myMutex;
};
int main()
{
	//网络游戏服务器
	//1. 收集玩家命令,把数据命令放进队列中
	//2. 从队列中取出玩家发送的命令,执行玩家需要的动作
	//3. 引入互斥量,防止同时读写 lock()加锁, unlock()解锁,成对使用;也可以使用std::lock_guard();可以不必自己写unlock
	/*
		list和vector
	*/
	Rev myRev;
	thread myOutThread(&Rev::outMsgRecvQue,&myRev);
	thread myInThread(&Rev::inMsgRecvQue, &myRev);


	myOutThread.join();
	myInThread.join();
	return 0;
}
```

###### 死锁的产生

```c++
/*
	由于业务需求需要两个锁, 但是锁的顺序时不一样的
	当有一次运行到线程t1的锁,上下文突然切换到线程t2执行了m2.lock(), 此时由于导致了t1中锁了m1导致t2线程无法继续执行下去, 而换回到t1的时候m2也被锁住了,导致了两边都无法解开对方的锁,形成死锁.
*/
mutex m1,m2;

void t1()
{
    /*code*/
    m1.lock(); //std::lock_guard<mutex> sg(m1,adopt_lock);防止死锁加上不用调用unlock
    /*code*/
    m2.lock();
    /*code*/
    m2.unlock();
    /*code*/
    m1.unlock();
}

void t2()
{
    /*code*/
    m2.lock();
    /*code*/
    m1.lock(); 
    /*code*/
    m1.unlock();
    /*code*/
    m2.unlock();
}

```

###### 死锁的解决方法

```c++
/*
	1. 调用顺序采用一致的顺序
	2. std::lock();//注意配对的问题
*/
```


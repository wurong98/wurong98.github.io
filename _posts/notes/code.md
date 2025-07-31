# 经典题目和代码解析

## 牛顿迭代

``` cpp
#include <stdio.h>
#include <iostream>

#define esp 0.000001

double func(double num)
{
    double x = 1;
    while (true)
    {
        // double nt = x - ((x * x) - num) / (2 * x);
        double nt = (x + num / x) / 2; // 化简可以得到
        if (std::abs(x - nt) < esp)
        {
            return nt;
        }
        x = nt;
    }
    return -1;
}

int main()
{
    double x;
    while (scanf("%lf", &x) != EOF)
    {
        printf("result = %lf\n", func(x));
    }
    return 0;
}
```

迭代的核心公式 $x_{i + 1} = x_{i} - \frac{f(x)}{f'(x))}$。计算$\sqrt{b}$对应的函数为：$f(x) = x^{2} - b$。迭代终止条件可以是和上一个数字比较精度在`1e-6`。
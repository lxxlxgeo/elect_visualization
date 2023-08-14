# WRF4.5 RLDAS 模式预报气象预报输出

## 集成了 RLDAS 的 降水量,风速,位能 3种气象要素

# 特性
## 数据读取强制使用时间匹配方式


# 方法
## ***1*** 首先根据 预报开始时间,预报结束时间,预报步长来确定 要渲染的时段,返回一个预报时间的列表
## ***2*** 使用时间列表遍历预报时间,根据不同的时间属性来获取想要的文件(强制使用时间来匹配文件,当前使用的是re表达式)
## ***3** 以不同的气象要素,选择不同合成方式:降水量累加,位能等其他要素求最大值和平均值

## 绘图思路
### 1.绘图要区分不同的预报模式,根据 step来确定不同的 level(刻度等)
### 2.绘图类需要再优化一下

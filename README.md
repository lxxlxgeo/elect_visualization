# 微气象服务项目

该项目是 2023 年微气象服务项目的一部分。它旨在使用 GRIB 格式的 ECMWF 数据提供微气象数据的分析和可视化。

## 入门指南

要运行代码并可视化微气象数据，请按照以下步骤操作：

1. 安装所需的 Python 包：

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">pip install -r requirements.txt
</code></div></div></pre>

3. 根据需要修改 main.py 脚本中的文件路径和设置。

## 数据读取器

data_reader.py 脚本包含了 GribDataReader 类，负责读取和处理 GRIB 数据。

* `get_data()`: 该函数从 GRIB 文件中读取数据，进行处理，并返回数据、纬度和经度数组。

## 数据可视化

elect_visualization.py 脚本包含了数据可视化的代码。

* `plot_data(data, lats, lons)`: 该函数接受数据、纬度和经度数组作为输入，并使用 matplotlib 将微气象数据绘制在地图上。

## 主程序

main.py 脚本是程序的入口点。它演示了如何使用 GribDataReader 类读取和处理数据，然后使用 plot_data () 函数在地图上可视化数据。

## 使用方法

运行 main.py 脚本以开始数据处理和可视化：

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">python main.py
</code></div></div></pre>

脚本将从指定的 GRIB 文件中读取数据，进行处理，然后生成一张地图，将微气象数据绘制在上面。

## 数据目录结构

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">/mnt/d/kt/project/yl/2023-HLJIEE-MicroMeteorologicalServices/
├── data_reader.py
├── elect_visualization.py
├── main.py
├── requirements.txt

`Emain.py` 脚本从这些文件中读取数据并进行数据可视化。

## 时间


  |      00时      |      03时      |      06时      |      09时      |      ...      |      18时      |
  |               |               |               |               |               |               |
  |    数据时间   |    数据时间   |    数据时间   |    数据时间   |    数据时间   |    数据时间   |
  |               |               |               |               |               |               |
  |       11时起报（预报步长为3小时）       |       17时起报（预报步长为3小时）       |
                 |               |               |               |               |               |
                 └───────────────┘               └───────────────┘
       手动出图（出报告）时间：11时              手动出图（出报告）时间：17时
       （需读取00时刻数据）                    （需读取00时刻数据）

  |      12时      |      15时      |      18时      |      21时      |      ...      |      06时      |
  |               |               |               |               |               |               |
  |    数据时间   |    数据时间   |    数据时间   |    数据时间   |    数据时间   |    数据时间   |
  |               |               |               |               |               |               |
  |       23时起报（预报步长为3小时）       |       05时起报（预报步长为3小时）       |
                 |               |               |               |               |               |
                 └───────────────┘               └───────────────┘
       手动出图（出报告）时间：23时              手动出图（出报告）时间：05时
       （需读取12时刻数据）                    （需读取12时刻数据）



```flow

```

# Lecture 0_Search

## 搜索
寻找问题的解决方案，即给定初始状态和目标状态，返回如何从前者到达后者的解决方案

**Agent**
**代理**，感知环境并对环境采取行动的实体

**State**
**状态**，代理在环境中的配置

**Initial State**
**初始状态**，搜索算法开始的状态

**Actions**
**行为**，在某个状态下可以做出的选择
定义为函数 Actions(s)：状态s为输入，返回可以在状态中执行的操作集

**Transition Model**
**过渡模型**，对在某状态下执行某种操作所产生的状态的描述
定义为函数Results(s,a)：状态s和操作a作为输入，返回在状态s中执行操作a所产生的状态

**State Space**
**状态空间**，从初始状态可到达的所有状态的集合，可视化为有向图

**Goal Test**
**目标测试**，确定给定状态是否为目标状态

**Path Cost**
**路径成本**，与给定路径相关的数字成本

## 解决搜索问题
**Solution**
**解决方案**，从初始状态到目标状态的一系列操作
**Optimal Solution**
**最优解**，所有解决方案中路径成本最低的解决方案

**Node**
搜索过程中的数据存储在**节点**中，包括：
    - **State**：一个**状态**
    - **Parent Node**：它的**父节点**
    - **Action**：一个**操作**，能从父节点的状态到达当前节点状态
    - **Path Cost**：从初始节点到此节点的**路径成本**

**Frontier**
**边界**，一种管理节点的机制，其包含一个初始状态和一个表示探索项的空集合，重复以下操作直到问题解决：
> 1. 如果边界为空：停止。此时问题没有解决方案。
> 2. 从边界中移除一个节点（这个节点是将要被考虑的节点）
> 3. 如果节点包含目标状态：得到解决方案，停止循环。
> 否则：
>       1. 找到从该节点可以到达的所有新节点，并将结果添加到边界
>       2. 将当前节点添加到已探索的集合中

### Depth-First Search (DFS)
**深度优先搜索**，尝试另一个方向之前会耗尽每个方向

优点：在最优情况下，算法是最快的
缺点：找到的解决方案可能不是最佳的；在最坏的情况下，该算法将在找到解决方案之前探索每条可能的路径，故在达到解决方案之前花费了尽可能长(as long as possible)的时间

使用**栈**作为数据结构。将节点添加到边界后，要删除和考虑的第一个节点是最后添加的节点。
```Python
# Define the function that removes a node from the frontier and returns it.
 def remove(self):
    # Terminate the search if the frontier is empty which means there is no solution 
    if self.empty():
        raise Exception("empty frontier")
    else:
        # Save the last item in the list (which is the newest node added)
        node = self.frontier[-1]
        # Remove the last node 
        self.frontier = self.frontier[:-1]
        return node
```

### Breadth-First Search (BFS)
**广度优先搜索**，同时遵循多个方向，在每个可能的方向上迈出一步，然后再在每个方向上迈出第二步

优点： 一定能找到最优解
缺点：几乎无法达到最短时间；在最坏的情况下，该算法需要尽可能长的时间来运行。

使用**队列**作为数据结构，将节点添加到边界后，要删除和考虑的第一个节点是最先添加的节点。
```Python
   # Define the function that removes a node from the frontier and returns it.
    def remove(self):
    	# Terminate the search if the frontier is empty which means there is no solution 
        if self.empty():
            raise Exception("empty frontier")
        else:
            # Save the oldest item on the list (which was the first one to be added)
            node = self.frontier[0]
            # Remove the first node
            self.frontier = self.frontier[1:]
            return node
```

### Greedy Best-First Search
**贪心最佳优先搜索**，先搜索扩展最接近目标的节点。

- **无信息搜索算法**：一类没有通过自己的探索获得有关问题信息的算法
    - 深度优先搜索
    - 广度优先搜索
- **知情搜索算法**：一类考虑额外信息来尝试提高其性能的算法

**启发式函数h(n)**：
估计下一个节点与目标的接近程度，以决定先扩展哪个节点，决定着贪婪最佳优先搜索的效率。
可能会出错从而导致算法比其他情况更慢。
在迷宫问题中依赖**曼哈顿距离**，即忽略墙壁计算从一个位置到目标位置需要向上下左右迈出多少步，也即两点横纵坐标差的绝对值之和。

### A* Search
**A\* 搜索**，贪婪最佳优先算法的发展，更准确地确定解决方案的成本并实时优化其选择

包括：
- **h(n)**：启发式函数，从当前位置到目标的路径成本。
    - **Admissible**：永远不高估真实成本
    - **Consistent**：当前节点的路径成本不大于下一个节点的路径成本加上到下一个节点的成本，即**h(n) ≤ h(n') + c**
- **g(n)**：到当前位置的累积成本

该算法会跟踪两个函数值的和，一旦超过某个先前选项的估计成本，该算法将放弃当前路径并返回到先前的选项，从而防止自己沿着一条漫长而低效的路径行走

在某些情况下，它的效率可能会低于贪婪的最佳优先搜索或其他算法

### Adversarial Search
对抗性搜索，即AI试图实现相反目标。以井字棋（tic tac toe）为例

#### 数学化
**玩家**
MAX(X)：目标最大化得分
MIN(O)：目标最小化得分

**游戏结果**
1分 —— X胜
0分 —— 平局
-1分 —— O胜

**函数**
$S_0$：初始状态，即一个空的3×3棋盘
Player(s)：一个函数，输入状态S，返回到达回合的玩家
Action(s)：一个函数，输入状态S，返回该状态下的所有合法动作
Result(S, a)：一个函数，输入状态S和操作a，返回在状态S上执行操作a所产生的新状态
Terminal(S)：一个函数，输入状态S，若有人获胜或平局则返回True，否则返回False
Utility(S)：一个函数，输入状态S，返回该状态的最终值：-1、0或1

#### **如何工作**
##### 以井字棋为例
![0_井字棋树.jpg](https://wlry-1323998276.cos.ap-nanjing.myqcloud.com/llm/202512281924972.jpg)

递归地模拟从当前状态开始直到最终状态为止可能发生的所有情况。 
算法在最小化得分和最大化得分之间交替，为每个可能的操作所产生的状态创建值。如最大化玩家问：“我采取这个行动会产生一个新的状态。如果最小化玩家要达到最佳效果，他会采取什么行动来达到最低值？”最小化玩家同理。最终，通过递归推理，最大化玩家得出当前状态下所有可能的动作产生的值，随后选择最高的值

##### 以一般对抗游戏为例
![0_对抗游戏树.jpg](https://wlry-1323998276.cos.ap-nanjing.myqcloud.com/llm/202512281934599.jpg)

对于一般的对抗游戏，伪代码表示如下：
```python
#给定一个状态S，目标最大化玩家在Action(S)中选择一个动作a，使Min_value(Result(s, a))的值最大
def Max_value(S)：
    if Terminal(S):
        return Utility(S)
    v = - ∞
    for a in Action(S):
        v = max(v, Min_value(Result(S, a)))
    return v

#目标最小化玩家在Action(S)中选择一个动作a，使Max_value(Result(s, a))的值最小
def Min_value(S)：
    if Terminal(S):
        return Utility(S)
    v = + ∞
    for a in Action(S):
        v = min(v, Max_value(Result(S, a)))
    return v
``` 

#### **Alpha-Beta Pruning**
*Alpha-Beta剪枝*，一种MiniMax算法的优化方法。在确定一个操作的价值后，如果有证据表明后续操作使对手得到的分数比已有操作使对手得到的分数更好，则无需进一步考察该操作，因为它肯定不如之前建立的那个操作有利。
![0_剪枝.jpg](https://wlry-1323998276.cos.ap-nanjing.myqcloud.com/llm/202512281933806.jpg)

#### **Depth-Limited Minimax**
*深度限制的MiniMax算法*，在停止之前仅考虑预定的移动次数，而不会到达最终状态。

**评估函数**：
根据给定状态估计游戏的预期值
以国际象棋为例，将当前棋盘状态作为输入，基于每个玩家拥有的棋子及其在棋盘上的位置，返回一个正值或负值，以代表一名玩家相对于另一名玩家的有利程度，这些值用于决定操作
评估函数的性能好坏决定着依赖它的MiniMax算法的好坏
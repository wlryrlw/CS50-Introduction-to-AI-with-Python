# 概率
## 基本概念
**可能的情况**：ω
$0 < P(ω) < 1$
$\Sigma P(ω) = 1$

**无条件概率**：
在没有任何其他证据的情况下，对某个命题的相信程度

**有条件概率**：
$P(a|b)=\frac{P(a∧b)}{P(b)}$

**随机变量**

**独立性**：
一个事件的发生不会影响另一个事件发生的概率
$P(a∧b) = P(a)P(b)$

**联合概率与边缘概率**

**容斥原理**：
$P(a∨b) = P(a) + P(b) - P(a∧b)$

## 贝叶斯网络
**贝叶斯公式**： $P(b|a)=\frac{P(a|b)P(b)}{P(a)}$

![image.png](https://wlry-1323998276.cos.ap-nanjing.myqcloud.com/llm/202601212014623.png)

定向图，每个节点代表一个随机变量
从 X 指向 Y 的箭头表示 X 是 Y 的父节点，Y 的概率分布取决于 X 的值
每个节点 X 都有概率分布 $P(X|Parents(X))$

### 推理
查询 X：要计算其概率分布的变量
证据变量 E ：针对事件 e 观测到的一个或多个变量
隐藏变量 Y：既不是查询变量，也没有被观测到的变量
目标：计算 $P(X|e)$

$P(x|e)= \alpha P(x,e) = \alpha \Sigma_y P(X,e,y)$

```python
from pomegranate import *

# Rain node has no parents
rain = Node(DiscreteDistribution({
    "none": 0.7,
    "light": 0.2,
    "heavy": 0.1
}), name="rain")

# Track maintenance node is conditional on rain
maintenance = Node(ConditionalProbabilityTable([
    ["none", "yes", 0.4],
    ["none", "no", 0.6],
    ["light", "yes", 0.2],
    ["light", "no", 0.8],
    ["heavy", "yes", 0.1],
    ["heavy", "no", 0.9]
], [rain.distribution]), name="maintenance")

# Train node is conditional on rain and maintenance
train = Node(ConditionalProbabilityTable([
    ["none", "yes", "on time", 0.8],
    ["none", "yes", "delayed", 0.2],
    ["none", "no", "on time", 0.9],
    ["none", "no", "delayed", 0.1],
    ["light", "yes", "on time", 0.6],
    ["light", "yes", "delayed", 0.4],
    ["light", "no", "on time", 0.7],
    ["light", "no", "delayed", 0.3],
    ["heavy", "yes", "on time", 0.4],
    ["heavy", "yes", "delayed", 0.6],
    ["heavy", "no", "on time", 0.5],
    ["heavy", "no", "delayed", 0.5],
], [rain.distribution, maintenance.distribution]), name="train")

# Appointment node is conditional on train
appointment = Node(ConditionalProbabilityTable([
    ["on time", "attend", 0.9],
    ["on time", "miss", 0.1],
    ["delayed", "attend", 0.6],
    ["delayed", "miss", 0.4]
], [train.distribution]), name="appointment")

# Create a Bayesian Network and add states
model = BayesianNetwork()
model.add_states(rain, maintenance, train, appointment)

# Add edges connecting nodes
model.add_edge(rain, maintenance)
model.add_edge(rain, train)
model.add_edge(maintenance, train)
model.add_edge(train, appointment)

# Finalize model
model.bake()
```

### 采样
每个变量都根据其概率分布被抽取一个值
```python
import pomegranate

from collections import Counter

from model import model

def generate_sample():

    # Mapping of random variable name to sample generated
    sample = {}

    # Mapping of distribution to sample generated
    parents = {}

    # Loop over all states, assuming topological order
    for state in model.states:

        # If we have a non-root node, sample conditional on parents
        if isinstance(state.distribution, pomegranate.ConditionalProbabilityTable):
            sample[state.name] = state.distribution.sample(parent_values=parents)

        # Otherwise, just sample from the distribution alone
        else:
            sample[state.name] = state.distribution.sample()

        # Keep track of the sampled value in the parents mapping
        parents[state.distribution] = sample[state.name]

    # Return generated sample
    return sample
    
# Rejection sampling
# Compute distribution of Appointment given that train is delayed
N = 10000
data = []

# Repeat sampling 10,000 times
for i in range(N):

    # Generate a sample based on the function that we defined earlier
    sample = generate_sample()

    # If, in this sample, the variable of Train has the value delayed, save the sample. Since we are interested interested in the probability distribution of Appointment given that the train is delayed, we discard the sampled where the train was on time.
    if sample["train"] == "delayed":
        data.append(sample["appointment"])

# Count how many times each value of the variable appeared. We can later normalize by dividing the results by the total number of saved samples to get the approximate probabilities of the variable that add up to 1.
print(Counter(data))
```

### 似然加权采样
传统的“拒绝采样”中，舍弃了与现有证据不符的样本，效率低下

1. 强行固定：
	遇到证据变量（比如“火车准点”）时，不进行随机采样
2. 采样：
	对于非证据变量（比如“天气”、“是否维护”），依然按照贝叶斯网络的概率分布采样
3. 计算权重：
	因为“强行”让证据变量发生了，这个样本可能并不符合自然的概率分布，为了修正这个偏差，要计算一个权重 $w=P(e|Parents(e))$ ，代表了在当前采样出的环境下，这个证据发生的可能性有多大
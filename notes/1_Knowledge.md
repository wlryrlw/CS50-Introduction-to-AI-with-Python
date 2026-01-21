# Lecture 1_Knowledge

**Knowledge-Based Agents**
*知识型代理*，通过对知识内部的表示进行操作来推理
**Sentence**
*句子*，是知识表示语言中关于世界的断言（在程序中的一阶逻辑），是人工智能存储知识并使用其来推断新信息的方式

## 命题逻辑
Propositional Symbols：*命题符号*，用于表示命题的字母

Logical Connectives：*逻辑联结词*，连接命题符号的逻辑符号

### 非(¬)
**Not**，反转命题的真值

|P|¬P|
|:--:|:--:|
|true|false|
|false|true|

### 与(∧)
**And**，连接两个不同的命题，命题都为真时才为真

|P|Q|P∧Q|
|:--:|:--:|:--:|
|true|true|true|
|true|false|false|
|false|true|false|
|false|false|false|

### 或(∨)
**Or**，只要其中一个参数为真，它就为真

|P|Q|P∨Q|
|:--:|:--:|:--:|
|true|true|true|
|true|false|true|
|false|true|true|
|false|false|false|

### 蕴含(→)
**Implication**，若 P 则 Q，P 称前件，Q 称后件
前件为真时，后件为真，蕴含式为真；后件为假，蕴含式为假
前件为假时，蕴含式永远为真（显然成立）

| P | Q | P→Q |
| :--: | :--: | :--: |
| true | true | true |
| true | false | false |
| false | * | true |

### 等价(↔)
**Biconditional**，即“当且仅当”

|P|Q|P↔Q|
|:--:|:--:|:--:|
|true|true|true|
|true|false|false|
|false|true|false|
|false|false|true|

### Model
**模型**，为每一个命题分配一个值（真或假）

### Knowledge Base (KB)
**知识库**，一个知识型代理所知道的一组句子。这些句子是 AI 以命题逻辑句子的形式提供的关于世界的知识，可以用来对世界进行额外的推理

### 蕴涵(⊨)
**Entailment**,根据已知的知识和逻辑规则，通过推理得出新的结论或信息
α ⊨ β：若 α 为真，则 β 也为真

> 蕴含(Implication) 是连接两个命题的逻辑联结词
> 蕴涵(Entailment) 是一个关系，意味着如果α中的所有信息都是真的，则β中的所有信息也是真的

## 推理
从旧句子推导出新句子的过程

**Query α**
*α查询*：α是否为真、KB 是否蕴含α。

### 模型检查算法

- 1.枚举所有可能的模型
- 2.如果在每个 KB 为真的模型中，α 也为真，则 KB ⊨ α
	- Step 1：枚举所有可能模型
	- Step 2：检查每个模型，并根据知识库检查它是否正确

例：
P: It is a Tuesday. Q: It is raining. R: Harry will go for a run.
KB: (P ∧ ¬Q) → R  , P , ¬Q
Query: R

|P|Q|R|KB|
|:--:|:--:|:--:|:--:|
|false|false|false|false|
|false|false|true|false|
|false|true|false|false|
|false|true|true|false|
|true|false|false|false|
|==true==|==false==|==true==|==true==|
|true|true|false|false|
|true|true|true|false|

在每个 KB 为真的模型中，α（例中为 R）为真，故 KB ⊨ R 成立

```python
def check_all(knowledge, query, symbols, model):

# If model has an assignment for each symbol
# (The logic below might be a little confusing: we start with a list of symbols. The function is recursive, and every time it calls itself it pops one symbol from the symbols list and generates models from it. Thus, when the symbols list is empty, we know that we finished generating models with every possible truth assignment of symbols.)
if not symbols:

    # If knowledge base is true in model, then query must also be true
    if knowledge.evaluate(model):
        return query.evaluate(model)
    return True
else:

    # Choose one of the remaining unused symbols
    remaining = symbols.copy()
    p = remaining.pop()

    # Create a model where the symbol is true
    model_true = model.copy()
    model_true[p] = True

    # Create a model where the symbol is false
    model_false = model.copy()
    model_false[p] = False

    # Ensure entailment holds in both models
```

`check_all`是递归的，它选择一个符号，创建两个模型，其中一个模型中该符号为真，另一个模型中该符号为假，然后再次调用自身。该函数会不断重复此过程，直到所有符号在模型中都被赋予真值，导致列表为 symbols 空
一旦列表为空（如代码行所示 if not symbols），在函数的每个实例中（每个实例都包含不同的模型），该函数都会检查知识库 (KB) 在该模型下是否为真。如果知识库在该模型下为真，则该函数会检查查询是否为真

## 知识工程
Knowledge Engineering，指在人工智能中如何表示命题和逻辑的过程

## 推理规则
|推理规则|已知|推论|
|:---:|:---:|:---:|
|命题演算分离|α→β,α|β|
|合取消去|α∧β|α|
|双重否定|¬(¬α)|α
|蕴含消去|α→β|¬α∨β
|等价消去|α↔β|(α→β)∧(β↔α)
|德摩根律|¬(α∧β)|¬α∨¬β
|分配率|α∨(β∧γ)|(α∨β)∧(α∨γ)

## 归结算法
### 生成 CNF
**析取**：由 “或” 连接的命题
**合取**：由 “与” 连接的命题

**子句**：文字、命题符号的析取
**合取范式 CNF**：子句的合取；任何逻辑语句都可以转换为 CNF

**生成合取范式**：
消除等价：α↔β 变为 (α→β)∧(β→α)
消除蕴含：(α→β) 变为 ¬α∨β
否定向内移动：¬(α∧β) 变为 ¬α∨¬β

### 归结
互补文字：两个相同的原子命题，其中一个被否定，而另一个不被否定，例如 P 和 ¬P

如果“或”命题中的两个子命题之一为假，则另一个命题必然为真
即，已知：P∨Q，¬P ，则：Q

特殊的，¬P 和 P 进行归结会得到空子句（始终为假）
一般的，先生成 CNF，后进行归结

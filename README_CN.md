# GaiaSage

**GaiaSage: 地理空间分析AI助手**

GaiaSage是一个专为地理空间分析师、环境科学家和研究人员设计的AI智能助手。该项目能够将用户的自然语言查询转换为可在Google Earth Engine等平台上执行的分析代码。

## 项目概述

GaiaSage旨在理解用户查询背后的*意图*，通过对话澄清需求（如研究区域和时间范围），然后生成执行分析所需的脚本。

系统采用分阶段多智能体协作架构：

```
用户查询
   ↓
根代理
   ↓
守卫代理  ──(如果有效)──▶ 规划代理 ⇄ 用户
   ↑                                │
   └──────(如果批准)────────────────┘
                 ↓
            根代理
                 ↓
            编码代理
                 ↓
           最终输出
```

## 项目状态

该项目目前正在积极开发中。执行计划可在[`plans/01_init_plan.md`](plans/01_init_plan.md:1)中找到。

## 快速开始

1. **安装依赖：**

    ```bash
    uv sync
    ```

2. **配置环境变量：**

    ```bash
    cd src
    cp gaiasage/.env.example gaiasage/.env
    # 编辑.env文件设置GOOGLE_API_KEY
    vim gaiasage/.env
    ```

**如何获取Gemini API密钥**：

- 访问Google AI Studio：https://aistudio.google.com/
- 使用Google账户登录
- 在左侧菜单中点击"Get API key"
- 点击"Create API key in new project"
- 您的API密钥将被生成

3. **运行代理：**

    ```bash
    cd src
    uv run python -m google.adk.cli web
    ```

## 对话示例

以下是一个关于在婆罗洲进行森林砍伐分析的[示例对话](chat.md)，最终代码可在Google Earth Engine上运行。

![演示](gaiasage_demo.jpg)

**用户**：森林正面临危险，我能做什么？

**GaiaSage**：很抱歉听到这个消息。但是，我是一个专业的地理空间分析助手，无法回答此领域之外的问题。

**用户**：你能帮我在婆罗洲进行森林砍伐分析吗？

**GaiaSage**：当然可以。听起来您想要分析婆罗洲岛的森林损失，以了解森林砍伐的程度和趋势。我绝对可以帮助您。

为了制定最佳的分析计划，我需要更多信息。请告诉我：

**时间范围**：您想分析哪个特定时期？例如，您是想看过去20年（如2001-2021年），还是更近期的时间？

**感兴趣区域（AOI）**：婆罗洲是一个非常大的岛屿。您是对整个岛屿感兴趣，还是特定区域，比如某个特定省份（如加里曼丹）、国家（文莱、印度尼西亚、马来西亚），或特定的国家公园？

**分析目标**：您希望得到什么主要输出？您是希望得到显示砍伐区域的地图、显示时间变化砍伐率的图表，还是森林损失总量的统计摘要？

**用户**：时间范围：从2020年到2022年
定义婆罗洲，合并文莱、印度尼西亚加里曼丹省份和马来西亚沙巴、沙捞越州的边界。
生成空间地图

**GaiaSage**：很好，谢谢您提供这些详细信息。

以下是我建议的创建森林砍伐地图的技术方法：

首先，我们将通过加载国际行政边界数据集来定义您的感兴趣区域（AOI）。我们将选择并合并您提到的特定区域——文莱、印度尼西亚加里曼丹省份和马来西亚沙巴、沙捞越州——创建婆罗洲岛的单一多边形。

接下来，我们将使用备受推崇的Hansen全球森林变化数据集。我们将识别并分离2020年至2022年间的森林损失区域。这种方法听起来可以吗？

**用户**：好的，继续。

**GaiaSage**：<返回详细的json计划>。您批准这个代码生成计划吗？

**用户**：批准。

**GaiaSage**：<完整的可运行的JavaScript Earth Engine代码>

**成本估算**

此任务涉及处理大量卫星图像，预计会消耗适量的GEE计算单元。主要计算负载来自处理整个婆罗洲岛30米分辨率的Hansen全球森林变化数据集，这是一个非常大的区域。但是，执行的操作（过滤、掩膜和简单波段数学）本质上并不复杂。没有密集的操作，如多年合成或复杂的统计缩减。由于数据的大面积和高分辨率，渲染最终地图图层可能需要几分钟时间。

点击[这里](https://code.earthengine.google.com/aa601898ec0f8ab0284172a590d713f1)查看可运行的Google Earth Engine代码。

LLM输出有时可能不可预测，因此偶尔需要您的协助来澄清需求——比如指定数据集或输出格式。

## 系统架构与代理设计

**目标受众**：对内部实现和设计细节感兴趣的技术审查员和工程师。

**主要目标**：解释*系统如何工作*，包括代理之间的协作和数据流。

### 1. 高级架构

**关键数据产物**：

* `用户查询`：来自用户的初始输入
* `JSON计划`：由`规划代理`输出的结构化分析计划
* `GEE代码`：为在Google Earth Engine（GEE）上执行而生成的最终代码

### 2. 代理团队简介

每个代理都有明确且独特的职责。以下是每个代理的简介：

#### `守卫代理`（门卫）

* **角色**：验证传入用户请求的范围和可行性
* **使用模型**：`gemini-1.5-flash-latest`
* **设计理念**：选择此模型是因为其速度和成本效率，适合处理轻量级分类任务
* **关键指令**：
  * 使用严格的二元决策规则操作
  * 立即拒绝超出范围的查询
  * 确保不会不必要地触发昂贵的计算

#### `规划代理`（规划师）

* **角色**：与用户协作创建详细的结构化分析计划
* **使用模型**：`gemini-2.5-pro`
* **设计理念**：需要高级语言理解、推理和规划能力
* **关键指令**：
  * 遵循四步工作流程：澄清、范围、提议、确认
  * 以严格的JSON格式输出计划
  * 等待用户批准后再继续

#### `编码代理`（编码员）

* **角色**：将批准的JSON计划转换为可执行代码并估算成本
* **使用模型**：`gemini-2.5-pro`
* **设计理念**：需要最先进的代码生成和资源估算能力
* **关键指令**：
  * 遵循顺序执行：首先生成代码，然后估算成本
  * 在没有产生可运行代码的情况下不得进行估算

#### `根代理`（协调员）

* **角色**：监督和协调所有子代理
* **设计理念**：确保确定性工作流程并防止跨代理混乱
* **执行逻辑**：
  * 作为驱动过程的状态机
  * 处理转换逻辑并强制执行协议合规性

## 设计理念与关键决策

### 问答格式：关键设计决策

#### Q1：为什么采用多代理架构而不是单体"一体化"代理？

**A**：遵循职责分离原则，每个代理专注于单一任务。这简化了提示设计，增强了可靠性，并提高了可维护性。它还允许模块化升级——例如，在不影响系统其余部分的情况下替换`规划代理`。

#### Q2：为什么为不同代理使用不同的LLM模型？

**A**：为了平衡成本和性能。

* `守卫代理`使用轻量级`Flash`模型进行快速二元分类，成本最低
* `规划代理`和`编码代理`使用更强大的`Pro`模型进行复杂推理和代码生成任务

#### Q3：为什么引入明确的"JSON计划"作为中间步骤？

**A**：JSON计划作为**检查点**和**合约**：

* 将模糊的自然语言转换为结构化、明确的格式
* 确保在代码生成前获得完整的用户批准，减少昂贵的返工
* 为`编码代理`提供清晰的输入接口

#### Q4：`守卫代理`的战略价值是什么？

**A**：它显著提升了用户体验和系统效率：

* 早期过滤无效请求，避免浪费时间和资源
* 保护更昂贵的代理免受无关输入的处理
* 作为节约成本的防火墙

### 未来工作与已知限制

**展望**：

* 利用`log_out_of_scope_question`工具的数据来增强用户指导功能

**限制**：

* 仅支持Google Earth Engine（GEE）代码生成

## 技术栈

- **语言**：Python
- **包管理器**：uv (https://github.com/astral-sh/uv)
- **AI代理框架**：Google ADK (Agent Development Kit)
- **模型**：Gemini 2.5 Pro
- **数据库**：PostgreSQL
# 《人生重启模拟器》Web版 (中文|[English](./README-EN.md))

《人生重启模拟器》Web版，一款基于[人生重来模拟器](https://github.com/EmbraceAGI/LifeReloaded)项目开发的创新网络游戏，由 ChatGPT 驱动，提供了一个交互式的模拟人生体验。玩家将沉浸在 AI 实时创造的丰富多彩、逼真的人生旅程中。本游戏深受文学与人工智能结合的影响，涵盖 AI 驱动的随机事件、基于心理学的角色构建等核心特性。

Web版不仅继承了原项目的精髓，还针对 GPT-3.5 特性进行了优化，简化了玩家的操作体验，无需烦恼 GPT-4 的配置问题。此外，得益于[EmbraceAGI社区](https://github.com/EmbraceAGI/)的支持，项目不断与玩家和开发者互动，推动 AI 在游戏行业的创新发展。

欢迎通过此[链接](https://sun-zhengwt.com/life-reload/)试玩。我们致力于打造一个更加便捷、直观的平台，带给广大用户由 AI 技术打造的全新人生重启体验。

## 1. 安装依赖

要安装此项目所需的依赖，请使用以下命令：

```bash
pip install -r requirements.txt
```

#### 可选：配置 Redis 以提高性能

如果您希望提高性能，请在本地机器上配置 Redis 服务，并安装 Python redis 依赖：

```bash
pip install redis
```

## 2. 设置环境变量

为了项目的正常运行，您需要设置一些环境变量。

- 在项目根目录中创建一个名为 `.env` 的新文件。

- `.env` 的内容结构应与 `.env.example` 相同。但是，请确保更新特定值。特别是：

  - 将 `OPENAI_API_KEY` 占位符替换为您的实际 API 密钥。
  - 将 `REDIS` 占位符替换为您的实际 Redis 密码。

**注意**：如果您打算在本地运行项目而不使用 Redis，请按照 `.env.example` 中给出的方式保持 `REDIS` 属性不变。

## 3. 运行代码

设置环境变量后，您可以执行以下命令在控制台环境下运行项目：

```
python moderator.py
```

如果希望能够在本地部署网页版项目，您可以运行如下的代码：

```
python app.py
```

## 为此存储库做出贡献

为了确保代码的一致性和质量，此存储库使用了 `pre-commit` 工具来自动格式化代码。在进行任何贡献或提交之前，建议您设置 `pre-commit`。

### 设置 `pre-commit`

1. **安装 `pre-commit`**：使用以下命令安装或升级 `pre-commit`：

   ```bash
   pip install -U pre-commit
   ```

2. **安装 Git 钩子**：安装 `pre-commit` 后，您需要为此存储库设置它。运行以下命令：

   ```bash
   pre-commit install
   ```

设置完成后，pre-commit 钩子将在每次提交之前自动检查并格式化您的更改。这有助于在整个项目中保持代码的一致性。

______________________________________________________________________

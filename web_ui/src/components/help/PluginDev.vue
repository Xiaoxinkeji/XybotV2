<template>
  <div class="plugin-dev">
    <h2>插件开发指南</h2>
    
    <div class="section">
      <h3>1. 插件结构</h3>
      <p>
        XyBotV2 的插件是一个包含以下文件的文件夹：
      </p>
      <ul class="plugin-files">
        <li>
          <i class="icon-folder"></i> 
          <span class="folder-name">YourPlugin</span>
          <ul>
            <li><i class="icon-file-text"></i> <code>__init__.py</code> - 插件入口点</li>
            <li><i class="icon-file-text"></i> <code>config.toml</code> - 插件配置文件</li>
            <li><i class="icon-file-text"></i> <code>main.py</code> - 插件主要逻辑</li>
            <li><i class="icon-file-text"></i> <code>README.md</code> - 插件文档（可选）</li>
          </ul>
        </li>
      </ul>
    </div>
    
    <div class="section">
      <h3>2. 创建新插件</h3>
      <p>
        以下是创建新插件的基本步骤：
      </p>
      <div class="code-examples">
        <div class="code-example">
          <h4>__init__.py</h4>
          <div class="code-block">
            <pre><code>from .main import YourPlugin

# 定义插件信息
plugin_info = {
    "name": "Your Plugin",
    "version": "1.0.0",
    "description": "A description of your plugin",
    "author": "Your Name",
    "dependencies": []
}

# 插件实例创建函数
def create_plugin(bot_instance):
    return YourPlugin(bot_instance)
</code></pre>
          </div>
        </div>
        
        <div class="code-example">
          <h4>main.py</h4>
          <div class="code-block">
            <pre><code>import logging
from XYBotV2.plugin import Plugin

class YourPlugin(Plugin):
    def __init__(self, bot):
        super().__init__(bot)
        self.logger = logging.getLogger(__name__)
        
    def on_enable(self):
        self.logger.info("YourPlugin enabled")
        # 插件启用时的逻辑
        return True
        
    def on_disable(self):
        self.logger.info("YourPlugin disabled")
        # 插件禁用时的逻辑
        return True
        
    def on_message(self, message):
        # 处理接收到的消息
        if message.content.startswith('/your_command'):
            # 执行命令逻辑
            return True  # 阻止其他插件处理此消息
        return False  # 允许其他插件继续处理
</code></pre>
          </div>
        </div>
        
        <div class="code-example">
          <h4>config.toml</h4>
          <div class="code-block">
            <pre><code># 插件配置示例
[settings]
option1 = "value1"
option2 = true
option3 = 123

[advanced]
feature_enabled = false
</code></pre>
          </div>
        </div>
      </div>
    </div>
    
    <div class="section">
      <h3>3. 插件生命周期</h3>
      <div class="lifecycle-diagram">
        <div class="lifecycle-step">
          <div class="step-icon load">
            <i class="icon-package"></i>
          </div>
          <div class="step-name">加载</div>
          <div class="step-desc">插件被发现并导入</div>
        </div>
        <div class="lifecycle-arrow"></div>
        <div class="lifecycle-step">
          <div class="step-icon enable">
            <i class="icon-power"></i>
          </div>
          <div class="step-name">启用</div>
          <div class="step-desc">调用 on_enable()</div>
        </div>
        <div class="lifecycle-arrow"></div>
        <div class="lifecycle-step">
          <div class="step-icon run">
            <i class="icon-play"></i>
          </div>
          <div class="step-name">运行</div>
          <div class="step-desc">响应事件和消息</div>
        </div>
        <div class="lifecycle-arrow"></div>
        <div class="lifecycle-step">
          <div class="step-icon disable">
            <i class="icon-power-off"></i>
          </div>
          <div class="step-name">禁用</div>
          <div class="step-desc">调用 on_disable()</div>
        </div>
        <div class="lifecycle-arrow"></div>
        <div class="lifecycle-step">
          <div class="step-icon unload">
            <i class="icon-trash-2"></i>
          </div>
          <div class="step-name">卸载</div>
          <div class="step-desc">从内存中移除</div>
        </div>
      </div>
    </div>
    
    <div class="section">
      <h3>4. API参考</h3>
      <p>
        XyBotV2 提供了丰富的API，您可以在插件中使用这些API与系统交互：
      </p>
      <div class="api-methods">
        <div class="api-method">
          <h4>消息发送</h4>
          <div class="code-block">
            <pre><code># 发送文本消息
self.bot.send_message(target, "Hello, world!")

# 发送图片消息
self.bot.send_image(target, "/path/to/image.jpg")

# 发送复合消息
from XYBotV2.message import Message, MessageSegment
msg = Message()
msg.append(MessageSegment.text("Hello"))
msg.append(MessageSegment.image("/path/to/image.jpg"))
self.bot.send_message(target, msg)</code></pre>
          </div>
        </div>
        
        <div class="api-method">
          <h4>定时任务</h4>
          <div class="code-block">
            <pre><code># 添加一次性任务，10秒后执行
self.bot.scheduler.add_once(self.your_function, seconds=10)

# 添加周期性任务，每小时执行一次
self.bot.scheduler.add_interval(self.your_function, hours=1)

# 添加定时任务，每天8点执行
self.bot.scheduler.add_cron(self.your_function, hour=8)</code></pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PluginDev',
}
</script>

<style scoped>
.plugin-dev {
  font-size: 14px;
  line-height: 1.6;
}

h2 {
  margin-top: 0;
  margin-bottom: 24px;
}

.section {
  margin-bottom: 32px;
}

h3 {
  font-size: 18px;
  margin-bottom: 16px;
  border-bottom: 1px solid #e1e5eb;
  padding-bottom: 8px;
}

code {
  background: #f1f5f9;
  padding: 2px 4px;
  border-radius: 4px;
  font-family: monospace;
}

.plugin-files {
  list-style: none;
  padding-left: 0;
}

.plugin-files ul {
  list-style: none;
  padding-left: 24px;
  margin-top: 8px;
}

.plugin-files li {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

.folder-name {
  font-weight: 600;
  margin-left: 6px;
}

.plugin-files i {
  color: #4361ee;
  margin-right: 6px;
}

.code-examples {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.code-example h4 {
  margin-top: 0;
  margin-bottom: 8px;
}

.code-block {
  background: #1a2236;
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
}

.code-block pre {
  margin: 0;
}

.code-block code {
  color: white;
  background: transparent;
  padding: 0;
  font-family: monospace;
}

.lifecycle-diagram {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 24px 0;
}

.lifecycle-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.step-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
  margin-bottom: 8px;
}

.step-icon.load {
  background: #4361ee;
}

.step-icon.enable {
  background: #10b981;
}

.step-icon.run {
  background: #3b82f6;
}

.step-icon.disable {
  background: #f59e0b;
}

.step-icon.unload {
  background: #ef4444;
}

.step-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.step-desc {
  font-size: 12px;
  color: #718096;
}

.lifecycle-arrow {
  width: 30px;
  height: 2px;
  background: #cbd5e1;
  position: relative;
}

.lifecycle-arrow:after {
  content: '';
  position: absolute;
  right: 0;
  top: -4px;
  border: 5px solid transparent;
  border-left-color: #cbd5e1;
}

.api-methods {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.api-method h4 {
  margin-top: 0;
  margin-bottom: 8px;
}
</style> 
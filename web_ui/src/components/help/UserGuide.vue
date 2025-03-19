<template>
  <div class="user-guide">
    <h2>XyBotV2 用户指南</h2>
    
    <div class="section">
      <h3>1. 基本概念</h3>
      <p>
        XyBotV2 是一个模块化、可扩展的聊天机器人框架，支持多种消息平台集成。通过插件系统，您可以轻松扩展机器人的功能。
      </p>
    </div>
    
    <div class="section">
      <h3>2. 快速开始</h3>
      <div class="steps">
        <div class="step">
          <div class="step-number">1</div>
          <div class="step-content">
            <h4>启动机器人</h4>
            <p>使用 <code>python main.py</code> 命令启动 XyBotV2。</p>
          </div>
        </div>
        
        <div class="step">
          <div class="step-number">2</div>
          <div class="step-content">
            <h4>访问控制面板</h4>
            <p>在浏览器中访问 <code>http://localhost:8080</code> 打开 Web 控制面板。</p>
          </div>
        </div>
        
        <div class="step">
          <div class="step-number">3</div>
          <div class="step-content">
            <h4>管理插件</h4>
            <p>在控制面板的"插件管理"页面启用或禁用插件。</p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="section">
      <h3>3. 配置机器人</h3>
      <p>
        机器人的主要配置在 <code>config.toml</code> 文件中，你可以通过控制面板的"系统设置"页面修改这些配置：
      </p>
      <div class="code-block">
        <pre><code># 示例配置
[general]
name = "XyBotV2"
log_level = "INFO"
auto_restart = true

[web_server]
enabled = true
port = 8080
</code></pre>
      </div>
    </div>
    
    <div class="section">
      <h3>4. 常见问题</h3>
      <div class="faq">
        <div class="faq-item">
          <div class="question">Q: 如何添加新插件？</div>
          <div class="answer">
            A: 将插件文件夹放入 <code>plugins</code> 目录，然后在控制面板启用它。
          </div>
        </div>
        
        <div class="faq-item">
          <div class="question">Q: 如何查看运行日志？</div>
          <div class="answer">
            A: 在控制面板的"运行日志"页面可以查看和过滤所有日志。
          </div>
        </div>
        
        <div class="faq-item">
          <div class="question">Q: 如何设置自动重启？</div>
          <div class="answer">
            A: 在"系统设置"中的"常规设置"选项卡中启用"自动重启"功能。
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserGuide',
}
</script>

<style scoped>
.user-guide {
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

.steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.step-number {
  width: 32px;
  height: 32px;
  background: #4361ee;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h4 {
  margin-top: 0;
  margin-bottom: 8px;
}

.step-content p {
  margin: 0;
  color: #4a5568;
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

.faq {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.faq-item {
  background: #f7fafc;
  padding: 16px;
  border-radius: 6px;
}

.question {
  font-weight: 600;
  margin-bottom: 8px;
  color: #1a202c;
}

.answer {
  color: #4a5568;
}
</style> 
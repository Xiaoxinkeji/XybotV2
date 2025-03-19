<template>
  <div class="troubleshooting">
    <h2>故障排除指南</h2>
    
    <div class="section">
      <h3>常见问题</h3>
      
      <div class="issue">
        <div class="issue-header">
          <div class="issue-title">
            <i class="icon-alert-circle"></i> 机器人无法启动
          </div>
        </div>
        <div class="issue-content">
          <p>如果机器人无法启动，请检查以下几点：</p>
          <ol>
            <li>确保已安装所有必要的依赖项 (<code>pip install -r requirements.txt</code>)</li>
            <li>检查 <code>config.toml</code> 文件是否存在格式错误</li>
            <li>检查日志文件，查找具体错误信息</li>
            <li>确保系统具有足够的资源（内存、磁盘空间）</li>
          </ol>
        </div>
      </div>
      
      <div class="issue">
        <div class="issue-header">
          <div class="issue-title">
            <i class="icon-alert-circle"></i> 插件加载失败
          </div>
        </div>
        <div class="issue-content">
          <p>插件加载失败可能有以下原因：</p>
          <ol>
            <li>插件代码存在语法错误</li>
            <li>插件依赖项未满足</li>
            <li>插件与当前版本的XyBotV2不兼容</li>
            <li>插件配置文件格式错误</li>
          </ol>
          <p>解决方法：</p>
          <ol>
            <li>查看日志文件中的详细错误信息</li>
            <li>在控制台运行时添加 <code>--debug</code> 参数获取更详细的日志</li>
            <li>修复插件代码中的错误或联系插件作者</li>
          </ol>
        </div>
      </div>
      
      <div class="issue">
        <div class="issue-header">
          <div class="issue-title">
            <i class="icon-alert-circle"></i> Web界面无法访问
          </div>
        </div>
        <div class="issue-content">
          <p>如果无法访问Web管理界面，请检查：</p>
          <ol>
            <li>确认Web服务器已在配置中启用</li>
            <li>检查防火墙设置，确保端口已开放</li>
            <li>验证服务器IP地址和端口号是否正确</li>
            <li>检查服务器日志中是否有相关错误信息</li>
          </ol>
        </div>
      </div>
    </div>
    
    <div class="section">
      <h3>日志分析</h3>
      <p>日志是排除故障的重要工具。XyBotV2的日志位于 <code>logs</code> 目录中。</p>
      
      <div class="log-levels">
        <div class="log-level">
          <div class="level-badge debug">DEBUG</div>
          <div class="level-desc">调试信息，开发时使用</div>
        </div>
        <div class="log-level">
          <div class="level-badge info">INFO</div>
          <div class="level-desc">一般信息，系统正常运行</div>
        </div>
        <div class="log-level">
          <div class="level-badge warning">WARNING</div>
          <div class="level-desc">警告信息，潜在问题</div>
        </div>
        <div class="log-level">
          <div class="level-badge error">ERROR</div>
          <div class="level-desc">错误信息，功能失效</div>
        </div>
        <div class="log-level">
          <div class="level-badge critical">CRITICAL</div>
          <div class="level-desc">严重错误，系统可能崩溃</div>
        </div>
      </div>
    </div>
    
    <div class="section">
      <h3>支持渠道</h3>
      <p>如果您无法解决问题，可以通过以下渠道获取支持：</p>
      
      <div class="support-channels">
        <div class="support-channel">
          <i class="icon-github"></i>
          <div class="channel-info">
            <div class="channel-name">GitHub Issues</div>
            <div class="channel-desc">
              <a href="https://github.com/your-repository/issues" target="_blank">报告问题或功能建议</a>
            </div>
          </div>
        </div>
        
        <div class="support-channel">
          <i class="icon-mail"></i>
          <div class="channel-info">
            <div class="channel-name">电子邮件</div>
            <div class="channel-desc">
              <a href="mailto:support@example.com">support@example.com</a>
            </div>
          </div>
        </div>
        
        <div class="support-channel">
          <i class="icon-message-circle"></i>
          <div class="channel-info">
            <div class="channel-name">社区讨论组</div>
            <div class="channel-desc">
              加入我们的<a href="#" target="_blank">讨论群组</a>获取社区支持
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Troubleshooting',
}
</script>

<style scoped>
.troubleshooting {
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

.issue {
  margin-bottom: 16px;
  border: 1px solid #e1e5eb;
  border-radius: 6px;
  overflow: hidden;
}

.issue-header {
  padding: 12px 16px;
  background: #f8fafc;
  border-bottom: 1px solid #e1e5eb;
}

.issue-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.issue-title i {
  color: #ef4444;
}

.issue-content {
  padding: 16px;
}

.issue-content p {
  margin-top: 0;
  margin-bottom: 12px;
}

.issue-content ol {
  margin-top: 0;
  padding-left: 20px;
}

.issue-content li {
  margin-bottom: 4px;
}

.log-levels {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}

.log-level {
  display: flex;
  align-items: center;
  gap: 12px;
}

.level-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  width: 80px;
  text-align: center;
}

.level-badge.debug {
  background: #f1f5f9;
  color: #64748b;
}

.level-badge.info {
  background: #e0f2fe;
  color: #0284c7;
}

.level-badge.warning {
  background: #fef3c7;
  color: #d97706;
}

.level-badge.error {
  background: #fee2e2;
  color: #dc2626;
}

.level-badge.critical {
  background: #fae8ff;
  color: #a855f7;
}

.level-desc {
  font-size: 14px;
  color: #4b5563;
}

.support-channels {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}

.support-channel {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 6px;
}

.support-channel i {
  font-size: 24px;
  color: #4361ee;
}

.channel-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.channel-desc {
  font-size: 14px;
  color: #4b5563;
}

a {
  color: #4361ee;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style> 
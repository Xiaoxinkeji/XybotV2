<template>
  <div class="api-reference">
    <h2>API参考文档</h2>
    <p class="intro">
      本文档提供XyBotV2 REST API的详细说明，您可以使用这些API与机器人进行交互。
    </p>
    
    <div class="api-section">
      <h3>基础信息</h3>
      <p>所有API请求都使用HTTP协议，基础URL为：<code>http://your-server:8080/api</code></p>
      <p>响应格式统一为JSON格式。</p>
    </div>
    
    <div class="api-section">
      <h3>认证</h3>
      <p>如果启用了访问控制，需要在请求头中添加以下认证信息：</p>
      <pre><code>Authorization: Bearer YOUR_API_TOKEN</code></pre>
    </div>
    
    <div class="api-section">
      <h3>端点列表</h3>
      
      <div class="endpoint" v-for="endpoint in endpoints" :key="endpoint.path">
        <div class="endpoint-header" @click="endpoint.expanded = !endpoint.expanded">
          <div class="method" :class="endpoint.method.toLowerCase()">{{ endpoint.method }}</div>
          <div class="path">{{ endpoint.path }}</div>
          <div class="description">{{ endpoint.description }}</div>
          <i :class="endpoint.expanded ? 'icon-chevron-up' : 'icon-chevron-down'"></i>
        </div>
        
        <div class="endpoint-details" v-if="endpoint.expanded">
          <div class="params" v-if="endpoint.params && endpoint.params.length">
            <h4>参数</h4>
            <table>
              <thead>
                <tr>
                  <th>名称</th>
                  <th>类型</th>
                  <th>必填</th>
                  <th>描述</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="param in endpoint.params" :key="param.name">
                  <td>{{ param.name }}</td>
                  <td>{{ param.type }}</td>
                  <td>{{ param.required ? '是' : '否' }}</td>
                  <td>{{ param.description }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="response">
            <h4>响应示例</h4>
            <pre><code>{{ endpoint.response }}</code></pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApiReference',
  data() {
    return {
      endpoints: [
        {
          method: 'GET',
          path: '/status',
          description: '获取机器人状态',
          expanded: false,
          response: JSON.stringify({
            online: true,
            uptime: 3600,
            version: '1.0.0',
            lastActivity: '2023-09-01T12:00:00Z'
          }, null, 2)
        },
        {
          method: 'GET',
          path: '/plugins',
          description: '获取所有插件列表',
          expanded: false,
          response: JSON.stringify([
            {
              id: 'BotStatusPush',
              name: '机器人状态推送',
              description: '定时推送机器人状态信息',
              version: '1.0.0',
              author: 'XyBot Team',
              enabled: true
            }
          ], null, 2)
        },
        {
          method: 'POST',
          path: '/plugins/{plugin_id}/toggle',
          description: '启用或禁用插件',
          expanded: false,
          params: [
            {
              name: 'enable',
              type: 'Boolean',
              required: true,
              description: 'true表示启用，false表示禁用'
            }
          ],
          response: JSON.stringify({
            success: true,
            plugin_id: 'BotStatusPush',
            enabled: true
          }, null, 2)
        },
        {
          method: 'GET',
          path: '/messages/recent',
          description: '获取最近消息',
          expanded: false,
          params: [
            {
              name: 'limit',
              type: 'Integer',
              required: false,
              description: '返回的消息数量，默认20'
            }
          ],
          response: JSON.stringify([
            {
              id: '12345',
              type: 'received',
              sender: 'user123',
              content: '你好，机器人',
              timestamp: '2023-09-01T12:00:00Z'
            }
          ], null, 2)
        },
        {
          method: 'GET',
          path: '/system/info',
          description: '获取系统信息',
          expanded: false,
          response: JSON.stringify({
            cpu: {
              percent: 25.5,
              cores: 4
            },
            memory: {
              total: 8589934592,
              available: 4294967296,
              percent: 50
            },
            disk: {
              total: 107374182400,
              free: 53687091200,
              percent: 50
            },
            platform: {
              system: 'Linux',
              release: '5.4.0',
              version: '#1 SMP'
            },
            python: '3.9.5'
          }, null, 2)
        }
      ]
    };
  }
}
</script>

<style scoped>
.api-reference {
  font-size: 14px;
  line-height: 1.5;
}

.intro {
  margin-bottom: 24px;
  color: #4a5568;
}

.api-section {
  margin-bottom: 32px;
}

h2 {
  margin-top: 0;
  margin-bottom: 16px;
}

h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 18px;
  border-bottom: 1px solid #e1e5eb;
  padding-bottom: 8px;
}

pre {
  background: #f7fafc;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
}

code {
  font-family: monospace;
}

.endpoint {
  margin-bottom: 16px;
  border: 1px solid #e1e5eb;
  border-radius: 4px;
  overflow: hidden;
}

.endpoint-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: #f7fafc;
  cursor: pointer;
}

.method {
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 4px;
  margin-right: 12px;
  min-width: 60px;
  text-align: center;
  font-size: 12px;
}

.method.get {
  background: #ebf8ff;
  color: #3182ce;
}

.method.post {
  background: #e6fffa;
  color: #319795;
}

.method.put {
  background: #fffbeb;
  color: #d97706;
}

.method.delete {
  background: #fef2f2;
  color: #dc2626;
}

.path {
  font-family: monospace;
  margin-right: 16px;
  min-width: 200px;
}

.description {
  flex: 1;
  color: #4a5568;
}

.endpoint-details {
  padding: 16px;
  border-top: 1px solid #e1e5eb;
}

.params, .response {
  margin-bottom: 16px;
}

h4 {
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 14px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid #e1e5eb;
}

th {
  background: #f7fafc;
  font-weight: 600;
}
</style> 
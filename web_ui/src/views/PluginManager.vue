<template>
  <div class="plugin-manager">
    <div class="page-header">
      <h1>插件管理</h1>
      <div class="header-actions">
        <div class="search-filter">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索插件..." 
            class="search-input"
          />
        </div>
        
        <button @click="refreshPlugins" class="btn btn-outline">
          <i class="icon-refresh"></i> 刷新列表
        </button>
      </div>
    </div>
    
    <div class="plugins-grid" v-if="!isLoading">
      <plugin-card 
        v-for="plugin in filteredPlugins" 
        :key="plugin.id"
        :plugin="plugin"
        @toggle="togglePlugin"
        @view-config="openConfigEditor"
      />
    </div>
    
    <div class="loading-state" v-else>
      <div class="spinner"></div>
      <p>加载插件中...</p>
    </div>
    
    <!-- 配置编辑器模态框 -->
    <modal v-if="showConfigEditor" @close="showConfigEditor = false">
      <template #header>
        <h3>编辑插件配置: {{ currentPlugin.name }}</h3>
      </template>
      
      <template #body>
        <div class="config-editor">
          <code-editor 
            v-model="configContent"
            language="toml"
            :options="editorOptions"
          />
        </div>
      </template>
      
      <template #footer>
        <button @click="showConfigEditor = false" class="btn btn-outline">取消</button>
        <button @click="savePluginConfig" class="btn btn-primary">保存配置</button>
      </template>
    </modal>
  </div>
</template>

<script>
import PluginCard from '@/components/plugins/PluginCard.vue';
import Modal from '@/components/ui/Modal.vue';
import CodeEditor from '@/components/ui/CodeEditor.vue';
import { getPlugins, togglePlugin, getPluginConfig, savePluginConfig } from '@/api/plugins';

export default {
  name: 'PluginManager',
  components: {
    PluginCard,
    Modal,
    CodeEditor
  },
  data() {
    return {
      plugins: [],
      isLoading: true,
      searchQuery: '',
      showConfigEditor: false,
      currentPlugin: null,
      configContent: '',
      editorOptions: {
        theme: 'vs-light',
        fontSize: 14,
        wordWrap: 'on',
        minimap: { enabled: false }
      }
    };
  },
  computed: {
    filteredPlugins() {
      if (!this.searchQuery) return this.plugins;
      
      const query = this.searchQuery.toLowerCase();
      return this.plugins.filter(plugin => 
        plugin.name.toLowerCase().includes(query) || 
        plugin.description.toLowerCase().includes(query) ||
        plugin.author.toLowerCase().includes(query)
      );
    }
  },
  methods: {
    async fetchPlugins() {
      this.isLoading = true;
      try {
        this.plugins = await getPlugins();
      } catch (error) {
        console.error('获取插件列表失败:', error);
        this.$toast.error('获取插件列表失败');
      } finally {
        this.isLoading = false;
      }
    },
    async togglePlugin(plugin) {
      try {
        await togglePlugin(plugin.id, !plugin.enabled);
        
        // 更新本地状态
        const index = this.plugins.findIndex(p => p.id === plugin.id);
        if (index !== -1) {
          this.plugins[index].enabled = !plugin.enabled;
        }
        
        this.$toast.success(`插件 "${plugin.name}" 已${plugin.enabled ? '禁用' : '启用'}`);
      } catch (error) {
        console.error('切换插件状态失败:', error);
        this.$toast.error(`切换插件状态失败: ${error.message}`);
      }
    },
    async openConfigEditor(plugin) {
      this.currentPlugin = plugin;
      this.showConfigEditor = true;
      this.isLoading = true;
      
      try {
        this.configContent = await getPluginConfig(plugin.id);
      } catch (error) {
        console.error('获取插件配置失败:', error);
        this.$toast.error(`获取插件配置失败: ${error.message}`);
      } finally {
        this.isLoading = false;
      }
    },
    async savePluginConfig() {
      if (!this.currentPlugin) return;
      
      try {
        await savePluginConfig(this.currentPlugin.id, this.configContent);
        this.showConfigEditor = false;
        this.$toast.success('配置保存成功');
      } catch (error) {
        console.error('保存插件配置失败:', error);
        this.$toast.error(`保存插件配置失败: ${error.message}`);
      }
    },
    refreshPlugins() {
      this.fetchPlugins();
      this.$toast.info('正在刷新插件列表');
    }
  },
  created() {
    this.fetchPlugins();
  }
}
</script>

<style scoped>
.plugin-manager {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #e1e5eb;
  border-radius: 4px;
  min-width: 240px;
}

.plugins-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #4361ee;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.config-editor {
  height: 400px;
  border: 1px solid #e1e5eb;
  border-radius: 4px;
  overflow: hidden;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-outline {
  background: transparent;
  border: 1px solid #e1e5eb;
  color: #4a5568;
}

.btn-primary {
  background: #4361ee;
  border: 1px solid #4361ee;
  color: white;
}
</style> 
<template>
  <div 
    class="log-entry" 
    :class="[source.level.toLowerCase(), { expanded: expanded }]" 
    @click="toggleExpand"
  >
    <div class="entry-main">
      <div class="entry-level">
        <div class="level-indicator" :class="source.level.toLowerCase()"></div>
        <span class="level-text">{{ source.level }}</span>
      </div>
      
      <div class="entry-timestamp">{{ formattedTime }}</div>
      
      <div class="entry-message">{{ truncatedMessage }}</div>
      
      <div class="entry-actions">
        <button class="btn-icon" @click.stop="viewDetails">
          <i class="icon-info"></i>
        </button>
      </div>
    </div>
    
    <div class="entry-details" v-if="expanded">
      <pre class="message-full">{{ source.message }}</pre>
      
      <div class="metadata" v-if="source.metadata">
        <h4>元数据</h4>
        <pre>{{ JSON.stringify(source.metadata, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LogEntry',
  props: {
    source: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      expanded: false
    };
  },
  computed: {
    formattedTime() {
      const date = new Date(this.source.timestamp);
      return date.toLocaleTimeString();
    },
    truncatedMessage() {
      const maxLength = 100;
      if (this.source.message.length > maxLength) {
        return this.source.message.substring(0, maxLength) + '...';
      }
      return this.source.message;
    }
  },
  methods: {
    toggleExpand() {
      this.expanded = !this.expanded;
    },
    viewDetails() {
      this.$parent.$parent.$parent.viewLogDetail(this.source);
    }
  }
}
</script>

<style scoped>
.log-entry {
  border-bottom: 1px solid #e1e5eb;
  cursor: pointer;
  transition: all 0.2s;
}

.log-entry:hover {
  background: #f5f7fa;
}

.log-entry.expanded {
  background: #f9fafc;
}

.entry-main {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  gap: 16px;
}

.entry-level {
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 80px;
}

.level-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.level-indicator.debug {
  background: #718096;
}

.level-indicator.info {
  background: #3182ce;
}

.level-indicator.warning {
  background: #d97706;
}

.level-indicator.error {
  background: #dc2626;
}

.level-indicator.critical {
  background: #9333ea;
}

.level-text {
  font-size: 12px;
  font-weight: 500;
}

.entry-timestamp {
  color: #8b9cb3;
  font-size: 12px;
  min-width: 100px;
}

.entry-message {
  flex: 1;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.entry-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  color: #8b9cb3;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}

.btn-icon:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #4a5568;
}

.entry-details {
  padding: 0 16px 16px;
  font-size: 14px;
  color: #4a5568;
}

.message-full {
  white-space: pre-wrap;
  background: #f1f5f9;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.metadata h4 {
  margin-bottom: 8px;
  font-size: 14px;
}

.metadata pre {
  background: #f1f5f9;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
  font-family: monospace;
}
</style> 
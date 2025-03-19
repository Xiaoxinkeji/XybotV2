<template>
  <div class="code-editor-container">
    <MonacoEditor
      v-model="code"
      :language="language"
      :options="editorOptions"
      @change="updateValue"
    />
  </div>
</template>

<script>
import MonacoEditor from 'monaco-editor-vue';

export default {
  name: 'CodeEditor',
  components: {
    MonacoEditor
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    language: {
      type: String,
      default: 'javascript'
    },
    options: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      code: this.value
    };
  },
  computed: {
    editorOptions() {
      return {
        theme: 'vs',
        fontSize: 14,
        tabSize: 2,
        minimap: { enabled: true },
        scrollBeyondLastLine: false,
        automaticLayout: true,
        ...this.options
      };
    }
  },
  watch: {
    value(newValue) {
      if (newValue !== this.code) {
        this.code = newValue;
      }
    }
  },
  methods: {
    updateValue(val) {
      this.$emit('input', val);
    }
  }
}
</script>

<style scoped>
.code-editor-container {
  width: 100%;
  height: 100%;
}
</style> 
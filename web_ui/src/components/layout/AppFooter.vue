<template>
  <footer class="footer">
    <div>
      <span class="copyright">© {{ currentYear }} XyBotV2 管理平台</span>
    </div>
    <div class="version">
      <span>版本 {{ version }}</span>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter',
  data() {
    return {
      version: '1.0.0'
    }
  },
  computed: {
    currentYear() {
      return new Date().getFullYear();
    }
  }
}
</script>

<style scoped>
.footer {
  height: 50px;
  background: white;
  border-top: 1px solid #e1e5eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  font-size: 14px;
  color: #8b9cb3;
}

.copyright, .version {
  font-size: 12px;
}
</style> 
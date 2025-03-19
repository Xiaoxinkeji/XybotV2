<template>
  <nav class="top-nav">
    <!-- 其他导航元素... -->
    
    <div class="nav-right">
      <!-- 添加主题切换按钮 -->
      <theme-toggle />
      
      <!-- 其他右侧导航元素... -->
    </div>
  </nav>
</template>

<script>
import ThemeToggle from '@/components/ui/ThemeToggle.vue';

export default {
  components: {
    ThemeToggle,
    // 其他组件...
  },
  // 其他代码...
}
</script> 
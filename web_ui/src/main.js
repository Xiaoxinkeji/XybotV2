import Vue from 'vue';
import App from './App.vue';
import router from './router';
import { setupAuthInterceptors } from './api/auth';

Vue.config.productionTip = false;

// 设置认证拦截器
setupAuthInterceptors(router);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app'); 
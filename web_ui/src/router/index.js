import Vue from 'vue';
import VueRouter from 'vue-router';
import { isAuthenticated } from '@/utils/auth';

// 页面组件
import Dashboard from '@/views/Dashboard.vue';
import PluginManager from '@/views/PluginManager.vue';
import MessageLogs from '@/views/MessageLogs.vue';
import Settings from '@/views/Settings.vue';
import LogViewer from '@/views/LogViewer.vue';
import Help from '@/views/Help.vue';
import Login from '@/views/Login.vue';
import NotFound from '@/views/NotFound.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/plugins',
    name: 'PluginManager',
    component: PluginManager,
    meta: { requiresAuth: true }
  },
  {
    path: '/messages',
    name: 'Messages',
    component: MessageLogs,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true }
  },
  {
    path: '/logs',
    name: 'LogViewer',
    component: LogViewer,
    meta: { requiresAuth: true }
  },
  {
    path: '/help',
    name: 'Help',
    component: Help,
    meta: { requiresAuth: true }
  },
  {
    path: '*',
    redirect: '/dashboard'
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

// 全局前置守卫
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false);
  
  if (requiresAuth && !isAuthenticated()) {
    // 需要认证但未登录，重定向到登录页
    next({
      path: '/login',
      query: { redirect: to.fullPath }  // 保存尝试访问的路径
    });
  } else {
    // 已登录或不需要认证的页面
    next();
  }
});

export default router; 
/**
 * 认证工具函数
 */

// 保存认证信息到本地存储
export const saveAuth = (authData) => {
  if (authData && authData.token) {
    localStorage.setItem('auth_token', authData.token);
    localStorage.setItem('auth_user', JSON.stringify({
      username: authData.username,
      role: authData.role
    }));
    return true;
  }
  return false;
};

// 从本地存储获取认证信息
export const getAuth = () => {
  const token = localStorage.getItem('auth_token');
  const userStr = localStorage.getItem('auth_user');
  
  if (!token || !userStr) {
    return null;
  }
  
  try {
    const user = JSON.parse(userStr);
    return {
      token,
      ...user
    };
  } catch (e) {
    clearAuth();
    return null;
  }
};

// 清除认证信息
export const clearAuth = () => {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('auth_user');
};

// 检查是否已认证
export const isAuthenticated = () => {
  return !!getAuth();
};

// 获取当前用户角色
export const getUserRole = () => {
  const auth = getAuth();
  return auth ? auth.role : null;
};

// 检查用户是否有特定权限
export const hasPermission = (requiredRole) => {
  const role = getUserRole();
  
  if (!role) return false;
  if (role === 'admin') return true;
  
  // 简单角色检查，可扩展为更复杂的权限系统
  if (requiredRole === 'admin') return role === 'admin';
  if (requiredRole === 'user') return ['admin', 'user'].includes(role);
  
  return false;
}; 
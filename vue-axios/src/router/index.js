// 导入vue构造函数
import Vue from 'vue'
// 导入vue-router
import VueRouter from 'vue-router'

// 使用VueRouter插件
Vue.use(VueRouter)

// 配置路由映射，创建路径与组件的映射关系
const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home.vue')
  }
]

// 创建路由实例
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// 导出路由实例
export default router

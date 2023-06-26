// 导入vue构造函数
import Vue from 'vue'
// 导入根组件App.vue
import App from './App.vue'
// 导入路由文件
import router from './router'
// 导入axios的二次封装
import request from "@/utils/request"
// 导入element-ui
import ElementUI from 'element-ui';
// 导入element-ui的样式
import 'element-ui/lib/theme-chalk/index.css';

// 关闭生产模式下的提示
Vue.config.productionTip = false

// 设置axios为Vue的原型属性
Vue.prototype.$axios = request

// 全局引入ElementUI
Vue.use(ElementUI);

// 挂载到Vue实例上
new Vue({
  router,
  render: function (h) { return h(App) }
}).$mount('#app')

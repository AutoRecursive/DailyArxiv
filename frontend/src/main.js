import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { router } from './router'
import App from './App.vue'
import './assets/styles/main.scss'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// 初始化主题
const theme = localStorage.getItem('theme') || 'light'
document.documentElement.className = `theme-${theme}`

app.mount('#app')

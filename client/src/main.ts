import { createApp } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import './style.css'

import App from './App.vue'
import Home from './components/Home.vue'
import NavBar from './components/NavBar.vue'

const routes: any = [
    {
        path: '/',
        components: {
            default: Home,
            NavBar
        }
    }
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

const app = createApp(App)
app.use(router)
app.mount('#app')
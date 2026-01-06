import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import ApiList from '../views/ApiList.vue'
import ApiDetail from '../views/ApiDetail.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/apis', component: ApiList },
  { path: '/apis/:id', component: ApiDetail },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

<template>
  <div class="card">
    <h1>欢迎来到 Woody API 系统</h1>
    <p>本系统提供安全高效的 API 服务管理与访问功能。</p>
    <p>请 <router-link to="/login">登录</router-link> 或 <router-link to="/register">注册</router-link> 以开始使用。</p>
    <div style="margin-top: 2rem; text-align: center;">
      <router-link to="/apis">
        <button style="padding: 1rem 2rem; font-size: 1.2rem;">浏览 API</button>
      </router-link>
    </div>
  </div>
</template>

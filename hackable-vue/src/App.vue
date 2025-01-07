<template>
  <div id="app">
    <header>
      <div class="wrapper">
        <nav>
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/posts">Posts</RouterLink>
          <RouterLink to="/walkthrough">Vulnerabilities Walkthrough</RouterLink>
        </nav>
      </div>
    </header>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HomeView from './views/HomeView.vue'
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100vw;
}

header {
  line-height: 1.5;
  width: 100%;
  background: var(--color-background, #f8f9fa);
  padding: 1rem 0;
  border-bottom: 1px solid var(--color-border, #ddd);
}

header .wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

nav {
  font-size: 14px;
  text-align: center;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border, #ddd);
  text-decoration: none;
  color: var(--color-text, #333);
}

nav a:first-of-type {
  border: none;
}

nav a.router-link-exact-active {
  font-weight: bold;
  color: var(--color-primary, #42b983);
}

main {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
</style>

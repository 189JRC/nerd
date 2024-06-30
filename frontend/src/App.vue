<script setup>
import { reactive } from 'vue';
import HelloWorld from './components/HelloWorld.vue'
import EntryPoint from './components/EntryPoint.vue'

import Investigation from '../js/Investigation';

let domain_origin = window.location.origin
if (domain_origin.slice(-5) == ":3001") {
  domain_origin = domain_origin.replace(":3001", ":5000")
}

const investigation = reactive(new Investigation(domain_origin))
</script>

<template>
  <!-- <div class="mt-5 p-6 max-w-sm mx-auto dark:bg-gray-00 rounded-xl shadow-md flex items-center space-x-4">
  <h1 class="text-white text-4xl">Named Entity Recognition Diagramiser</h1>
  </div>
  <br> -->
  <EntryPoint :investigation="investigation"/>
  
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>

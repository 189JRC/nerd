<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)
</script>

<template>
  <div><h1 class="mb-2 text-xl font-medium dark:text-gray-300 text-center">{{ msg }}</h1></div>
  <hr class="mb-3 dark:text-gray-500">
  <div class="flex justify-between items-center space-x-5">
    
    <div>
      <button type="button" @click="count++"
        class="ml-0 bg-yellow-500 text-black font-bold py-2 px-4 rounded dark:bg-yellow-600">
        {{ count }}
      </button>
    </div>
    <div class="dark:text-gray-300">
      <code>This is the HelloWorld.vue component</code> 
    </div>
  </div>
  
</template>


<style scoped>
.read-the-docs {
  color: #888;
}
</style>

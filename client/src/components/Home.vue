<script setup lang="ts">
  import HomeInfo from './HomeInfo.vue';
</script>

<template>
  <Suspense>
    <template #fallback>
      <div>Loading...</div>
    </template>
    <template #default>
      <HomeInfo />
    </template>
  </Suspense>

</template>

<style>
  #container {
    height: 100%;
    background-color: green;
    display: flex;
    flex-direction: column;
    margin-left: 100px;
    margin-right: 100px;
}

#container > * {
    color: white;
}
</style>
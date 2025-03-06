<script setup lang="ts">
async function fetchName() {
    const response = await fetch("http://localhost:8000/users/c5f614d0-657e-4fd4-ae3b-05890216a832")
    const result = await response.json()
    return await result.username
  }
  const Name = await fetchName()
</script>

<template>
    <div id="container">
        <p>{{ Name }}</p>
    </div>
</template>

<style>

</style>
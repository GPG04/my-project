<script setup lang="ts">

</script>

<template>
    <nav id="NavContainer">
        <RouterLink to="/">Home</RouterLink>
    </nav>
</template>

<style>
    #NavContainer {
        display: flex;
        background-color: green;
    }

    #NavContainer > * {
        color: white;
    }
</style>
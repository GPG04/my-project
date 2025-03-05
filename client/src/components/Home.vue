<template>

    <div id="container">
        <p>{{ message }}</p>
    </div>

</template>

<script lang="ts">

export default {
    
    data() {
      return {
        message: "",
      };
    },
    
      mounted() {
        fetch("http://localhost:8000/users")
        .then(response => response.text())
        .then(data => {
          this.message = data;
        });
    },
    
    };

</script>
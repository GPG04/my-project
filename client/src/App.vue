<template>

  <div>
    <h1>{{ message }}</h1>
  </div>
  
  </template>
  
  <script>
  
  export default {
    
  data() {
    return {
      message: "",
    };
  },
  
    mounted() {
      fetch("http://localhost:8000/")
      .then(response => response.text())
      .then(data => {
        this.message = data;
      });
  },
  
  };
  
  </script>
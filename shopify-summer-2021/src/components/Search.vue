<template>
  <div>
    <h2 class="is-size-2">Search</h2>
    <div class="level is-3">
      <input
        class="input is-medium"
        type="text"
        placeholder="Enter relevant keywords for image or click the button to upload images"
      />
      <button class="button is-light is-medium">Search</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Search",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.level {
  padding: 0 2rem 0.5rem 2rem;
}

.input {
  margin-right: 1rem;
}

.is-size-2 {
  margin-top: 1rem;
}
</style>

<template>
  <div class="parent">
    <h1 class="is-size-2">Search</h1>
    <div class="level">
      <input
        class="file input is-medium"
        type="text"
        placeholder="Enter relevant keywords for image "
      />
      <button class="button is-light is-medium">Search</button>
    </div>
  </div>
</template>

<script>
export default { name: "Search" };
</script>
<style scoped>
.level {
  margin-left: 2rem;
  margin-right: 2rem;
}
.button {
  margin-left: 2rem;
}
.parent {
  margin-top: 3rem;
}
</style>
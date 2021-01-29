<template>
  <div class="parent">
    <h1 class="is-size-2">Search</h1>
    <div class="level">
      <input
        class="file input is-medium"
        type="text"
        placeholder="Enter relevant keywords for image and we will show the top 5 images "
      />
      <button class="button is-light is-medium">Search</button>
    </div>
    <div class="control">
      <label class="radio">
        <input type="radio" id="public" value="Public" v-model="permissions" />
        Public
      </label>
      <label class="radio">
        <input type="radio" id="private" value="Private" v-model="permissions" />
        Private
      </label>
    </div>
  </div>
</template>

<script>
export default {
  name: "Search",
  data() {
    {
      return { permissions: "" };
    }
  }
};
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
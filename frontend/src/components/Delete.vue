<template>
  <div>
    <h1 class="is-size-2">Delete</h1>
    <div class="level">
      <button v-on:click="foo" class="button is-light is-medium">Show my images to delete</button>
    </div>
  </div>
</template>


<script>
export default {
  name: "Delete",
  data() {
    return {};
  },
  props: { email: String },
  methods: {
    foo: function() {
      return 0;
    }
  }
};
</script>


<style scoped>
.level {
  justify-content: center;
  margin-bottom: 2rem;
}
</style>
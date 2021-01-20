<template>
  <div class="hello">
    <h1 class="is-size-1">{{ msg }}</h1>
    <Add />
    <Search />
  </div>
</template>

<script>
import Add from "./Add";
import Search from "./Search";
export default {
  name: "HelloWorld",
  props: {
    msg: String
  },
  components: {
    Add,
    Search
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

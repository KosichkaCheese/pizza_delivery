<template>
    <button class="button-white"  @click="handleClick(click)">
        <span class="button-white__title">{{ title }}</span>
    </button>
</template>

<script>
export default {
    name: 'VButtonWhite',
    props: {
        title: String,
        click: String,
    },
    methods:{
      handleClick(method){
        this.$emit(method);
      }
    }
  }
</script>
<style scoped>
.button-white{
  border: solid 4px #BF0200;
  background-color: #FFF9ED;
  text-align: center;
  border-radius: 25px;
  padding: 6px 20px;
  height: fit-content;
  margin-top: 15px;
}
.button-white__title{
  font-family: Nunito;
  font-size: 1.5rem;
  color: #BF0200;
  font-weight: 500;
}
</style>

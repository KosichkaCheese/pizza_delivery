<template>
    <div class="button-white">
        <span class="button-white__title">{{ title }}</span>
    </div>
</template>

<script>
export default {
    name: 'VButtonWhite',
    props: {
        title: String
    }
  }
</script>
<style scoped>
.button-white{
  border: solid 4px #BF0200;
  background-color: #FFF9ED;
  width:fit-content;
  text-align: center;
  border-radius: 25px;
  padding: 4px 20px;
  margin-top: 15px;
}
.button-white__title{
  font-family: Nunito;
  font-size: 1.5rem;
  color: #BF0200;
  font-weight: 500;
}
</style>

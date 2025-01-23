<template>
    <button class="button-red" @click="$emit('addToBasket')">
        <span class="button-red__title">{{ title }}</span>
    </button>
</template>

<script>
export default {
    name: 'VButtonRed',
    props: {
        title: String
    }
  }
</script>
<style scoped>
/*стили надо жестко редачить думать чета блин  */
.button-red{
  background-color: #BF0200;
  /* width: 100%; */
  text-align: center;
  border-radius: 25px;
  padding: 8px 20px;
  margin-top: 15px;
  border: none;
}
.button-red__title{
  font-family: Nunito;
  font-size: 1.5rem;
  color: #FFF9ED;
  font-weight: 300;
}
</style>

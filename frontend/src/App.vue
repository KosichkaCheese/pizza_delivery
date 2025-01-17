<template>
    <RouterView></RouterView>
</template>

<script>

export default {
  name: 'App',
}
</script>

<style>
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 800;
  src: url(./assets/Nunito-Black.ttf) format('truetype');
}
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 500;
  src: url(./assets/Nunito-Bold.ttf) format('truetype');
}
@font-face {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 300;
  src: url(./assets/Nunito-SemiBold.ttf) format('truetype');
}
body {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  /* text-align: center; */
  background-color: #FFF9ED;
}
#app{
  width: 100%;
  height: 100%;
  
}
</style>

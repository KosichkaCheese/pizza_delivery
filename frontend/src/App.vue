<template>
  <div id="app">
    <div class="page__header">
      <div class="lk_button">
        <LkSVG></LkSVG>
      </div>
      <LogoSVG></LogoSVG>
      <div class="busket_button">
        <BusketSVG></BusketSVG>
      </div>
    </div>
    <div class="page__menu-title">
      <span>наше меню</span>
    </div>
    <div class="page__menu-content">
      <TitleIconSVG></TitleIconSVG>
      <span class="mini-title">супер популярное!</span>
    </div>
    <div class="page__menu-content-pizzas">
      <template v-for="i in (0, 4)">
        <PizzaCard :key="i"></PizzaCard>
      </template>
    </div>
  </div>
</template>

<script>

import LogoSVG from '@/img/logoSVG.vue';
import BusketSVG from '@/img/busketSVG.vue';
import LkSVG from '@/img/lkSVG.vue';
import TitleIconSVG from '@/img/titleIconSVG.vue';
import PizzaCard from './components/PizzaCard.vue';

export default {
  name: 'App',
  components: {
    LogoSVG,
    BusketSVG,
    LkSVG,
    TitleIconSVG,
    PizzaCard,
  }
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
.page__header{
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.busket_button,.lk_button{
  background-color: #FFE9C1;
  border: 4px solid #CA151C;
  border-radius: 50px;
  width:65px;
  height: 65px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 50px;
  /* justify-self: flex-end; */
}
.page__menu-title{
  background-color: #FFE9C1;
  border: 4px solid #CA151C;
  border-radius: 50px;
  width: 95%;
  height: auto;
  color: #CA151C;
  margin: 30px 50px;
  text-align: center;
  font-family: Nunito;
  font-size: 2.7rem;
  font-weight: 800;
  justify-self: center;
}
.page__menu-content{
  display: flex;
  justify-content: flex-start;
  align-items: center;
  font-family: Nunito;
  font-size: 2.2rem;
  color: #CA151C;
  margin-left: 130px;
}
.mini-title{
  margin-left: 20px;
  margin-bottom: 20px;
}
.page__menu-content-pizzas{
  display: flex;
  justify-content: space-evenly;
  margin: 0px 50px;
}
</style>

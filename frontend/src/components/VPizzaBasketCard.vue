<template>
  <div class="pizza-basket-card">
    
    <img src="../img/pizza.png" class="pizza_pic"/>
    <span class="card-title">пепперони</span>
    <span class="card-price">450 руб.</span>
    <ArrowLeftSVG></ArrowLeftSVG>
    <span class="card-amount">2 шт.</span>
    <ArrowRightSVG></ArrowRightSVG>
    <TrashSVG></TrashSVG>
  </div>
</template>

<script>
import ArrowLeftSVG from '@/img/arrowLeftSVG.vue';
import ArrowRightSVG from '@/img/arrowRightSVG.vue';
import TrashSVG from '@/img/trashSVG.vue';

export default {
  name: 'VPizzaBasketCard',
  components: {
    ArrowLeftSVG,
    ArrowRightSVG,
    TrashSVG,
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.pizza-card{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 390px;
  width: 250px;
  background-color: #FFEFD2;
  border: 3px solid #BF0200;
  border-radius: 30px;
  padding: 20px;
}
.pizza_pic{
  height: 235px;
  width: 224px;
}
.card-title{
  font-family: Nunito;
  font-size: 2.2rem;
  color: #CA151C;
}
.card-price{
  font-family: Nunito;
  font-size: 1.7rem;
  color: #CA151C;
  font-weight: 300;
}
.card-button{
  background-color: #BF0200;
  width: 100%;
  text-align: center;
  border-radius: 25px;
  padding: 8px 0px;
  margin-top: 15px;
}
.card-button__title{
  font-family: Nunito;
  font-size: 1.5rem;
  color: #FFF9ED;
  font-weight: 300;
}
svg{
  align-self: flex-end;
  /* margin: 0px 15px; */
  margin-bottom: -30px;
}
</style>

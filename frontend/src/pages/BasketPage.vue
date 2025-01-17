<template>
    <div class="basket-page">
        <div class="basket-page__header">
          <RouterLink to="/" class="back_button">
            <ArrowLeftSVG></ArrowLeftSVG>
          </RouterLink>
          <div class="basket-page__title">
            <span>корзина</span>
          </div>
        </div>
        <VPizzaBasketCard></VPizzaBasketCard>
        <div class="card-button">
        <span class="card-button__title">очистить корзину</span>
        </div>
        <span class="basket-page__sum">итого: 700 руб.</span>
        <div class="card-button">
          <span class="card-button__title">оформить заказ</span>
        </div>
    </div>
</template>

<script>

import ArrowLeftSVG from '@/img/arrowLeftSVG.vue';
import VPizzaBasketCard from '../components/VPizzaBasketCard.vue'

export default {
  name: 'BasketPage',
  components: {
    ArrowLeftSVG,
    VPizzaBasketCard,
  }
}
</script>

<style>
.basket-page__header{
  width: 100%;
  display: flex;
  align-items: center;
  /* justify-content: center; */
}
.basket-page__title{
  background-color: #FFE9C1;
  border: 4px solid #CA151C;
  border-radius: 50px;
  width: 100%;
  height: auto;
  color: #CA151C;
  margin: 30px 50px;
  text-align: center;
  font-family: Nunito;
  font-size: 2.7rem;
  font-weight: 800;
  justify-self: center;
}

</style>
